# coding=utf-8
"""
    @project: GomokuCode
    @Author：念卿 刘
    @file： a2.py
    @date：2023/11/16 23:00
    
"""
from itertools import chain

import numpy as np


class AI:
    """
    电脑类
    """

    def __init__(self):
        self.array_status = None
        self.FREE = None
        self.ROBOT = None
        self.USER = None
        self.ChessType = []  # 棋盘类型
        self.ChessWightDict = {}  # 棋型对应的权值
        self.sumScore = {}  # 每个空位置的总得分,初始化为0
        self.linkNum = 4  # 连棋数量，从4开始，7结束
        self.init_chess_typ_and_chess_wight()

    def start(self, list_board_status_array, player, index):
        """ 开始 """
        self.array_status = list_board_status_array
        self.FREE = 0
        self.ROBOT = 3 - player
        self.USER = player
        self.sumScore = {}  # 每个空位置的总得分,初始化为0
        self.compute()
        return self.compare(self.sumScore, index)

    def init_chess_typ_and_chess_wight(self):
        """
        初始化棋盘类型、初始化棋型对应的权值
        """
        FREE, USER, ROBOT = self.FREE, self.USER, self.ROBOT
        # 黑棋棋型
        # 连五：ooooo
        R_L5 = [ROBOT, ROBOT, ROBOT, ROBOT, ROBOT]

        # 活四：?oooo?
        R_L4 = [FREE, ROBOT, ROBOT, ROBOT, ROBOT, FREE]

        # 冲四：?oooox  o?ooo  oo?oo
        R_S41 = [FREE, ROBOT, ROBOT, ROBOT, ROBOT, USER]
        R_S42 = [ROBOT, FREE, ROBOT, ROBOT, ROBOT]
        R_S43 = [ROBOT, ROBOT, FREE, ROBOT, ROBOT]

        # 活三：?ooo?   o?oo
        R_L31 = [FREE, ROBOT, ROBOT, ROBOT, FREE]
        R_L32 = [ROBOT, FREE, ROBOT, ROBOT]

        # 眠三：??ooox  ?o?oox  ?oo?ox o??oo o?o?o x?ooo?x
        R_S31 = [FREE, FREE, ROBOT, ROBOT, ROBOT, USER]
        R_S32 = [FREE, ROBOT, FREE, ROBOT, ROBOT, USER]
        R_S33 = [FREE, ROBOT, ROBOT, FREE, ROBOT, USER]
        R_S34 = [ROBOT, FREE, FREE, ROBOT, ROBOT]
        R_S35 = [ROBOT, FREE, ROBOT, FREE, ROBOT]
        R_S36 = [USER, FREE, ROBOT, ROBOT, ROBOT, FREE, USER]

        # 活二：??oo??  ?o?o?  o??o
        R_L21 = [FREE, FREE, ROBOT, ROBOT, FREE, FREE]
        R_L22 = [FREE, ROBOT, FREE, ROBOT, FREE]
        R_L23 = [ROBOT, FREE, FREE, ROBOT]

        # 眠二：???oox  ??o?ox ?o??ox o???o
        R_S21 = [FREE, FREE, FREE, ROBOT, ROBOT, USER]
        R_S22 = [FREE, FREE, ROBOT, FREE, ROBOT, USER]
        R_S23 = [FREE, ROBOT, FREE, FREE, ROBOT, USER]
        R_S24 = [ROBOT, FREE, FREE, FREE, ROBOT]

        # 白棋棋型
        # 连五：ooooo
        U_L5 = [USER, USER, USER, USER, USER]

        # 活四：?oooo?
        U_L4 = [FREE, USER, USER, USER, USER, FREE]

        # 冲四：?oooox  o?ooo  oo?oo
        U_S41 = [FREE, USER, USER, USER, USER, ROBOT]
        U_S42 = [USER, FREE, USER, USER, USER]
        U_S43 = [USER, USER, FREE, USER, USER]

        # 活三：?ooo?   o?oo
        U_L31 = [FREE, USER, USER, USER, FREE]
        U_L32 = [USER, FREE, USER, USER]

        # 眠三：??ooox  ?o?oox  ?oo?ox o??oo o?o?o x?ooo?x
        U_S31 = [FREE, FREE, USER, USER, USER, ROBOT]
        U_S32 = [FREE, USER, FREE, USER, USER, ROBOT]
        U_S33 = [FREE, USER, USER, FREE, USER, ROBOT]
        U_S34 = [USER, FREE, FREE, USER, USER]
        U_S35 = [USER, FREE, USER, FREE, USER]
        U_S36 = [ROBOT, FREE, USER, USER, USER, FREE, ROBOT]

        # 活二：??oo??  ?o?o?  o??o
        U_L21 = [FREE, FREE, USER, USER, FREE, FREE]
        U_L22 = [FREE, USER, FREE, USER, FREE]
        U_L23 = [USER, FREE, FREE, USER]

        # 眠二：???oox  ??o?ox ?o??ox o???o
        U_S21 = [FREE, FREE, FREE, USER, USER, ROBOT]
        U_S22 = [FREE, FREE, USER, FREE, USER, ROBOT]
        U_S23 = [FREE, USER, FREE, FREE, USER, ROBOT]
        U_S24 = [USER, FREE, FREE, FREE, USER]
        # 黑棋
        self.ChessType.append(R_L5)
        self.ChessType.append(R_L4)
        self.ChessType.append(R_S41)
        self.ChessType.append(R_S42)
        self.ChessType.append(R_S43)
        self.ChessType.append(R_L31)
        self.ChessType.append(R_L32)
        self.ChessType.append(R_S31)
        self.ChessType.append(R_S32)
        self.ChessType.append(R_S33)
        self.ChessType.append(R_S34)
        self.ChessType.append(R_S35)
        self.ChessType.append(R_S36)
        self.ChessType.append(R_L21)
        self.ChessType.append(R_L22)
        self.ChessType.append(R_L23)
        self.ChessType.append(R_S21)
        self.ChessType.append(R_S22)
        self.ChessType.append(R_S23)
        self.ChessType.append(R_S24)
        # 白棋
        self.ChessType.append(U_L5)
        self.ChessType.append(U_L4)
        self.ChessType.append(U_S41)
        self.ChessType.append(U_S42)
        self.ChessType.append(U_S43)
        self.ChessType.append(U_L31)
        self.ChessType.append(U_L32)
        self.ChessType.append(U_S31)
        self.ChessType.append(U_S32)
        self.ChessType.append(U_S33)
        self.ChessType.append(U_S34)
        self.ChessType.append(U_S35)
        self.ChessType.append(U_S36)
        self.ChessType.append(U_L21)
        self.ChessType.append(U_L22)
        self.ChessType.append(U_L23)
        self.ChessType.append(U_S21)
        self.ChessType.append(U_S22)
        self.ChessType.append(U_S23)
        self.ChessType.append(U_S24)

        r_scoreLow2 = 20  # 眠二权值
        r_scoreHigh2 = 40  # 活二权值
        r_scoreLow3 = 60  # 眠三权值
        r_scoreHigh3 = 80  # 活三权值
        r_scoreLow4 = 100  # 冲四权值
        r_scoreHigh4 = 120  # 活四权值
        r_scoreHigh5 = 140  # 完成权值

        u_scoreLow2 = 10  # 眠二权值
        u_scoreHigh2 = 30  # 活二权值
        u_scoreLow3 = 50  # 眠三权值
        u_scoreHigh3 = 70  # 活三权值
        u_scoreLow4 = 90  # 冲四权值
        u_scoreHigh4 = 110  # 活四权值
        u_scoreHigh5 = 130  # 完成权值
        # 黑棋
        self.ChessWightDict[str(R_L5)] = r_scoreHigh5
        self.ChessWightDict[str(R_L4)] = r_scoreHigh4
        self.ChessWightDict[str(R_S41)] = r_scoreLow4
        self.ChessWightDict[str(R_S42)] = r_scoreLow4
        self.ChessWightDict[str(R_S43)] = r_scoreLow4
        self.ChessWightDict[str(R_L31)] = r_scoreHigh3
        self.ChessWightDict[str(R_L32)] = r_scoreHigh3
        self.ChessWightDict[str(R_S31)] = r_scoreLow3
        self.ChessWightDict[str(R_S32)] = r_scoreLow3
        self.ChessWightDict[str(R_S33)] = r_scoreLow3
        self.ChessWightDict[str(R_S34)] = r_scoreLow3
        self.ChessWightDict[str(R_S35)] = r_scoreLow3
        self.ChessWightDict[str(R_S36)] = r_scoreLow3
        self.ChessWightDict[str(R_L21)] = r_scoreHigh2
        self.ChessWightDict[str(R_L22)] = r_scoreHigh2
        self.ChessWightDict[str(R_L23)] = r_scoreHigh2
        self.ChessWightDict[str(R_S21)] = r_scoreLow2
        self.ChessWightDict[str(R_S22)] = r_scoreLow2
        self.ChessWightDict[str(R_S23)] = r_scoreLow2
        self.ChessWightDict[str(R_S24)] = r_scoreLow2
        # 白棋
        self.ChessWightDict[str(U_L5)] = u_scoreHigh5
        self.ChessWightDict[str(U_L4)] = u_scoreHigh4
        self.ChessWightDict[str(U_S41)] = u_scoreLow4
        self.ChessWightDict[str(U_S42)] = u_scoreLow4
        self.ChessWightDict[str(U_S43)] = u_scoreLow4
        self.ChessWightDict[str(U_L31)] = u_scoreHigh3
        self.ChessWightDict[str(U_L32)] = u_scoreHigh3
        self.ChessWightDict[str(U_S31)] = u_scoreLow3
        self.ChessWightDict[str(U_S32)] = u_scoreLow3
        self.ChessWightDict[str(U_S33)] = u_scoreLow3
        self.ChessWightDict[str(U_S34)] = u_scoreLow3
        self.ChessWightDict[str(U_S35)] = u_scoreLow3
        self.ChessWightDict[str(U_S36)] = u_scoreLow3
        self.ChessWightDict[str(U_L21)] = u_scoreHigh2
        self.ChessWightDict[str(U_L22)] = u_scoreHigh2
        self.ChessWightDict[str(U_L23)] = u_scoreHigh2
        self.ChessWightDict[str(U_S21)] = u_scoreLow2
        self.ChessWightDict[str(U_S22)] = u_scoreLow2
        self.ChessWightDict[str(U_S23)] = u_scoreLow2
        self.ChessWightDict[str(U_S24)] = u_scoreLow2

    def compare(self, return_ai, ind) -> tuple:
        """
        如果有多个权值相同的点，找出其中里上次下的白棋最近的那个
        """
        if not np.count_nonzero(np.array(self.array_status)):
            return 7, 7
        AI_max_value = return_ai[max(return_ai, key=return_ai.get)]
        min_dis = 1000
        (rex, rey) = (0, 0)
        for key, val in return_ai.items():
            if val == AI_max_value:
                AI_str = key
                AI_array = AI_str.split(',')
                str1 = AI_array[0].strip('(')
                str2 = AI_array[1].strip(')').strip(' ')
                x = int(str1)
                y = int(str2)
                if pow(ind[0] - x, 2) + pow(ind[1] - y, 2) < min_dis:
                    min_dis = pow(ind[0] - x, 2) + pow(ind[1] - y, 2)
                    (rex, rey) = (x, y)
        return rex, rey

    @staticmethod
    def to_list_format(format_list):
        """
        二维列表转一维列表
        """
        res = list(chain(*format_list.tolist()))
        return res

    def compute_row(self, row, col):
        """
        # 横
        """
        for i_ in range(0, 15 - self.linkNum):
            if col in range(i_, i_ + self.linkNum):
                typeList = self.to_list_format(self.array_status[row:row + 1, i_:i_ + self.linkNum])
                typeList[col - i_] = self.ROBOT  # 将空白位置换成黑棋，寻找棋型
                try:
                    self.ChessType.index(typeList)  # 有该棋型
                    try:
                        self.sumScore[str((row, col))] = max(self.ChessWightDict[str(typeList)],
                                                             self.sumScore[str((row, col))])  # 记录该坐标的权重
                    except KeyError:
                        self.sumScore[str((row, col))] = self.ChessWightDict[str(typeList)]  # 记录该坐标的权
                except ValueError or KeyError:  # 没有该棋型， 将权重置为typeList中的黑棋和白棋较多的棋数
                    typeList[col - i_] = self.USER  # 将空白位置换成白棋，寻找棋型
                    try:
                        self.ChessType.index(typeList)  # 有该棋型
                        try:
                            self.sumScore[str((row, col))] = max(self.ChessWightDict[str(typeList)],
                                                                 self.sumScore[str((row, col))])  # 记录该坐标的权重
                        except KeyError:
                            self.sumScore[str((row, col))] = self.ChessWightDict[str(typeList)]  # 记录该坐标的权
                    except ValueError or KeyError:  # 没有该棋型， 将权重置为typeList中的黑棋和白棋较多的棋数
                        try:
                            self.sumScore[str((row, col))] = max(typeList.count(self.ROBOT),
                                                                 typeList.count(self.USER),
                                                                 self.sumScore[str((row, col))])
                        except KeyError:
                            self.sumScore[str((row, col))] = max(typeList.count(self.ROBOT),
                                                                 typeList.count(self.USER))
            else:
                pass

    def compute_col(self, row, col):
        """
                    # 竖
        """
        for i_ in range(0, 15 - self.linkNum):
            if row in range(i_, i_ + self.linkNum):
                typeList = self.to_list_format(self.array_status[i_:i_ + self.linkNum, col:col + 1])
                typeList[row - i_] = self.ROBOT  # 将空白位置换成黑棋，寻找棋型
                try:
                    # ChessType.index(typeList)  # 有该棋型
                    try:
                        self.sumScore[str((row, col))] = max(self.ChessWightDict[str(typeList)],
                                                             self.sumScore[str((row, col))])  # 记录该坐标的权重
                    except KeyError:
                        self.sumScore[str((row, col))] = self.ChessWightDict[str(typeList)]  # 记录该坐标的权
                except KeyError:  # 没有该棋型， 将权重置为typeList中的黑棋和白棋较多的棋数
                    typeList[row - i_] = self.USER  # 将空白位置换成白棋，寻找棋型
                    try:
                        # ChessType.index(typeList)  # 有该棋型
                        try:
                            self.sumScore[str((row, col))] = max(self.ChessWightDict[str(typeList)],
                                                                 self.sumScore[str((row, col))])  # 记录该坐标的权重
                        except KeyError:
                            self.sumScore[str((row, col))] = self.ChessWightDict[str(typeList)]  # 记录该坐标的权
                    except KeyError:  # 没有该棋型， 将权重置为typeList中的黑棋和白棋较多的棋数
                        try:
                            self.sumScore[str((row, col))] = max(typeList.count(self.ROBOT),
                                                                 typeList.count(self.USER),
                                                                 self.sumScore[str((row, col))])
                        except KeyError:
                            self.sumScore[str((row, col))] = max(typeList.count(self.ROBOT),
                                                                 typeList.count(self.USER))
            else:
                pass

    def compute_oblique_l(self, row, col):
        """
                    # 左斜 左下对角(10<=row<=14  0<=col<=4)  右上对角(0<=row<=4  10<=col<=14)
        """
        for i_ in range(0, 15 - self.linkNum):
            for m in range(0, 15 - self.linkNum):
                # 斜率相同，即在同一条线上，且在选的范围内
                if (row - i_) == (col - m) and row in range(i_, i_ + self.linkNum) and range(m, m + self.linkNum):
                    typeList = []
                    for k in range(self.linkNum):
                        typeList.append(self.array_status[i_ + k][m + k])
                    typeList[row - i_] = self.ROBOT  # 将空白位置换成黑棋，寻找棋型
                    try:
                        self.ChessType.index(typeList)  # 有该棋型
                        try:
                            self.sumScore[str((row, col))] = max(self.ChessWightDict[str(typeList)],
                                                                 self.sumScore[str((row, col))])  # 记录该坐标的权重
                        except KeyError:
                            self.sumScore[str((row, col))] = self.ChessWightDict[str(typeList)]  # 记录该坐标的权
                    except ValueError:  # 没有该棋型， 将权重置为typeList中的黑棋和白棋较多的棋数
                        typeList[row - i_] = self.USER  # 将空白位置换成白棋，寻找棋型
                        try:
                            self.ChessType.index(typeList)  # 有该棋型
                            try:
                                self.sumScore[str((row, col))] = max(self.ChessWightDict[str(typeList)],
                                                                     self.sumScore[str((row, col))])  # 记录该坐标的权重
                            except KeyError:
                                self.sumScore[str((row, col))] = self.ChessWightDict[str(typeList)]  # 记录该坐标的权
                        except ValueError:  # 没有该棋型， 将权重置为typeList中的黑棋和白棋较多的棋数
                            try:
                                self.sumScore[str((row, col))] = max(typeList.count(self.ROBOT),
                                                                     typeList.count(self.USER),
                                                                     self.sumScore[str((row, col))])
                            except KeyError:
                                self.sumScore[str((row, col))] = max(typeList.count(self.ROBOT),
                                                                     typeList.count(self.USER))
                else:
                    pass

    def compute_oblique_r(self, row, col):
        """
                    # 右斜
        """
        for i_ in range(0, 15 - self.linkNum):
            for m in range(self.linkNum, 15):
                # 斜率相同，即在同一条线上，且在选的范围内
                if (row - i_) == -(col - m) and row in range(i_, i_ + self.linkNum) and range(m - self.linkNum, m):
                    typeList = []
                    for k in range(self.linkNum):
                        typeList.append(self.array_status[i_ + k][m - k])
                    typeList[row - i_] = self.ROBOT  # 将空白位置换成黑棋，寻找棋型
                    try:
                        self.ChessType.index(typeList)  # 有该棋型
                        try:
                            self.sumScore[str((row, col))] = max(self.ChessWightDict[str(typeList)],
                                                                 self.sumScore[str((row, col))])  # 记录该坐标的权重
                        except KeyError:
                            self.sumScore[str((row, col))] = self.ChessWightDict[str(typeList)]  # 记录该坐标的权
                    except ValueError:  # 没有该棋型， 将权重置为typeList中的黑棋和白棋较多的棋数
                        typeList[row - i_] = self.USER  # 将空白位置换成白棋，寻找棋型
                        try:
                            self.ChessType.index(typeList)  # 有该棋型
                            try:
                                self.sumScore[str((row, col))] = max(self.ChessWightDict[str(typeList)],
                                                                     self.sumScore[str((row, col))])  # 记录该坐标的权重
                            except KeyError:
                                self.sumScore[str((row, col))] = self.ChessWightDict[str(typeList)]  # 记录该坐标的权
                        except ValueError:  # 没有该棋型， 将权重置为typeList中的黑棋和白棋较多的棋数
                            try:
                                self.sumScore[str((row, col))] = max(typeList.count(self.ROBOT),
                                                                     typeList.count(self.USER),
                                                                     self.sumScore[str((row, col))])
                            except KeyError:
                                self.sumScore[str((row, col))] = max(typeList.count(self.ROBOT),
                                                                     typeList.count(self.USER))
                else:
                    pass

    def compute(self):
        """
        电脑
        """
        for row in range(15):
            for col in range(15):
                if self.array_status[row][col] == self.FREE:  # 计算空位置的最大（横 列 左斜 右斜）权值
                    # 4 棋子
                    self.compute_row(row, col)
                    self.compute_col(row, col)
                    self.compute_oblique_l(row, col)
                    self.compute_oblique_r(row, col)
                    # 5 棋子
                    self.linkNum = 5
                    self.compute_row(row, col)
                    self.compute_col(row, col)
                    self.compute_oblique_l(row, col)
                    self.compute_oblique_r(row, col)
                    # 6 棋子
                    self.linkNum = 6
                    self.compute_row(row, col)
                    self.compute_col(row, col)
                    self.compute_oblique_l(row, col)
                    self.compute_oblique_r(row, col)
                    # 7 棋子
                    self.linkNum = 7
                    self.compute_row(row, col)
                    self.compute_col(row, col)
                    self.compute_oblique_l(row, col)
                    self.compute_oblique_r(row, col)
                    # 回到原状态
                    self.linkNum = 4
                else:
                    pass
