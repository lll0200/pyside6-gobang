# coding=utf-8
"""
    @project: GomokuCode
    @Author：念卿 刘
    @file： Thread.py
    @date：2023/11/15 16:13
    
"""
from PySide6.QtCore import QThread, Signal, QDateTime


class AiThread(QThread):
    """ ai线程 """
    completed = Signal(int, int)  # 自定义信号，用于传递AI计算的结果

    def __init__(self, ai_function, board, player, index, parent=None):
        super().__init__(parent)
        self.ai_function = ai_function
        self.board = board
        self.player = player
        self.index = index

    def run(self):
        """ 执行线程 """
        x, y = self.ai_function(self.board, self.player, self.index)  # 获取AI计算的结果
        self.completed.emit(x, y)  # 发出信号


class AiVsAiThread(QThread):
    """ 电脑对电脑的对战 线程 """
    completed = Signal(int, int)  # 自定义信号，用于传递AI计算的结果

    def __init__(self, ai_function1, ai_function2, parent=None):
        super().__init__(parent)
        self.ai_function1 = ai_function1
        self.ai_function2 = ai_function2
        self.parent = parent

    def run(self):
        """执行线程"""
        while not self.parent.game_window.game_over:
            ai_function = self.ai_function1 if self.parent.BoardLogic.current_player == 1 else self.ai_function2
            self.parent.game_window.lastTime = QDateTime.currentDateTime()  # 记录开始时间
            x, y = ai_function(self.parent.BoardLogic.board, self.parent.BoardLogic.current_player,
                               self.parent.BoardLogic.old_index)  # 获取AI计算的结果
            self.parent.BoardLogic.old_index = (x, y)  # 暂时记录上一步下棋位置
            self.completed.emit(x, y)  # 发出信号
            self.msleep(1000)  # 每一步之间添加一些延时
