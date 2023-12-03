# coding=utf-8
"""
    @project: GomokuCode
    @Author：念卿 刘
    @file： GameWindow.py
    @date：2023/11/12 21:42
    
"""
from PySide6.QtCore import QPropertyAnimation, QRect
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtWidgets import QMainWindow, QApplication, QStackedWidget

from CODE.interface.GamePlayWindow import GamePlayWindow
from CODE.interface.GameSettings import GameSettings
from CODE.widgets.MainWidget import MainWidget


class GameWindow(QMainWindow):
    """    主界面    """

    def __init__(self):
        super().__init__()
        self.board_size = 15  # 棋盘大小
        self.cell_size = 40  # 单个棋格大小
        self.play1 = "None"
        self.play2 = "None"
        self.save_log = True  # 是否开启保存日志
        self.play_mode = 0  # 0 人 人 对战  1 人 电脑 对战 2 电脑 人 对战 3 电脑 电脑 对战
        self.win_width, self.win_height = 250, 250
        self.font = QFont("Arial", 16)  # 设置字体为Arial，大小为16
        self.init_ui()

    def init_ui(self):
        """ 构建主窗口的UI元素和布局。 """
        self.setWindowTitle("五子棋")  # 窗口标题
        self.center_window()  # 在屏幕中间显示主界面
        self.stacked_widget = QStackedWidget(self)
        self.main_widget = MainWidget(self)
        self.settings_window = GameSettings(self)
        self.game_play_window = GamePlayWindow(self)

        self.stacked_widget.addWidget(self.main_widget)
        self.stacked_widget.addWidget(self.settings_window)
        self.stacked_widget.addWidget(self.game_play_window)
        self.setCentralWidget(self.stacked_widget)

        self.setWindowIcon(QIcon('imag/icon.jpg'))  # 设置窗口图标
        self.set_background_image('imag/background.jpg')  # 设置背景图片

        self.main_widget.start_game_button.clicked.connect(self.switch_to_game_play)  # 主界面切换到游戏页面
        self.main_widget.settings_button.clicked.connect(self.switch_to_setting)  # 主界面切换到设置界面
        self.main_widget.exit_button.clicked.connect(self.close)  # 关闭界面
        self.game_play_window.return_button.clicked.connect(self.switch_to_main)  # 游戏界面切换到主界面
        self.settings_window.back_button.clicked.connect(self.switch_to_main)  # 设置界面切换到主界面
        self.settings_window.spinBox.valueChanged.connect(self.spinbox_value_changed)  # 修改棋盘大小
        self.settings_window.combo_box_1.currentTextChanged.connect(lambda value: self.change_player(value, 1))  # 修改玩家一
        self.settings_window.combo_box_2.currentTextChanged.connect(lambda value: self.change_player(value, 2))  # 修改玩家二
        self.settings_window.log_radio_group.buttonClicked.connect(self.log_set_change)  # 修改是否保存日志

        self.animation = QPropertyAnimation(self, b"geometry")

    def closeEvent(self, event):
        """ 关闭窗口 """
        # 步骤2：在关闭事件中释放资源，例如关闭文件或数据库连接
        # ...

        # 步骤3：删除窗口对象
        current_index = self.stacked_widget.currentIndex()
        if current_index == 0:
            self.deleteLater()
            super().closeEvent(event)  # 直接关闭程序
        else:
            event.ignore()  # 忽略关闭时间
            self.switch_to_main()  # 切换到主窗口

    def animate_window_size(self, target_size: QRect):
        """
        以动画效果调整窗口的尺寸。
        :param target_size: 动画结束时窗口的尺寸。
        """
        current_geometry = self.frameGeometry()
        if current_geometry.width() * current_geometry.height() <= target_size.width() * target_size.height():
            centerPoint = current_geometry.center()
            target_size.moveCenter(centerPoint)
            self.animation.setDuration(500)
            self.animation.setStartValue(current_geometry)
            self.animation.setEndValue(target_size)
            self.animation.start()
        else:
            new_x = round(current_geometry.center().x() - target_size.width() / 2, 0)
            new_y = round(current_geometry.center().y() - 30 - target_size.height() / 2, 0)
            new_geometry = QRect(new_x, new_y, target_size.width(), target_size.height())
            self.animation.setDuration(500)
            self.animation.setStartValue(current_geometry)
            self.animation.setEndValue(new_geometry)
            self.animation.start()

    def switch_to_main(self):
        """ 切换到主窗口并缩小动画。 """
        self.setWindowTitle("五子棋")
        if self.stacked_widget.currentIndex() - 1:
            self.animate_window_size(QRect(0, 0, self.win_width, self.win_height))
        self.stacked_widget.setCurrentWidget(self.main_widget)

    def switch_to_setting(self):
        """ 切换到子窗口并展开动画。 """
        self.setWindowTitle("游戏设置")
        # self.animate_window_size(QRect(0, 0, self.win_width, self.win_height))
        self.stacked_widget.setCurrentWidget(self.settings_window)

    def switch_to_game_play(self):
        """ 切换到子窗口并展开动画。 """
        self.setWindowTitle("游戏界面")
        window_width = self.cell_size * self.board_size + 168 + 120
        window_height = self.cell_size * self.board_size + 50
        self.animate_window_size(QRect(0, 0, window_width, window_height))
        self.stacked_widget.setCurrentWidget(self.game_play_window)

    def spinbox_value_changed(self, value):
        """更新棋盘大小"""
        self.board_size = value

    def change_play_mode(self):
        """ 修改游戏模式 0 人 人 对战  1 人 电脑 对战 2 电脑 人 对战 3 电脑 电脑 对战 """
        if self.play1 == "None" and self.play2 != "None":
            self.play_mode = 1
        elif self.play1 != "None" and self.play2 == "None":
            self.play_mode = 2
        elif self.play1 != "None" and self.play2 != "None":
            self.play_mode = 3
        else:
            self.play_mode = 0

    def change_player(self, value, user):
        """ 修改玩家 """
        if user - 1:  # 修改玩家一
            self.play2 = value
        else:  # 修改玩家二
            self.play1 = value
        self.change_play_mode()  # 修改游戏模式

    def log_set_change(self):
        """ 修改保存日志设置 """
        self.save_log = bool(self.settings_window.log_radio_group.checkedId())

    def set_background_image(self, image_path):
        """# 设置背景图片"""
        background = QPixmap(image_path)
        palette = self.palette()
        palette.setBrush(self.backgroundRole(), background)
        self.setPalette(palette)

    def center_window(self):
        """# 获取屏幕尺寸和窗口尺寸"""
        screen = QApplication.primaryScreen().geometry()
        # 计算窗口居中的新位置
        new_left = (screen.width() - self.win_width) / 2
        new_top = (screen.height() - self.win_height) / 2
        self.setGeometry(QRect(new_left, new_top, self.win_width, self.win_height))
