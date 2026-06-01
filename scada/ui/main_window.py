"""Janela principal do SCADA: barra de conexão + sinótico + painéis."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTabWidget, QStatusBar
)

import config
from plc.modbus_worker import ModbusWorker
from core.process_engine import ProcessEngine
from ui.synoptic_widget import SynopticWidget
from ui.manual_panel import ManualPanel
from ui.auto_panel import AutoPanel
from ui.tag_table import TagTable
from ui.trend_widget import TrendWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SCADA — Planta de 2 Tanques (OpenPLC / Factory I/O)")
        self.resize(1000, 720)

        # ---------------- backend ----------------
        self.worker = ModbusWorker()
        self.engine = ProcessEngine()

        # ---------------- barra de conexão ----------------
        self.host_edit = QLineEdit(config.MODBUS_HOST)
        self.host_edit.setMaximumWidth(140)
        self.port_edit = QLineEdit(str(config.MODBUS_PORT))
        self.port_edit.setMaximumWidth(70)
        self.btn_connect = QPushButton("Conectar")
        self.btn_disconnect = QPushButton("Desconectar")
        self.btn_disconnect.setEnabled(False)
        conn_bar = QHBoxLayout()
        conn_bar.addWidget(QLabel("Servidor OpenPLC:"))
        conn_bar.addWidget(self.host_edit)
        conn_bar.addWidget(QLabel("Porta:"))
        conn_bar.addWidget(self.port_edit)
        conn_bar.addWidget(self.btn_connect)
        conn_bar.addWidget(self.btn_disconnect)
        conn_bar.addStretch()

        # ---------------- widgets ----------------
        self.synoptic = SynopticWidget()
        self.manual = ManualPanel()
        self.auto = AutoPanel()
        self.tag_table = TagTable()
        self.trend = TrendWidget()

        tabs = QTabWidget()
        tabs.addTab(self._wrap(self.manual, self.auto), "Controle")
        tabs.addTab(self.tag_table, "Tags")
        tabs.addTab(self.trend, "Tendência")

        central = QWidget()
        lay = QVBoxLayout(central)
        lay.addLayout(conn_bar)
        lay.addWidget(self.synoptic, stretch=3)
        lay.addWidget(tabs, stretch=2)
        self.setCentralWidget(central)

        self.setStatusBar(QStatusBar())
        self._set_status(False, "Desconectado")

        # ---------------- ligações ----------------
        self.btn_connect.clicked.connect(self._connect)
        self.btn_disconnect.clicked.connect(self._disconnect)

        self.worker.values_updated.connect(self.synoptic.update_values)
        self.worker.values_updated.connect(self.manual.update_values)
        self.worker.values_updated.connect(self.tag_table.update_values)
        self.worker.values_updated.connect(self.trend.update_values)
        self.worker.values_updated.connect(self.engine.update_values)
        self.worker.connection_changed.connect(self._on_connection_changed)

        # comandos (coils) -> worker
        self.manual.coil_command.connect(self.worker.write_coil)
        self.tag_table.coil_command.connect(self.worker.write_coil)
        self.engine.coil_command.connect(self.worker.write_coil)

        # processo automático
        self.auto.start_requested.connect(self.engine.start)
        self.auto.stop_requested.connect(self.engine.stop)
        self.engine.state_changed.connect(self.auto.on_state_changed)
        self.engine.progress.connect(self.auto.on_progress)

    @staticmethod
    def _wrap(*widgets):
        w = QWidget()
        lay = QVBoxLayout(w)
        for x in widgets:
            lay.addWidget(x)
        lay.addStretch()
        return w

    # ------------------------------------------------------------- conexão
    def _connect(self):
        try:
            port = int(self.port_edit.text())
        except ValueError:
            self._set_status(False, "Porta inválida")
            return
        self.worker.configure(self.host_edit.text().strip(), port)
        if not self.worker.isRunning():
            self.worker.start()
        self.btn_connect.setEnabled(False)
        self.btn_disconnect.setEnabled(True)

    def _disconnect(self):
        self.engine.stop()
        self.worker.stop()
        self.worker.wait(2000)
        self.btn_connect.setEnabled(True)
        self.btn_disconnect.setEnabled(False)
        self._set_status(False, "Desconectado")

    def _on_connection_changed(self, connected, msg):
        self._set_status(connected, msg)

    def _set_status(self, connected, msg):
        cor = "#2ecc71" if connected else "#e74c3c"
        self.statusBar().showMessage(msg)
        self.statusBar().setStyleSheet(f"color: {cor};")

    def closeEvent(self, event):
        self.engine.stop()
        self.worker.stop()
        self.worker.wait(2000)
        super().closeEvent(event)
