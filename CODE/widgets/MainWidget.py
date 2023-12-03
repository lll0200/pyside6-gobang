# coding=utf-8
"""
    @project: GomokuCode
    @Author：念卿 刘
    @file： MainWidget.py
    @date：2023/11/14 21:32
    
"""
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class MainWidget(QWidget):
    """    主窗口的界面部件。    """

    def __init__(self, parent: QWidget = None):
        """ 初始化主窗口界面。 """
        super().__init__(parent)
        self.font = QFont("楷体", 14)
        self.init_ui()

    def init_ui(self):
        """ 构建UI布局和元素。 """
        self.layout = QVBoxLayout(self)
        self.start_game_button = QPushButton("开始游戏")  # 按钮
        self.start_game_button.setFont(self.font)  # 将字体应用于标签
        self.settings_button = QPushButton("游戏设置")
        self.settings_button.setFont(self.font)  # 将字体应用于标签
        self.exit_button = QPushButton("退出游戏")
        self.exit_button.setFont(self.font)  # 将字体应用于标签

        self.layout.addWidget(self.start_game_button)  # 界面添加按钮
        self.layout.addWidget(self.settings_button)
        self.layout.addWidget(self.exit_button)
