"""Painel de controle manual ponto a ponto (por tanque)."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
)

import tags


class _TankControls(QGroupBox):
    """Botões Encher / Pausar / Esvaziar para um tanque."""

    # (address, value)
    coil_command = Signal(int, bool)

    def __init__(self, title, fill_tag, drain_tag, parent=None):
        super().__init__(title, parent)
        self._fill = fill_tag
        self._drain = drain_tag

        self.btn_fill = QPushButton("Encher")
        self.btn_pause = QPushButton("Pausar")
        self.btn_drain = QPushButton("Esvaziar")
        self.status = QLabel("—")

        self.btn_fill.clicked.connect(self._on_fill)
        self.btn_pause.clicked.connect(self._on_pause)
        self.btn_drain.clicked.connect(self._on_drain)

        row = QHBoxLayout()
        row.addWidget(self.btn_fill)
        row.addWidget(self.btn_pause)
        row.addWidget(self.btn_drain)

        lay = QVBoxLayout(self)
        lay.addLayout(row)
        lay.addWidget(self.status)

    def _on_fill(self):
        # encher: abre entrada, fecha saída
        self.coil_command.emit(self._fill.address, True)
        self.coil_command.emit(self._drain.address, False)

    def _on_pause(self):
        # pausar: fecha ambas as válvulas (nível segura)
        self.coil_command.emit(self._fill.address, False)
        self.coil_command.emit(self._drain.address, False)

    def _on_drain(self):
        # esvaziar: abre saída, fecha entrada
        self.coil_command.emit(self._fill.address, False)
        self.coil_command.emit(self._drain.address, True)

    def update_status(self, snapshot, nivel_tag, vin_tag, vout_tag):
        nivel = snapshot.get(nivel_tag.name)
        vin = snapshot.get(vin_tag.name)
        vout = snapshot.get(vout_tag.name)
        estado = "entrada ABERTA" if (vin or 0) > 0 else (
            "saída ABERTA" if (vout or 0) > 0 else "fechado")
        self.status.setText(f"Nível: {nivel}  |  {estado}")


class ManualPanel(QWidget):
    coil_command = Signal(int, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.t1 = _TankControls("Tanque 1", tags.CMD_FILL_T1, tags.CMD_DRAIN_T1)
        self.t2 = _TankControls("Tanque 2", tags.CMD_FILL_T2, tags.CMD_DRAIN_T2)
        self.t1.coil_command.connect(self.coil_command)
        self.t2.coil_command.connect(self.coil_command)

        lay = QHBoxLayout(self)
        lay.addWidget(self.t1)
        lay.addWidget(self.t2)

    def update_values(self, snapshot):
        self.t1.update_status(snapshot, tags.NIVEL_T1, tags.VALV_ENTRADA_T1, tags.VALV_SAIDA_T1)
        self.t2.update_status(snapshot, tags.NIVEL_T2, tags.VALV_ENTRADA_T2, tags.VALV_SAIDA_T2)
