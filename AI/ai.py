# coding=utf-8
"""
    @project: GomokuCode
    @Author：念卿 刘
    @file： ai.py
    @date：2023/11/15 17:23
    
"""
# 并发编程和并行计算
import random

import numpy as np


class AiChess:
    """ 五子棋AI类(五子棋) """

    def __init__(self):
        self.BOARD_SIZE = 15  # 棋盘大小
        self.board = None
        self.PLAYER_PIECE = 1  # 玩家一
        self.OPPONENT_PIECE = 2  # 玩家二
        self.EMPTY = 0  # 空
        self.MAX_DEPTH = 3  # 最大搜索深度
        self.transposition_table = {}  # 置换表，用于存储已经搜索过的棋局（节点）及其评估结果
        self.killer_moves = [(-1, -1), (-1, -1)]  # 杀手启发式表
        # 定义棋型对应的分数
        self.patterns_scores = {
            (1, 1, 1, 1, 1): 100000,  # 连五
            (0, 1, 1, 1, 1, 0): 10000,  # 活四
            (1, 1, 1, 1, 0): 5000,  # 冲四
            (0, 1, 1, 1, 0): 1000,  # 活三
            (1, 1, 1, 0, 0): 500,  # 眠三
            (0, 1, 1, 0): 200,  # 活二
            (1, 1, 0, 0): 100,  # 眠二
            # 双活三
            (0, 1, 1, 0, 1, 1, 0): 5000,
            # 活三死四
            (1, 1, 1, 1, 0, 1, 1, 0): 5000,
            # 跳活三
            (0, 1, 0, 1, 1, 0): 1000,
            (0, 1, 1, 0, 1, 0): 1000,
            # 双死四
            (1, 1, 1, 1, 0, 1, 1, 1): 10000,
            # 复杂棋型
            (0, 1, 1, 0, 1, 0, 1): 3000,  # 跳活三
            (0, 1, 0, 1, 0, 1, 1, 0): 3000,  # 跳活三
            (0, 1, 1, 1, 0, 1, 0): 4000,  # 活三眠三
            (1, 1, 0, 1, 1): 3000,  # 断活四
            (1, 0, 1, 1, 1, 0): 4000,  # 断活四
            (0, 1, 0, 1, 1, 1, 0): 4000,  # 断活四
            (1, 0, 1, 1, 0, 1): 3000,  # 断活四
            (1, 1, 0, 1, 0, 1): 3000,  # 断活四
            (0, 1, 1, 0, 1, 0, 1, 0): 3500,  # 跳活三和眠三
            (0, 1, 0, 1, 1, 0, 1): 2500,  # 跳活三
            (1, 0, 1, 1, 1): 4000,  # 断四
            (1, 1, 1, 0, 1): 4000,  # 断四
            (0, 1, 1, 0, 1, 1): 3000,  # 跳活三
            (1, 1, 0, 1, 1, 0): 3000,  # 跳活三
            (0, 1, 0, 1, 0, 1, 0): 2000,  # 跳眠三
            (1, 0, 1, 0, 1, 1): 2500,  # 断四与活二
            (1, 1, 0, 1, 0, 1, 1): 4500,  # 死四与活三
            (1, 0, 1, 0, 1, 1, 0): 3000,  # 断四与活二
            # ... 可以继续添加更多复杂棋型的评分
        }

    def start(self, board, player, index):
        """ 启动AI决策过程，并使用并行搜索返回最佳走法 """
        self.BOARD_SIZE, _ = board.shape
        self.board = np.copy(board)  # 创建棋盘的副本，以免直接修改原棋盘
        self.PLAYER_PIECE = player
        self.OPPONENT_PIECE = 1 if player == 2 else 2
        print(self.PLAYER_PIECE, self.OPPONENT_PIECE)
        # 动态调整搜索深度
        self.MAX_DEPTH = self.adjust_search_depth(self.board)
        """ 迭代加深搜索 """
        best_move = self.iterative_deepening_search(self.board, self.MAX_DEPTH, True)
        """ 并行搜索 """
        # # 获取所有可能的走法
        # possible_moves = self.get_possible_moves(self.board)
        #
        # # 使用并行搜索 并行搜索方法会创建多个线程，每个线程都在评估一个不同的走法
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     futures = {executor.submit(self.simulate_move, move,
        #                                self.MAX_DEPTH, self.board, is_maximizing_player):
        #                    move for move in possible_moves}
        #     best_move = None
        #     best_eval = float('-inf') if is_maximizing_player else float('inf')
        #
        #     for future in concurrent.futures.as_completed(futures):
        #         move = futures[future]
        #         eval_ = future.result()
        #         if (is_maximizing_player and eval_ > best_eval) or (not is_maximizing_player and eval_ < best_eval):
        #             best_eval = eval_
        #             best_move = move

        if not best_move:
            print('随机')
            best_move = self.random_play()
        return best_move

    def evaluate_board(self, board):
        """ 考虑不同的模式，评估给定玩家的棋盘 """
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 水平，垂直，对角线

        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                if board[x][y] == self.PLAYER_PIECE:
                    for dx, dy in directions:
                        line = [self.get_cell(board, x + i * dx, y + i * dy) for i in range(-4, 5)]
                        score += self.evaluate_line(line, self.PLAYER_PIECE)
        return score

    def evaluate_line(self, line, player):
        """ 直接使用数值对一行9个单元格进行评分 """
        score = 0

        # 遍历每个窗口，检查是否匹配某个棋型
        for i in range(len(line) - 4):
            window = tuple(line[i:i + 5])  # 5格窗口
            if window in self.patterns_scores:
                score += self.patterns_scores[window]

        # 如果是对手的棋型，分数取负
        if player != self.PLAYER_PIECE:
            score = -score

        return score

    def get_cell(self, board, x, y):
        """ 安全地获得单元格值;如果越界则返回None """
        if 0 <= x < self.BOARD_SIZE and 0 <= y < self.BOARD_SIZE:
            return board[x][y]
        return None

    def is_terminal_node(self, board):
        """ 检查游戏是否已经结束——无论是赢还是平 """
        # Check for a win
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                if board[x][y] != self.EMPTY:
                    # Check horizontally
                    if y <= self.BOARD_SIZE - 5:
                        if all(board[x][y + i] == board[x][y] for i in range(5)):
                            return True
                    # Check vertically
                    if x <= self.BOARD_SIZE - 5:
                        if all(board[x + i][y] == board[x][y] for i in range(5)):
                            return True
                    # Check diagonal (top-left to bottom-right)
                    if x <= self.BOARD_SIZE - 5 and y <= self.BOARD_SIZE - 5:
                        if all(board[x + i][y + i] == board[x][y] for i in range(5)):
                            return True
                    # Check diagonal (bottom-left to top-right)
                    if x >= 4 and y <= self.BOARD_SIZE - 5:
                        if all(board[x - i][y + i] == board[x][y] for i in range(5)):
                            return True

        # Check for a draw (no empty spaces)
        if all(board[x][y] != self.EMPTY for x in range(self.BOARD_SIZE) for y in range(self.BOARD_SIZE)):
            return True

        return False

    def get_possible_moves(self, board):
        """ 只在现有棋子附近生成移动，以减少搜索空间 """
        moves = set()
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                if board[x][y] == self.EMPTY:
                    # Check if the empty cell is near an existing piece
                    if any(board[x + dx][y + dy] != self.EMPTY
                           for dx in range(-1, 2) for dy in range(-1, 2)
                           if 0 <= x + dx < self.BOARD_SIZE and 0 <= y + dy < self.BOARD_SIZE):
                        moves.add((x, y))
        return list(moves)

    def minimax_alpha_beta(self, board, depth, alpha, beta, is_maximizing):
        """ 极大极小和修剪 """
        # 检查棋盘状态是否在换位表中
        # board_state = tuple(map(tuple, board))
        # if board_state in self.transposition_table:
        #     return self.transposition_table[board_state]

        if depth == 0 or self.is_terminal_node(board):
            # 当depth为0或者达到终止节点（即游戏结束的状态）时，返回当前棋盘的评估分数。
            return None, self.evaluate_board(board)
        # 如果是is_maximizing玩家（通常是AI自己），则尝试最大化评估分数；否则，尝试最小化评估分数
        # 通过递归地调用自身，并在每一层上切换is_maximizing参数，来模拟双方玩家的最佳走法
        if is_maximizing:
            max_eval = float('-inf')
            best_move = None
            possible_move = self.get_possible_moves(board)
            for move in possible_move:
                board[move[0]][move[1]] = self.PLAYER_PIECE
                _, eval_ = self.minimax_alpha_beta(board, depth - 1, alpha, beta, False)
                board[move[0]][move[1]] = self.EMPTY
                if eval_ > max_eval:
                    max_eval = eval_
                    best_move = move

                alpha = max(alpha, eval_)
                if beta <= alpha:
                    break
            # 返回之前将结果保存在换位表中
            # self.transposition_table[board_state] = (best_move, max_eval)
            return best_move, max_eval
        else:
            min_eval = float('inf')
            best_move = None
            for move in self.get_possible_moves(board):
                board[move[0]][move[1]] = self.OPPONENT_PIECE
                _, eval_ = self.minimax_alpha_beta(board, depth - 1, alpha, beta, True)
                board[move[0]][move[1]] = self.EMPTY
                if eval_ < min_eval:
                    min_eval = eval_
                    best_move = move

                beta = min(beta, eval_)
                if beta <= alpha:
                    break
            # 返回之前将结果保存在换位表中
            # self.transposition_table[board_state] = (best_move, min_eval)
            return best_move, min_eval

    def iterative_deepening_search(self, board, max_depth, is_maximizing_player):
        """ 迭代加深搜索 """
        """ 结合了深度优先搜索（Depth-First Search, DFS）和广度优先搜索（Breadth-First Search, BFS）的特点，
        逐渐增加搜索深度，直到找到解为止 """
        best_move = None
        best_eval = float('-inf')

        for depth in range(1, max_depth + 1):
            move, eval_ = self.minimax_alpha_beta(board, depth, float('-inf'), float('inf'), is_maximizing_player)
            if move and eval_ > best_eval:
                best_move = move
                best_eval = eval_

        return best_move

    def random_play(self):
        """ 如果α - β没有解，就随机进行 """
        empty_cells = [(x, y) for x in range(self.BOARD_SIZE) for y in range(self.BOARD_SIZE) if
                       self.board[x][y] == self.EMPTY]
        return random.choice(empty_cells) if empty_cells else None

    def adjust_search_depth(self, board):
        """  动态调整搜索深度 """
        empty_cells = sum(cell == self.EMPTY for row in board for cell in row)
        if empty_cells > (self.BOARD_SIZE ** 2) / 2:
            return 3  # 较浅的搜索深度
        elif empty_cells > 10:
            return 4  # 中等搜索深度
        else:
            return 6  # 深度搜索

    def simulate_move(self, move, depth, board, is_maximizing_player):
        """ 模拟一次移动并返回其计算值 """
        """ 为每个走法创建棋盘的副本，并在该副本上执行一次极小极大搜索以评估该走法。这种方法使得每个走法都能独立地在不同的线程上进行评估 """
        board_copy = np.copy(board)
        board_copy[move[0]][move[1]] = self.PLAYER_PIECE if is_maximizing_player else self.OPPONENT_PIECE

        # 执行一次完整的极小极大搜索，评估这一走法
        _, eval_ = self.minimax_alpha_beta(board_copy, depth, float('-inf'), float('inf'), not is_maximizing_player)
        return eval_
