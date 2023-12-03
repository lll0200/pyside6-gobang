# coding=utf-8
"""
    @project: GomokuCode
    @Author：念卿 刘
    @file： CustomWidget.py
    @date：2023/11/12 23:20
    
"""
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtWidgets import QWidget


class CustomWidget(QWidget):
    """自定义QWidget"""

    def __init__(self, background, parent=None):
        super().__init__(parent)
        self.background_pixmap = QPixmap(background)

    def paintEvent(self, event):
        """画背景图"""
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_pixmap)
