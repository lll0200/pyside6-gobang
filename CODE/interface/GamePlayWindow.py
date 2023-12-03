# coding=utf-8
"""
    @project: GomokuCode
    @Author：念卿 刘
    @file： GamePlayWindow.py
    @date：2023/11/12 21:46
    
"""
import sys

from PySide6.QtCore import QTimer, Qt, QTime, QDateTime
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QGridLayout, QListWidget

from CODE.ChessBoard.ChessBoard import ChessBoard
from CODE.widgets.CustomWidget import CustomWidget

mode = {0: "人 PK 人", 1: "人 PK 电脑", 2: "电脑 PK 人", 3: "电脑 PK 电脑"}


class GamePlayWindow(QWidget):
    """    游戏界面    """

    def __init__(self, main_window=None):
        super().__init__(main_window)
        self.parent = main_window
        self.is_game_paused = False  # 游戏是否暂停的标志
        self.game_over = False  # 游戏是否结束的标志
        self.chess_board = ChessBoard(self)
        self.chess_board.current_player_changed.connect(self.update_current_player_label)
        self.lastTime = None
        self.stop_continue_Time = None
        self.init_ui()

    def init_ui(self):
        """ 构建主窗口的UI元素和布局。 """

        self.layout = QHBoxLayout(self)  # 创建包含棋盘和按钮容器的水平布局
        self.game_log = QListWidget(self)  # 游戏事件记录
        self.grid_layout = QGridLayout(self)  # 网格布局

        self.pieces_num_label = QLabel("棋子数量: 0")  # 棋子数量
        self.chess_board.pieces_num.connect(self.update_pieces_num_label)
        self.pieces_num_label.setAlignment(Qt.AlignLeft)  # 文字左对齐

        # 添加计时器显示
        self.timer_label = QLabel("游戏时间: 00:00")
        self.timer_label.setAlignment(Qt.AlignLeft)  # 文字左对齐

        # 当前玩家提示
        self.current_player_label = QLabel(f"轮到玩家 1")
        self.current_player_label.setAlignment(Qt.AlignLeft)  # 文字左对齐

        # 游戏模式
        self.game_mode = QLabel("游戏模式")
        self.game_mode.setAlignment(Qt.AlignLeft)  # 文字左对齐

        # 玩家
        self.play1_label = QLabel()
        self.play2_label = QLabel()
        self.play1_label.setAlignment(Qt.AlignLeft)  # 文字左对齐
        self.play2_label.setAlignment(Qt.AlignLeft)  # 文字左对齐

        # 初始化计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.start_time = QTime(0, 0)

        self.grid_layout.addWidget(self.pieces_num_label, 0, 0)
        self.grid_layout.addWidget(self.timer_label, 0, 1)
        self.grid_layout.addWidget(self.current_player_label, 1, 0)
        self.grid_layout.addWidget(self.game_mode, 1, 1)
        self.grid_layout.addWidget(self.play1_label, 2, 0)
        self.grid_layout.addWidget(self.play2_label, 2, 1)

        self.pause_button = QPushButton("暂停游戏")  # 暂停/继续游戏按钮
        self.pause_button.clicked.connect(self.toggle_game_pause)
        self.pause_button.setEnabled(True)

        self.return_button = QPushButton("返回主界面")  # 返回主界面按钮

        self.restart_button = QPushButton("重新开始游戏")  # 添加重新开始游戏按钮
        self.restart_button.clicked.connect(self.restart_game)

        # 使用自定义的 QWidget 来包含返回按钮
        self.right_container = CustomWidget("imag/back.jpg")
        self.right_container_layout = QVBoxLayout(self.right_container)
        self.right_container_layout.addLayout(self.grid_layout)
        self.right_container_layout.addWidget(self.game_log)
        self.right_container_layout.addWidget(self.pause_button)
        self.right_container_layout.addWidget(self.restart_button)
        self.right_container_layout.addWidget(self.return_button)
        # self.right_container_layout.addStretch() #添加一个可伸缩的空间
        self.right_container.setFixedWidth(230)  # 设置容器宽度
        # 设置容器的样式：左边框
        self.right_container.setStyleSheet("border-left: 2px solid black;")

        self.layout.addWidget(self.chess_board)
        self.layout.addWidget(self.right_container)

    def showEvent(self, event):
        """ 界面显示时的操作 """
        self.timer.start(1000)  # 每1000毫秒更新一次
        self.game_mode.setText(f"模式: {mode[self.parent.play_mode]}")
        self.play1_label.setText(f'play1: {"玩家" if self.parent.play1 == "None" else self.parent.play1} 白棋')
        self.play2_label.setText(f'play2: {"玩家" if self.parent.play2 == "None" else self.parent.play2} 黑棋')
        self.chess_board.BoardLogic.reset_board()
        self.current_player_label.setText(f"轮到玩家 {self.chess_board.BoardLogic.current_player}")
        self.pieces_num_label.setText(f"棋子数量: {self.chess_board.BoardLogic.pieces_nums}")
        self.game_log.clear()  # 清空列表显示
        super().showEvent(event)

    def hideEvent(self, event):
        """ 隐藏窗口 """
        self.timer.stop()  # 停止计时器
        self.start_time = QTime(0, 0)  # 重置计时器
        self.timer_label.setText("游戏时间: 00:00")  # 重置计时器显示
        self.is_game_paused = False  # 重置游戏暂停状态
        self.pause_button.setText("暂停游戏")  # 更新暂停按钮文本
        self.pause_button.setEnabled(True)  # 启用暂停按钮 为了防止被禁用的情况下 返回主界面
        self.game_over = False  # 游戏结束标志重置
        super().hideEvent(event)

    def update_current_player_label(self, player_number):
        """更新玩家提示"""
        self.current_player_label.setText(f"轮到玩家 {player_number}")

    def update_pieces_num_label(self, pieces_num):
        """ 更新已下棋子数量 """
        self.pieces_num_label.setText(f"棋子数量: {pieces_num}")

    def toggle_game_pause(self):
        """ 暂停 继续 游戏 """
        if self.game_over:  # 如果游戏结束了，则不需要暂停、继续游戏
            return
        self.is_game_paused = not self.is_game_paused
        if self.is_game_paused:
            self.pause_button.setText("继续游戏")
            self.stop_continue_Time = QDateTime.currentDateTime()  # 记录暂停时间开始时间
            self.timer.stop()
        else:
            self.pause_button.setText("暂停游戏")
            currentTime = QDateTime.currentDateTime()
            self.stop_continue_Time = (self.stop_continue_Time.
                                       msecsTo(currentTime)) / 1000 if self.stop_continue_Time else 0  # 计算暂停了多长时间
            self.timer.start()

    def restart_game(self):
        """ 重新开始游戏 """
        self.chess_board.BoardLogic.reset_board()  # 重置棋盘
        self.start_time = QTime(0, 0)  # 重置计时器
        self.timer_label.setText("游戏时间: 00:00")  # 重置计时器显示
        self.timer.start(1000)  # 每1000毫秒更新一次
        self.is_game_paused = False  # 重置游戏暂停状态
        self.game_over = False  # 重置游戏结束状态
        self.pause_button.setText("暂停游戏")  # 更新暂停按钮文本
        self.current_player_label.setText(f"轮到玩家 {self.chess_board.BoardLogic.current_player}")
        self.pieces_num_label.setText(f"棋子数量: {self.chess_board.BoardLogic.pieces_nums}")
        self.game_log.clear()  # 清空列表显示
        self.chess_board.setMouseTracking(True)  # 开启鼠标跟踪
        self.pause_button.setEnabled(True)  # 启用暂停游戏按钮

        # 判断是否需要电脑下
        if self.parent.play_mode == 2:  # 电脑先下
            self.chess_board.BoardLogic.ai_make_move()
        elif self.parent.play_mode == 3:  # 电脑对战电脑
            self.chess_board.BoardLogic.ai_vs_ai()

    def update_timer(self):
        """ 更新计时器 """
        if not self.is_game_paused:
            self.start_time = self.start_time.addSecs(1)
            self.timer_label.setText(f'游戏时间: {self.start_time.toString("mm:ss")}')

    def update_game_log(self, text, flag: bool = True):
        """更新游戏日志"""
        if flag:
            currentTime = QDateTime.currentDateTime()
            interval_seconds = self.lastTime.msecsTo(currentTime) / 1000 if self.lastTime else 0
            self.stop_continue_Time = self.stop_continue_Time if self.stop_continue_Time else 0
            text += f" 用时: {interval_seconds - self.stop_continue_Time:.3f} s"
            self.stop_continue_Time = None
        self.game_log.addItem(text)  # 添加新的日志条目
        self.game_log.scrollToBottom()  # 滚动到最底部的项

    def save_game_log(self):
        """保存游戏日志到文本文件"""
        items = []  # 获取日志内容
        for index in range(self.game_log.count()):
            item = self.game_log.item(index)
            items.append(item.text())
        file_path = (f"{sys.path[0]}/logs/{self.parent.play1} PK {self.parent.play2} "
                     f"{QDateTime.currentDateTime().toString('yyyy-MM-dd hh_mm_ss')}.txt")  # 指定文件保存路径
        with open(file_path, "w", encoding='utf-8') as file:
            file.write("\n".join(items))
