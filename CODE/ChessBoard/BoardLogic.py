# coding=utf-8
"""
    @project: GomokuCode
    @Author：念卿 刘
    @file： BoardLogic.py
    @date：2023/11/14 8:11
    棋盘逻辑
"""
import numpy as np
from PySide6.QtCore import QDateTime, QTimer, Qt
from PySide6.QtWidgets import QMessageBox

from AI.a1 import Computer as A1
from AI.a2 import AI as A2
from AI.ai import AiChess
from CODE.ChessBoard.Thread import AiThread, AiVsAiThread

a1 = A1()
a2 = A2()
test = AiChess()
ai_dict = {'a1': a1, "a2": a2, 'test': test}


class BoardLogic:
    """ 棋盘逻辑 """

    def __init__(self, chess=None):
        super().__init__()
        self.chess = chess
        self.old_index = (-1, -1)
        self.pieces_nums = 0  # 棋子数量
        self.play_flag = False  # 是否正在下棋
        self.current_player = 1  # 1 代表玩家1，2 代表玩家2
        self.board = np.zeros((self.chess.board_size, self.chess.board_size), dtype=int)  # 棋盘

    def check_play(self, flag: bool):
        """ 检查是否正在下棋 """
        self.play_flag = flag
        if flag:
            self.chess.setMouseTracking(False)  # 关闭鼠标跟踪
            self.chess.game_window.pause_button.setEnabled(False)  # 禁用暂停游戏按钮
            self.chess.game_window.restart_button.setEnabled(False)  # 禁用重新开始游戏按钮
        else:
            self.chess.setMouseTracking(True)  # 开期鼠标跟踪
            self.chess.game_window.restart_button.setEnabled(True)  # 启用重新开始游戏按钮
            if not self.chess.game_window.game_over:  # 如果游戏结束了，不需要启用暂停游戏按钮
                self.chess.game_window.pause_button.setEnabled(True)  # 启用暂停游戏按钮

    def player_make_move(self, game_x: int = -1, game_y: int = -1):
        """ 玩家下棋 """
        if self.chess.game_window.game_over:  # 如果游戏已经结束，则不需要下棋
            return
        self.check_play(True)  # 锁定棋盘
        if 0 <= game_x < self.chess.board_size and 0 <= game_y < self.chess.board_size:  # 检查是否在棋盘范围内
            self.after_play(game_x, game_y)
        self.check_play(False)  # 解锁棋盘
        self.chess.game_window.lastTime = QDateTime.currentDateTime()  # 记录开始时间

    def ai_make_move(self):
        """AI 下棋逻辑"""
        if self.chess.game_window.game_over:  # 如果游戏已经结束，则不需要下棋
            return
        self.check_play(True)
        if self.chess.game_window.parent.play_mode == 2:
            QTimer.singleShot(100, lambda: self.ai_move_thread(self.chess.game_window.parent.play1))  # 延迟启动线程
        elif self.chess.game_window.parent.play_mode == 1:
            QTimer.singleShot(100, lambda: self.ai_move_thread(self.chess.game_window.parent.play2))  # 延迟启动线程

    def ai_move_thread(self, player):
        """ ai下棋 """

        def ai_task(board, play, index):
            """ 任务 """
            self.chess.game_window.lastTime = QDateTime.currentDateTime()  # 记录开始时间
            x, y = ai_dict[player].start(board, play, index)  # 执行AI计算
            return x, y

        def thread_complete(x, y):
            """ 完成一次后"""
            self.after_play(x, y)
            self.check_play(False)
            self.chess.game_window.lastTime = QDateTime.currentDateTime()  # 更新开始时间
            self.ai_thread.deleteLater()  # 线程结束后释放资源

        self.ai_thread = AiThread(ai_task, self.board.copy(), self.current_player, self.old_index)
        self.ai_thread.completed.connect(thread_complete)
        self.ai_thread.start()

    def after_play(self, x, y):
        """ 在那里落子以及检查棋盘状态 """
        if self.place_piece(x, y):  # 落子
            self.current_player = 3 - self.current_player  # 更新该谁下
            self.chess.current_player_changed.emit(self.current_player)  # 发出信号
            self.check_game_status()  # 判断输、赢、平局
            self.chess.update()

    def ai_random(self):
        """ 超简单电脑 随机下 """
        if self.chess.game_window.game_over:  # 如果游戏已经结束，则不需要下棋
            return
        import random
        while True:
            x = random.randint(0, self.chess.board_size - 1)
            y = random.randint(0, self.chess.board_size - 1)
            self.after_play(x, y)
            break

    def ai_vs_ai(self):
        """ 电脑对战电脑 """
        self.check_play(True)

        def on_ai_completed(x, y):
            """ 线程完成一次之后 """
            self.after_play(x, y)
            if self.chess.game_window.game_over:
                self.check_play(False)
                self.ai_vs_ai_thread.terminate()  # 结束线程

        self.ai_vs_ai_thread = AiVsAiThread(ai_dict[self.chess.game_window.parent.play1].start,
                                            ai_dict[self.chess.game_window.parent.play2].start,
                                            self.chess)
        self.ai_vs_ai_thread.completed.connect(on_ai_completed)
        self.ai_vs_ai_thread.start()

    def has_chess_pieces(self, x, y):
        """  判断x y 位置是否有棋子 有 返回 false 无 返回 true  """
        return self.board[x][y] == 0

    def place_piece(self, x, y):
        """ 落子 """
        if self.chess.board_size > x >= 0 == self.board[x][y] and 0 <= y < self.chess.board_size:
            self.board[x][y] = self.current_player
            self.old_index = (x, y)
            self.pieces_nums = np.count_nonzero(self.board)
            self.chess.pieces_num.emit(self.pieces_nums)  # 发出信号
            self.chess.game_window.update_game_log(f"{self.pieces_nums} 玩家{self.current_player} 落子于{x + 1, y + 1}",
                                                   True)  # 添加日志
            self.chess.setCursor(Qt.ArrowCursor)
            self.chess.corner_widget.hide()
            return True
        return False

    def game_overed(self, win_player=None):
        """ 游戏结束 """
        self.chess.setMouseTracking(False)  # 关闭鼠标跟踪
        self.chess.game_window.game_over = True  # 游戏结束标志
        self.chess.game_window.pause_button.setEnabled(False)  # 禁用暂停游戏按钮
        self.chess.game_window.timer.stop()  # 停止计时
        self.chess.game_window.update_game_log(
            f'{"玩家" if self.chess.game_window.parent.play1 == "None" else self.chess.game_window.parent.play1} PK '
            f'{"玩家" if self.chess.game_window.parent.play2 == "None" else self.chess.game_window.parent.play2}, '
            f'用时: {self.chess.game_window.start_time.toString("mm:ss")}, 共经历{self.pieces_nums}步厮杀, '
            f'{f"玩家{win_player} 赢了"}' if win_player else "双方平局", False)  # 添加日志
        response = QMessageBox.information(self.chess, "游戏结束",
                                           f'{f"恭喜，玩家 {win_player} 赢了！" if win_player else f"平局！"}')  # 游戏结束提示
        if response and self.chess.game_window.parent.save_log:  # 点击确定之后 检查是否开启了自动保存日志功能
            self.chess.game_window.save_game_log()  # 保存日志

    def check_game_status(self):
        """ 判断棋局输赢 返回 是否出现结果 """
        for x in range(self.chess.board_size):  # 出现赢家
            for y in range(self.chess.board_size):
                player = self.board[x][y]
                if player != 0 and self.is_winning_move(x, y, player):
                    self.game_overed(player)  # 游戏结束
                    return True

        if all(self.board[x][y] != 0 for x in range(self.chess.board_size) for y in
               range(self.chess.board_size)):  # 平局
            self.game_overed()  # 游戏结束
            return True

        return False

    def is_winning_move(self, x, y, player):
        """ 判断这一步能否赢 """
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            if self.count_consecutive(x, y, dx, dy, player) >= 5:
                return True
        return False

    def count_consecutive(self, x, y, dx, dy, player):
        """从 (x, y) 开始沿着 (dx, dy) 方向计算连续的相同棋子数"""
        count = 0
        while (0 <= x < self.chess.board_size and 0 <= y < self.chess.board_size and
               self.board[x][y] == player):
            count += 1
            x += dx
            y += dy
        return count

    def reset_board(self):
        """ 重置棋盘 """
        self.board = np.zeros((self.chess.board_size, self.chess.board_size), dtype=int)  # 棋盘
        self.current_player = 1
        self.pieces_nums = 0
        self.play_flag = False  # 是否正在下棋
        self.chess.update()
