from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QDialog
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QTimer
from PyQt5.QtGui import QIcon

from game_logic import GameLogic
from constants import *
from dialogs import PurchaseDialog, RegistrationDialog, LoginDialog
from planets import Planet

class ClickerGame(QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.click_button = None
        self.leaderboard_button = None
        self.score_per_second_label = None
        self.layout = None
        self.multiplier_label = None
        self.auto_click_timer = None
        self.score_label = None
        self.logic = GameLogic()
        self.window_width = width
        self.window_height = height
        self.current_username = None
        self.username_label = None
        self.login_button = None

        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(self.window_width, self.window_height)

        with open(STYLE_FILE, "r") as f:
            self.setStyleSheet(f.read())

        self.init_ui()
        self.init_timer()

        self.boost_timer = QTimer()
        self.boost_timer.setSingleShot(True)
        self.boost_timer.timeout.connect(self.remove_boost)

    def init_timer(self):
        self.auto_click_timer = QTimer()
        self.auto_click_timer.timeout.connect(self.on_auto_click)
        self.auto_click_timer.start(1000)

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        self.layout.addLayout(self.build_header())
        self.layout.addLayout(self.build_main())
        self.layout.addLayout(self.build_footer())

    def build_header(self):
        layout = QHBoxLayout()
        self.score_label = self.create_label("Score: 0", 130)
        self.multiplier_label = self.create_label("1x")
        self.score_per_second_label = self.create_label("1/s")

        self.login_button = QPushButton("Log In")
        self.login_button.clicked.connect(self.open_login)


        # Create username label (initially hidden)
        self.username_label = QLabel()
        self.username_label.hide()


        for widget in (self.score_label, self.multiplier_label,
                           self.score_per_second_label, self.leaderboard_button,
                           self.login_button, self.username_label):
                layout.addWidget(widget)
        return layout


    def open_login(self):
        dialog = LoginDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Get the username from the dialog
            if hasattr(dialog, 'logged_in_username'):
                self.current_username = dialog.logged_in_username
                self.update_login_state()

    def update_login_state(self):
        if self.current_username:
            # Hide login button and show username
            self.login_button.hide()
            self.username_label.setText(f"Welcome, {self.current_username}!")
            self.username_label.show()
        else:
            # Show login button and hide username
            self.login_button.show()
            self.username_label.hide()

    def build_main(self):
        layout = QVBoxLayout()
        self.click_button = QPushButton()
        self.click_button.setIcon(QIcon(EARTH_IMAGE))
        self.click_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.click_button.setIconSize(QSize(300, 300))
        self.click_button.clicked.connect(lambda: self.animate_button(self.click_button))
        self.click_button.clicked.connect(self.on_click)
        layout.addWidget(self.click_button)
        return layout

    def build_footer(self):
        layout = QHBoxLayout()
        self.mult_button = QPushButton("Mult")
        self.boost_button = QPushButton("Boost")
        self.auto_button = QPushButton("Auto")

        self.mult_button.clicked.connect(self.on_buy_multiplier)
        self.boost_button.clicked.connect(self.on_boost)
        self.auto_button.clicked.connect(self.on_auto)

        for button in (self.mult_button, self.boost_button, self.auto_button):
            layout.addWidget(button)
        return layout

    def on_click(self):
        self.logic.add_click()
        self.update_ui()

    def on_auto_click(self):
        self.logic.auto_click()
        self.update_ui()

    def on_buy_multiplier(self):
        self.buy_upgrade(
            f"Gain more score per click\n {self.logic.multiplier} → {self.logic.multiplier + 1}",
            self.logic.multiplier_price,
            self.logic.buy_multiplier
        )

    def on_boost(self):
        # if self.logic.buy_boost_upgrade():
        #     self.update_ui()
        # else:
        #     if not self.logic.boost_active:
        #         self.logic.activate_boost()
        #         self.boost_timer.start(5000)
        #         self.update_ui()
        self.buy_upgrade(
            f"Activate Boost ({self.logic.boost_multiplier}x for 5s)\nNext boost +5x",
            self.logic.boost_price,
            self.buy_and_activate_boost
        )

    def buy_and_activate_boost(self):
        if self.logic.buy_boost_upgrade():
            self.logic.activate_boost()
            QTimer.singleShot(5000, self.logic.deactivate_boost)
            return True
        return False
    def remove_boost(self):
        self.logic.boost_active = False
        self.update_ui()

    def on_auto(self):
        # TODO: Implement autoclick upgrade
        ...

    def buy_upgrade(self, description: str, price: int, upgrade_func: callable):
        def confirm_purchase():
            if upgrade_func():
                self.update_ui()

        PurchaseDialog(self, description, price, self.logic.is_affordable(price), confirm_purchase, self.window_width, self.window_height).exec_()

    def update_ui(self):
        self.score_label.setText(f"Score: {self.logic.clicks}")
        if self.logic.boost_active:
            self.multiplier_label.setText(f"{self.logic.multiplier}x × {self.logic.boost_multiplier} BOOST!")
        else:
            self.multiplier_label.setText(f"{self.logic.multiplier}x")

    def open_leaderboard(self):
        ...

    @staticmethod
    def animate_button(button):
        anim = QPropertyAnimation(button, b"iconSize")
        anim.setDuration(100)
        anim.setStartValue(QSize(250, 250))
        anim.setKeyValueAt(0.5, QSize(235, 235))
        anim.setEndValue(QSize(250, 250))
        anim.start()
        button.anim = anim

    @staticmethod
    def create_label(text, width=None):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        if width:
            label.setFixedWidth(width)
        return label
