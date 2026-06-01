"""Tabela com todas as tags da planta (ver tudo; escrever comandos)."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QHeaderView
)

import tags
from tags import COIL


class TagTable(QWidget):
    coil_command = Signal(int, bool)

    COLS = ["Tag", "IEC", "Modbus", "Tipo", "Valor", "Ação"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.table = QTableWidget(len(tags.ALL_TAGS), len(self.COLS))
        self.table.setHorizontalHeaderLabels(self.COLS)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self._value_items = {}
        for row, tag in enumerate(tags.ALL_TAGS):
            self.table.setItem(row, 0, QTableWidgetItem(tag.name))
            self.table.setItem(row, 1, QTableWidgetItem(tag.iec))
            self.table.setItem(row, 2, QTableWidgetItem(f"{tag.kind}:{tag.address}"))
            self.table.setItem(row, 3, QTableWidgetItem(tag.kind))
            val_item = QTableWidgetItem("—")
            val_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 4, val_item)
            self._value_items[tag.name] = val_item

            if tag.writable and tag.kind == COIL:
                btn = QPushButton("Alternar")
                btn.clicked.connect(lambda _=False, t=tag: self._toggle(t))
                self.table.setCellWidget(row, 5, btn)
            else:
                ro = QTableWidgetItem("somente leitura")
                ro.setForeground(Qt.gray)
                self.table.setItem(row, 5, ro)

        lay = QVBoxLayout(self)
        lay.addWidget(self.table)
        self._last = {}

    def _toggle(self, tag):
        current = bool(self._last.get(tag.name, 0))
        self.coil_command.emit(tag.address, not current)

    def update_values(self, snapshot):
        self._last = snapshot
        for name, item in self._value_items.items():
            v = snapshot.get(name)
            item.setText("—" if v is None else str(int(v)))
