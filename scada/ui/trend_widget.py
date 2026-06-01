"""Gráfico de tendência dos níveis dos tanques (QtCharts)."""

from collections import deque

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis

import config

_MAX_POINTS = 300  # ~60 s a 200 ms


class TrendWidget(QChartView):
    def __init__(self, parent=None):
        self._chart = QChart()
        super().__init__(self._chart, parent)
        self.setRenderHint(QPainter.Antialiasing)

        self._s1 = QLineSeries()
        self._s1.setName("Nível T1 (%)")
        self._s2 = QLineSeries()
        self._s2.setName("Nível T2 (%)")
        self._chart.addSeries(self._s1)
        self._chart.addSeries(self._s2)
        self._chart.setTitle("Tendência de níveis")

        self._axis_x = QValueAxis()
        self._axis_x.setTitleText("amostras")
        self._axis_y = QValueAxis()
        self._axis_y.setRange(0, 100)
        self._axis_y.setTitleText("%")
        self._chart.addAxis(self._axis_x, Qt.AlignBottom)
        self._chart.addAxis(self._axis_y, Qt.AlignLeft)
        for s in (self._s1, self._s2):
            s.attachAxis(self._axis_x)
            s.attachAxis(self._axis_y)

        self._d1 = deque(maxlen=_MAX_POINTS)
        self._d2 = deque(maxlen=_MAX_POINTS)
        self._k = 0

    def update_values(self, snapshot):
        n1 = snapshot.get("nivel_t1")
        n2 = snapshot.get("nivel_t2")
        if n1 is None and n2 is None:
            return
        self._k += 1
        self._d1.append(QPointF(self._k, config.raw_to_percent(n1 or 0)))
        self._d2.append(QPointF(self._k, config.raw_to_percent(n2 or 0)))
        self._s1.replace(list(self._d1))
        self._s2.replace(list(self._d2))
        lo = self._d1[0].x() if self._d1 else 0
        self._axis_x.setRange(lo, self._k + 1)
