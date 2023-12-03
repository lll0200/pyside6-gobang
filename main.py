# coding=utf-8
"""
    @project: GomokuCode
    @Author：念卿 刘
    @file： main.py
    @date：2023/11/12 20:21
    
"""
from CODE.interface.GameWindow import GameWindow
import sys
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = GameWindow()
    mainWin.show()
    sys.exit(app.exec())
