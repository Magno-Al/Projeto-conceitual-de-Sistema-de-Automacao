"""Painel do processo automático: 4 parâmetros + start/stop + estado."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget, QGroupBox, QFormLayout, QVBoxLayout, QHBoxLayout,
    QSpinBox, QDoubleSpinBox, QPushButton, QLabel
)


class AutoPanel(QGroupBox):
    # alvo_t1, tempo_t1, alvo_t2, tempo_t2
    start_requested = Signal(int, float, int, float)
    stop_requested = Signal()

    def __init__(self, parent=None):
        super().__init__("Processo Automático", parent)

        self.alvo_t1 = QSpinBox()
        self.alvo_t1.setRange(0, 100000)
        self.alvo_t1.setValue(8000)
        self.alvo_t1.setSuffix(" (cru)")

        self.tempo_t1 = QDoubleSpinBox()
        self.tempo_t1.setRange(0, 3600)
        self.tempo_t1.setValue(5.0)
        self.tempo_t1.setSuffix(" s")

        self.alvo_t2 = QSpinBox()
        self.alvo_t2.setRange(0, 100000)
        self.alvo_t2.setValue(8000)
        self.alvo_t2.setSuffix(" (cru)")

        self.tempo_t2 = QDoubleSpinBox()
        self.tempo_t2.setRange(0, 3600)
        self.tempo_t2.setValue(5.0)
        self.tempo_t2.setSuffix(" s")

        form = QFormLayout()
        form.addRow("Nível-alvo T1:", self.alvo_t1)
        form.addRow("Tempo de espera T1:", self.tempo_t1)
        form.addRow("Nível-alvo T2:", self.alvo_t2)
        form.addRow("Tempo de espera T2:", self.tempo_t2)

        self.btn_start = QPushButton("Iniciar processo")
        self.btn_stop = QPushButton("Parar")
        self.btn_stop.setEnabled(False)
        self.btn_start.clicked.connect(self._on_start)
        self.btn_stop.clicked.connect(self._on_stop)
        btns = QHBoxLayout()
        btns.addWidget(self.btn_start)
        btns.addWidget(self.btn_stop)

        self.lbl_state = QLabel("Estado: Parado")
        self.lbl_progress = QLabel("—")

        lay = QVBoxLayout(self)
        lay.addLayout(form)
        lay.addLayout(btns)
        lay.addWidget(self.lbl_state)
        lay.addWidget(self.lbl_progress)

    def _on_start(self):
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self._set_params_enabled(False)
        self.start_requested.emit(
            self.alvo_t1.value(), self.tempo_t1.value(),
            self.alvo_t2.value(), self.tempo_t2.value(),
        )

    def _on_stop(self):
        self.stop_requested.emit()
        self._reset_buttons()

    def _reset_buttons(self):
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self._set_params_enabled(True)

    def _set_params_enabled(self, enabled):
        for w in (self.alvo_t1, self.tempo_t1, self.alvo_t2, self.tempo_t2):
            w.setEnabled(enabled)

    # slots conectados ao engine
    def on_state_changed(self, state_text):
        self.lbl_state.setText(f"Estado: {state_text}")
        if state_text in ("Concluído", "Parado"):
            self._reset_buttons()

    def on_progress(self, text):
        self.lbl_progress.setText(text)
