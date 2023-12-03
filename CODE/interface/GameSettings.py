# coding=utf-8
"""
    @project: GomokuCode
    @Author：念卿 刘
    @file： GameSettings.py
    @date：2023/11/12 21:43
    
"""
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSpinBox, QPushButton, QComboBox, QHBoxLayout,
                               QRadioButton, QGridLayout, QButtonGroup)

from CODE.ChessBoard.BoardLogic import ai_dict

players = list(ai_dict.keys())
players.insert(0, 'None')


class GameSettings(QWidget):
    """    游戏设置    """

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("游戏设置")
        self.min_num = 10
        self.max_num = 20
        self.default_num = 15
        self.players = players
        self.font = QFont("楷体", 14)
        self.init_ui()

    def init_ui(self):
        """ 构建UI布局和元素。 """
        self.layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout(self)  # 网格布局
        self.grid_layout.setVerticalSpacing(22)
        self.chess_size_label = QLabel("设置棋盘大小：")
        self.chess_size_label.setFont(self.font)  # 将字体应用于标签
        self.chess_size_label.setFixedWidth(90)
        self.play1_label = QLabel("设置玩家1：")
        self.play1_label.setFont(self.font)  # 将字体应用于标签
        self.play1_label.setFixedWidth(90)
        self.play2_label = QLabel("设置玩家2：")
        self.play2_label.setFont(self.font)  # 将字体应用于标签
        self.play2_label.setFixedWidth(90)

        self.spinBox = QSpinBox()
        self.spinBox.setRange(self.min_num, self.max_num)
        self.spinBox.setValue(self.default_num)  # 棋盘大小默认值
        self.spinBox.lineEdit().setReadOnly(True)  # 设置 QSpinBox 的 lineEdit 为只读

        self.log_layout = QHBoxLayout(self)
        self.log_label = QLabel("自动保存日志:")
        self.log_label.setFont(self.font)  # 将字体应用于标签
        self.log_radio_group = QButtonGroup()
        self.radioButton1 = QRadioButton("NO")  # 创建两个单选按钮
        self.radioButton2 = QRadioButton("YES")
        self.log_radio_group.addButton(self.radioButton1, 0)  # 将选项 1 添加到按钮组，并分配ID为1
        self.log_radio_group.addButton(self.radioButton2, 1)  # 将选项 2 添加到按钮组，并分配ID为2
        self.radioButton2.setChecked(True)  # 默认选择第二个选项

        self.log_layout.addWidget(self.radioButton1)
        self.log_layout.addWidget(self.radioButton2)

        self.back_button = QPushButton("返回主菜单")
        self.back_button.setFont(self.font)  # 将字体应用于标签
        # 创建一个QComboBox实例
        self.combo_box_1 = QComboBox()
        self.combo_box_2 = QComboBox()
        # 向下拉框中添加选项
        self.combo_box_1.addItems(self.players)
        self.combo_box_2.addItems(self.players)
        self.combo_box_1.currentIndexChanged.connect(self.update_combo_box_2)
        self.combo_box_2.currentIndexChanged.connect(self.update_combo_box_1)
        # 添加布局
        self.grid_layout.addWidget(self.chess_size_label, 0, 0)
        self.grid_layout.addWidget(self.spinBox, 0, 1)
        self.grid_layout.addWidget(self.play1_label, 1, 0)
        self.grid_layout.addWidget(self.combo_box_1, 1, 1)
        self.grid_layout.addWidget(self.play2_label, 2, 0)
        self.grid_layout.addWidget(self.combo_box_2, 2, 1)
        self.grid_layout.addWidget(self.log_label, 4, 0)
        self.grid_layout.addLayout(self.log_layout, 4, 1)
        self.grid_layout.addWidget(self.back_button, 5, 0, 1, 2)

        self.layout.addLayout(self.grid_layout)
        # self.layout.addStretch()  # 添加一个可伸缩的空间

    def update_combo_box_2(self, index):
        """更新下拉框2的选项，使其不能选择下拉框1已选择的选项"""
        current_choice = self.combo_box_1.currentText()
        self.combo_box_2.blockSignals(True)
        for i in range(self.combo_box_2.count()):
            self.combo_box_2.model().item(i).setEnabled(True)
        if self.players[index] == "None":
            self.combo_box_2.blockSignals(False)
            return
        if current_choice in self.combo_box_2.currentText():
            self.combo_box_2.setCurrentIndex((index + 1) % self.combo_box_2.count())
        self.combo_box_2.model().item(index).setEnabled(False)
        self.combo_box_2.blockSignals(False)

    def update_combo_box_1(self, index):
        """更新下拉框1的选项，使其不能选择下拉框2已选择的选项"""
        current_choice = self.combo_box_2.currentText()
        self.combo_box_1.blockSignals(True)
        for i in range(self.combo_box_1.count()):
            self.combo_box_1.model().item(i).setEnabled(True)
        if self.players[index] == "None":
            self.combo_box_1.blockSignals(False)
            return
        if current_choice in self.combo_box_1.currentText():
            self.combo_box_1.setCurrentIndex((index + 1) % self.combo_box_1.count())
        self.combo_box_1.model().item(index).setEnabled(False)
        self.combo_box_1.blockSignals(False)
