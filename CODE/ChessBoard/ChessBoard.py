# coding=utf-8
"""
    @project: GomokuCode
    @Author：念卿 刘
    @file： ChessBoard.py
    @date：2023/11/12 22:24
    
"""
import numpy as np
from PySide6.QtCore import Qt, Signal, QPoint, QDateTime
from PySide6.QtGui import QPainter, QPen, QColor, QRadialGradient
from PySide6.QtWidgets import QWidget

from CODE.ChessBoard.BoardLogic import BoardLogic
from CODE.widgets.corner_widget import CornerWidget


class ChessBoard(QWidget):
    """画棋盘"""
    current_player_changed = Signal(int)  # 定义信号
    pieces_num = Signal(int)  # 定义信号

    def __init__(self, game_window=None):
        super().__init__(game_window)
        self.game_window = game_window
        self.init_params()
        self.BoardLogic = BoardLogic(self)
        self.corner_widget = CornerWidget(self)
        self.corner_widget.hide()

    def init_params(self):
        """ 初始化参数 """
        self.board_size = self.game_window.parent.board_size  # 棋盘大小
        self.cell_size = self.game_window.parent.cell_size  # 格子大小
        self.hover_x, self.hover_y = -1, -1  # 初始鼠标悬停位置
        self.last_pos = (-1, -1)
        self.length = self.board_size * self.cell_size
        self.corner_l = self.cell_size // 2

    def showEvent(self, event):
        """ 界面显示时的操作 """
        self.init_params()
        self.BoardLogic.board = np.zeros((self.board_size, self.board_size), dtype=int)  # 棋盘
        self.game_window.lastTime = QDateTime.currentDateTime()  # 记录开始时间
        self.setMouseTracking(True)  # 开启鼠标跟踪
        super().showEvent(event)
        if self.game_window.parent.play_mode == 2:  # 电脑先下
            self.BoardLogic.ai_make_move()
        elif self.game_window.parent.play_mode == 3:  # 电脑对战电脑
            self.setMouseTracking(False)  # 关闭鼠标跟踪
            self.BoardLogic.ai_vs_ai()

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        # 确保游戏没有暂停 也没有结束 且不为电脑 电脑 对战 也不为正在下棋状态
        if (self.game_window.is_game_paused or self.game_window.game_over or
                self.game_window.parent.play_mode == 3 or self.BoardLogic.play_flag):
            self.setCursor(Qt.ArrowCursor)  # 设置鼠标形状为箭头
            self.corner_widget.hide()  # 鼠标跟踪提示 隐藏
            return
        x = event.x()
        y = event.y()
        if self.corner_l + 5 <= x <= self.length and self.cell_size <= y <= self.length and (
                x % self.cell_size <= self.corner_l - 5 or x % self.cell_size >= self.corner_l + 5) and (
                y % self.cell_size <= self.corner_l - 5 or y % self.cell_size >= self.corner_l + 5):
            game_x = int((x + self.corner_l - 5) // self.cell_size) - 1
            game_y = int((y + self.corner_l - 5) // self.cell_size) - 1
        else:  # 鼠标当前的位置不对应任何一个游戏格子，将其标记为(01, 01
            game_x = -1
            game_y = -1
        # 2. 然后判断鼠标位置较前一时刻是否发生了变化
        pos_change = False  # 标记鼠标位置是否发生了变化
        if game_x != self.last_pos[0] or game_y != self.last_pos[1]:
            pos_change = True
        self.last_pos = (game_x, game_y - 1)
        # 3. 最后根据鼠标位置的变化，绘制特殊标记
        if pos_change and game_x != -1 and game_y != -1:
            # 判断当前鼠标位置是否有棋子  # 如果鼠标位置有棋子，则返回
            if not self.BoardLogic.has_chess_pieces(game_x, game_y):
                return
            self.setCursor(Qt.PointingHandCursor)
            self.corner_widget.move(self.corner_l + 5 + game_x * self.cell_size,
                                    self.corner_l + 5 + game_y * self.cell_size)
            self.corner_widget.show()
        if pos_change and game_x == -1 and game_y == -1:
            self.setCursor(Qt.ArrowCursor)
            self.corner_widget.hide()

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        # 确保游戏没有暂停 也没有结束 且不为电脑 电脑 对战 也不为正在下棋状态
        if (self.game_window.is_game_paused or self.game_window.game_over or
                self.game_window.parent.play_mode == 3 or self.BoardLogic.play_flag):
            return
        if event.button() == Qt.LeftButton:
            # 计算棋盘上的行和列索引
            mouse_x = event.x()
            mouse_y = event.y()
            if (mouse_x % self.cell_size <= self.corner_l - 5 or mouse_x % self.cell_size >= self.corner_l + 5) and (
                    mouse_y % self.cell_size <= self.corner_l - 5 or mouse_y % self.cell_size >= self.corner_l + 5):
                game_x = int((mouse_x + self.corner_l - 5) // self.cell_size) - 1
                game_y = int((mouse_y + self.corner_l - 5) // self.cell_size) - 1
            else:  # 鼠标点击的位置不正确
                return
            # 如果鼠标位置有棋子，则不执行
            if not self.BoardLogic.has_chess_pieces(game_x, game_y):
                return
            if self.game_window.parent.play_mode == 0:  # 人人对战
                self.BoardLogic.player_make_move(game_x, game_y)
            elif self.game_window.parent.play_mode in [1, 2]:  # 人 电脑 对战 or 电脑 人
                self.BoardLogic.player_make_move(game_x, game_y)  # 人下
                self.BoardLogic.ai_make_move()  # 电脑下

    def paintEvent(self, event):
        """画"""
        painter = QPainter(self)
        pen = QPen(QColor(0, 0, 0), 2)
        painter.setPen(pen)

        # 绘制棋盘
        for i in range(self.board_size):
            painter.drawLine(self.cell_size, i * self.cell_size + self.cell_size,
                             self.cell_size * self.board_size, i * self.cell_size + self.cell_size)
            painter.drawLine(i * self.cell_size + self.cell_size, self.cell_size,
                             i * self.cell_size + self.cell_size, self.cell_size * self.board_size)

        # 绘制棋盘中的黑点
        painter.setBrush(QColor(0, 0, 0))
        c = self.cell_size * self.board_size // 2 + self.cell_size - self.cell_size // 2
        painter.drawEllipse(QPoint(c, c), 5, 5)

        # 绘制棋子
        radius = self.cell_size // 2  # 棋子的半径
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.BoardLogic.board[i][j] != 0:
                    # 计算棋子中心的坐标
                    center_x = i * self.cell_size + radius
                    center_y = j * self.cell_size + radius

                    # 创建渐变效果
                    gradient = QRadialGradient(center_x, center_y, radius)
                    gradient.setColorAt(0, QColor(255, 255, 255))

                    if self.BoardLogic.board[i][j] == 1:
                        # 白棋：添加高光和阴影
                        gradient.setColorAt(0.4, QColor(220, 220, 220))
                        gradient.setColorAt(1, QColor(255, 255, 255))
                    else:
                        # 黑棋：添加高光和阴影
                        gradient.setColorAt(0.7, QColor(30, 30, 30))
                        gradient.setColorAt(1, QColor(10, 10, 10))
                    painter.setBrush(gradient)
                    painter.drawEllipse(
                        center_x,
                        center_y,
                        radius * 2,
                        radius * 2
                    )
