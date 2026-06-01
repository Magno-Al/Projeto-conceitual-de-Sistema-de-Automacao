import time
from enum import Enum

from PySide6.QtCore import QObject, QTimer, Signal

import tags


class State(Enum):
    IDLE = "Parado"
    FILL_T1 = "Enchendo T1"
    HOLD_T1 = "Aguardando em T1"
    DRAIN_T1_FILL_T2 = "Esvaziando T1 / Enchendo T2"
    HOLD_T2 = "Aguardando em T2"
    DRAIN_T2 = "Esvaziando T2"
    DONE = "Concluído"


class ProcessEngine(QObject):
    coil_command = Signal(int, bool)
    state_changed = Signal(str)    
    progress = Signal(str)            

    TICK_MS = 200

    def __init__(self, parent=None):
        super().__init__(parent)
        self._state = State.IDLE
        self._timer = QTimer(self)
        self._timer.setInterval(self.TICK_MS)
        self._timer.timeout.connect(self._tick)

        # parâmetros do processo
        self._alvo_t1 = 0
        self._tempo_t1 = 0.0
        self._alvo_t2 = 0
        self._tempo_t2 = 0.0

        # nível corrente 
        self._nivel_t1 = 0
        self._nivel_t2 = 0

        self._hold_until = 0.0
        self._desired = {c.address: False for c in tags.COMMAND_COILS}

    # ------------------------------------------------------------------ API
    def update_values(self, snapshot: dict):
        """Recebe o snapshot do worker Modbus (níveis ao vivo)."""
        if snapshot.get("nivel_t1") is not None:
            self._nivel_t1 = snapshot["nivel_t1"]
        if snapshot.get("nivel_t2") is not None:
            self._nivel_t2 = snapshot["nivel_t2"]

    def start(self, alvo_t1: int, tempo_t1: float, alvo_t2: int, tempo_t2: float):
        self._alvo_t1 = alvo_t1
        self._tempo_t1 = tempo_t1
        self._alvo_t2 = alvo_t2
        self._tempo_t2 = tempo_t2
        self._enter(State.FILL_T1)
        self._timer.start()

    def stop(self):
        """Parada segura: desliga todos os comandos e volta para IDLE."""
        self._timer.stop()
        self._all_off()
        self._enter(State.IDLE)

    @property
    def state(self) -> State:
        return self._state

    # ------------------------------------------------------------- internos
    def _enter(self, state: State):
        self._state = state
        self.state_changed.emit(state.value)
        if state in (State.HOLD_T1,):
            self._hold_until = time.monotonic() + self._tempo_t1
        elif state in (State.HOLD_T2,):
            self._hold_until = time.monotonic() + self._tempo_t2

    def _set_coil(self, tag, value: bool):
        if self._desired.get(tag.address) != value:
            self._desired[tag.address] = value
            self.coil_command.emit(tag.address, value)

    def _all_off(self):
        for c in tags.COMMAND_COILS:
            self._set_coil(c, False)

    def _tick(self):
        s = self._state

        if s == State.FILL_T1:
            self._set_coil(tags.CMD_FILL_T1, True)
            self._set_coil(tags.CMD_DRAIN_T1, False)
            self.progress.emit(f"T1 {self._nivel_t1} / alvo {self._alvo_t1}")
            if self._nivel_t1 >= self._alvo_t1:
                self._set_coil(tags.CMD_FILL_T1, False)
                self._enter(State.HOLD_T1)

        elif s == State.HOLD_T1:
            self._all_off()
            restante = max(0.0, self._hold_until - time.monotonic())
            self.progress.emit(f"Aguardando T1: {restante:0.1f}s")
            if restante <= 0:
                self._enter(State.DRAIN_T1_FILL_T2)

        elif s == State.DRAIN_T1_FILL_T2:
            self._set_coil(tags.CMD_DRAIN_T1, True)
            self._set_coil(tags.CMD_FILL_T2, True)
            self.progress.emit(
                f"T1 {self._nivel_t1} | T2 {self._nivel_t2} / alvo {self._alvo_t2}"
            )
            if self._nivel_t2 >= self._alvo_t2:
                self._set_coil(tags.CMD_FILL_T2, False)
                self._set_coil(tags.CMD_DRAIN_T1, False)
                self._enter(State.HOLD_T2)

        elif s == State.HOLD_T2:
            self._all_off()
            restante = max(0.0, self._hold_until - time.monotonic())
            self.progress.emit(f"Aguardando T2: {restante:0.1f}s")
            if restante <= 0:
                self._enter(State.DRAIN_T2)

        elif s == State.DRAIN_T2:
            self._set_coil(tags.CMD_DRAIN_T2, True)
            self.progress.emit(f"Esvaziando T2: nível {self._nivel_t2}")
            if self._nivel_t2 <= 0:
                self._set_coil(tags.CMD_DRAIN_T2, False)
                self._all_off()
                self._enter(State.DONE)
                self._timer.stop()
