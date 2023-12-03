# coding=utf-8
"""
    @project: GomokuCode
    @Author：念卿 刘
    @file： corner_widget.py
    @date：2023/11/12 22:24

"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QWidget


class CornerWidget(QWidget):
    """ 鼠标跟踪  """

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setFixedSize(30, 30)

    def paintEvent(self, e):
        """        画        """
        qp = QPainter()
        qp.begin(self)
        pen = QPen(Qt.red, 3, Qt.DashDotLine)
        qp.setPen(pen)
        qp.drawLine(0, 8, 0, 0)
        qp.drawLine(0, 0, 8, 0)
        qp.drawLine(22, 0, 28, 0)
        qp.drawLine(28, 0, 28, 8)
        qp.drawLine(28, 22, 28, 28)
        qp.drawLine(28, 28, 20, 28)
        qp.drawLine(8, 28, 0, 28)
        qp.drawLine(0, 28, 0, 22)
