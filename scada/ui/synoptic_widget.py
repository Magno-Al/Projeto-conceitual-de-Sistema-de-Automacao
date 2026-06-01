"""Sinótico (mímico) animado da planta: 2 tanques desenhados com QPainter."""

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from PySide6.QtWidgets import QWidget

import config


_WATER = QColor(40, 130, 220)
_WATER_TOP = QColor(90, 175, 255)
_TANK = QColor(70, 70, 80)
_OPEN = QColor(40, 190, 90)      # válvula aberta
_CLOSED = QColor(120, 120, 130)  # válvula fechada
_PIPE = QColor(150, 150, 160)
_BG = QColor(28, 30, 36)
_TEXT = QColor(235, 235, 240)
_ALARM = QColor(220, 60, 60)


class SynopticWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(520, 380)
        self._values = {}

    def update_values(self, snapshot: dict):
        self._values = snapshot
        self.update()

    # ------------------------------------------------------------- helpers
    def _v(self, name, default=0):
        v = self._values.get(name)
        return default if v is None else v

    def _valve_open(self, name):
        return self._v(name, 0) and self._v(name, 0) > 0

    # ------------------------------------------------------------- painting
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(), _BG)

        w = self.width()
        tank_w = 150
        gap = (w - 2 * tank_w) / 3
        y_top = 70
        tank_h = 230

        self._draw_tank(
            p, x=gap, y=y_top, w=tank_w, h=tank_h, title="TANQUE 1",
            nivel="nivel_t1", v_in="valv_entrada_t1", v_out="valv_saida_t1",
            led="led_start_t1", emerg="bt_emerg_t1",
        )
        self._draw_tank(
            p, x=2 * gap + tank_w, y=y_top, w=tank_w, h=tank_h, title="TANQUE 2",
            nivel="nivel_t2", v_in="valv_entrada_t2", v_out="valv_saida_t2",
            led="led_start_t2", emerg="bt_emerg_t2",
        )
        p.end()

    def _draw_tank(self, p, x, y, w, h, title, nivel, v_in, v_out, led, emerg):
        pct = config.raw_to_percent(self._v(nivel, 0))

        # título
        p.setPen(_TEXT)
        f = QFont()
        f.setBold(True)
        f.setPointSize(11)
        p.setFont(f)
        p.drawText(QRectF(x, y - 50, w, 22), Qt.AlignCenter, title)

        # tubulação de entrada (topo) + válvula
        in_open = self._valve_open(v_in)
        p.setPen(QPen(_PIPE, 6))
        p.drawLine(int(x + w / 2), int(y - 6), int(x + w / 2), int(y))
        self._draw_valve(p, x + w / 2, y - 18, in_open)

        # corpo do tanque
        body = QRectF(x, y, w, h)
        p.setPen(QPen(_TANK, 3))
        p.setBrush(QBrush(QColor(20, 22, 28)))
        p.drawRect(body)

        # água
        water_h = (h - 6) * (pct / 100.0)
        if water_h > 0:
            wr = QRectF(x + 3, y + h - 3 - water_h, w - 6, water_h)
            p.setBrush(QBrush(_WATER))
            p.setPen(Qt.NoPen)
            p.drawRect(wr)
            p.setBrush(QBrush(_WATER_TOP))
            p.drawRect(QRectF(wr.x(), wr.y(), wr.width(), min(6, water_h)))

        # texto de nível
        p.setPen(_TEXT)
        f2 = QFont()
        f2.setPointSize(13)
        f2.setBold(True)
        p.setFont(f2)
        p.drawText(body, Qt.AlignCenter, f"{pct:0.0f}%\n({self._v(nivel, 0)})")

        # tubulação de saída (base) + válvula
        out_open = self._valve_open(v_out)
        p.setPen(QPen(_PIPE, 6))
        p.drawLine(int(x + w / 2), int(y + h), int(x + w / 2), int(y + h + 22))
        self._draw_valve(p, x + w / 2, y + h + 28, out_open)

        # indicadores: LED start e emergência
        led_on = bool(self._v(led, 0))
        # emergência é NF (1 = não pressionado / OK; 0 = pressionado / alarme)
        emerg_alarm = self._v(emerg, 1) == 0
        self._draw_led(p, x + 8, y + h + 46, "START", led_on, _OPEN)
        self._draw_led(p, x + 8, y + h + 64, "EMERG", emerg_alarm, _ALARM)

    def _draw_valve(self, p, cx, cy, is_open):
        color = _OPEN if is_open else _CLOSED
        p.setPen(QPen(_TANK, 2))
        p.setBrush(QBrush(color))
        r = 9
        p.drawEllipse(QRectF(cx - r, cy - r, 2 * r, 2 * r))

    def _draw_led(self, p, x, y, label, on, on_color):
        p.setBrush(QBrush(on_color if on else QColor(60, 60, 66)))
        p.setPen(QPen(_TANK, 1))
        p.drawEllipse(QRectF(x, y, 12, 12))
        p.setPen(_TEXT)
        f = QFont()
        f.setPointSize(8)
        p.setFont(f)
        p.drawText(int(x + 18), int(y + 11), label)
