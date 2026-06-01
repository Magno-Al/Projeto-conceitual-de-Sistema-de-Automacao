import inspect
import queue

from PySide6.QtCore import QThread, Signal

from pymodbus.client import ModbusTcpClient


def _unit_kwarg_name() -> str:
    """pymodbus mudou o nome do parâmetro de unidade entre versões
    (`unit` -> `slave` -> `device_id`). Detecta o nome correto em runtime."""
    params = inspect.signature(ModbusTcpClient.read_coils).parameters
    for name in ("device_id", "slave", "unit"):
        if name in params:
            return name
    return "slave"


_UNIT_KW = _unit_kwarg_name()

import config
import tags
from tags import DISCRETE_INPUT, COIL, INPUT_REGISTER, HOLDING_REGISTER


# Quantidade de registradores/bits lidos por ciclo (cobre todos os endereços usados)
_READ_DI_COUNT = 8       # discrete inputs 0..7
_READ_COIL_COUNT = 24    # coils 0..23 (inclui comandos 16..20)
_READ_IR_COUNT = 6       # input registers 0..5
_READ_HR_COUNT = 8       # holding registers 0..7


class ModbusWorker(QThread):
    # snapshot {tag_name: valor} a cada ciclo de polling
    values_updated = Signal(dict)
    # (conectado?, mensagem)
    connection_changed = Signal(bool, str)

    def __init__(self, host=None, port=None, parent=None):
        super().__init__(parent)
        self._host = host or config.MODBUS_HOST
        self._port = port or config.MODBUS_PORT
        self._unit = config.MODBUS_UNIT_ID
        self._client = None
        self._running = False
        self._connected = False
        self._write_queue: "queue.Queue[tuple]" = queue.Queue()

    # ------------------------------------------------------------------ API
    def configure(self, host: str, port: int):
        """Atualiza host/porta (aplicado na próxima reconexão)."""
        self._host = host
        self._port = port

    def write_coil(self, address: int, value: bool):
        self._write_queue.put(("coil", address, bool(value)))

    def write_register(self, address: int, value: int):
        self._write_queue.put(("register", address, int(value)))

    def stop(self):
        self._running = False

    # --------------------------------------------------------------- thread
    def run(self):
        self._running = True
        self._client = ModbusTcpClient(
            host=self._host, port=self._port, timeout=config.MODBUS_TIMEOUT
        )
        while self._running:
            if not self._connected:
                self._try_connect()
                if not self._connected:
                    self.msleep(1000)
                    continue
            try:
                self._drain_writes()
                snapshot = self._poll()
                self.values_updated.emit(snapshot)
            except Exception as exc:  # erro de E/S -> tenta reconectar
                self._set_connected(False, f"Erro de comunicação: {exc}")
                try:
                    self._client.close()
                except Exception:
                    pass
            self.msleep(config.POLL_INTERVAL_MS)

        if self._client is not None:
            try:
                self._client.close()
            except Exception:
                pass
        self._set_connected(False, "Desconectado")

    # ------------------------------------------------------------- internos
    def _try_connect(self):
        # recria o cliente para refletir host/porta atuais
        try:
            self._client.close()
        except Exception:
            pass
        self._client = ModbusTcpClient(
            host=self._host, port=self._port, timeout=config.MODBUS_TIMEOUT
        )
        ok = self._client.connect()
        if ok:
            self._set_connected(True, f"Conectado a {self._host}:{self._port}")
        else:
            self._set_connected(False, f"Falha ao conectar em {self._host}:{self._port}")

    def _set_connected(self, state: bool, msg: str):
        if state != self._connected:
            self._connected = state
            self.connection_changed.emit(state, msg)
        elif not state:
            # mantém a mensagem de erro atualizada mesmo sem mudança de estado
            self.connection_changed.emit(state, msg)

    def _drain_writes(self):
        while True:
            try:
                kind, address, value = self._write_queue.get_nowait()
            except queue.Empty:
                break
            if kind == "coil":
                self._client.write_coil(address, value, **{_UNIT_KW: self._unit})
            else:
                self._client.write_register(address, value, **{_UNIT_KW: self._unit})

    def _poll(self) -> dict:
        di = self._read_bits(self._client.read_discrete_inputs, 0, _READ_DI_COUNT)
        coils = self._read_bits(self._client.read_coils, 0, _READ_COIL_COUNT)
        irs = self._read_regs(self._client.read_input_registers, 0, _READ_IR_COUNT)
        hrs = self._read_regs(self._client.read_holding_registers, 0, _READ_HR_COUNT)

        snapshot = {}
        for tag in tags.ALL_TAGS:
            if tag.kind == DISCRETE_INPUT:
                snapshot[tag.name] = self._at(di, tag.address)
            elif tag.kind == COIL:
                snapshot[tag.name] = self._at(coils, tag.address)
            elif tag.kind == INPUT_REGISTER:
                snapshot[tag.name] = self._at(irs, tag.address)
            elif tag.kind == HOLDING_REGISTER:
                snapshot[tag.name] = self._at(hrs, tag.address)
        return snapshot

    def _read_bits(self, fn, address, count):
        resp = fn(address, count=count, **{_UNIT_KW: self._unit})
        if resp.isError():
            raise IOError(str(resp))
        return resp.bits

    def _read_regs(self, fn, address, count):
        resp = fn(address, count=count, **{_UNIT_KW: self._unit})
        if resp.isError():
            raise IOError(str(resp))
        return resp.registers

    @staticmethod
    def _at(arr, idx):
        return arr[idx] if 0 <= idx < len(arr) else None
