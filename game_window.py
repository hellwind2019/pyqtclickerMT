from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize
from PyQt5.QtGui import QIcon

from constants import *
from dialogs import PurchaseDialog
from planets import Planet

class ClickerGame(QWidget):
    def __init__(self):
        super().__init__()

        self.clicks = 0
        self.multiplier = 1
        self.multiplier_price = 10
        self.planet = Planet.MERCURY

        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        with open(STYLE_FILE, "r") as f:
            self.setStyleSheet(f.read())

        self.init_ui()

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

        self.leaderboard_button = QPushButton("Leaderboard")
        self.leaderboard_button.setObjectName("leaderboard_button")
        self.leaderboard_button.clicked.connect(self.open_leaderboard)

        for widget in (self.score_label, self.multiplier_label, self.score_per_second_label, self.leaderboard_button):
            layout.addWidget(widget)
        return layout

    def build_main(self):
        layout = QVBoxLayout()
        self.click_button = QPushButton()
        self.click_button.setIcon(QIcon(EARTH_IMAGE))
        self.click_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.click_button.setIconSize(QSize(300, 300))
        self.click_button.clicked.connect(lambda: self.animate_button(self.click_button))
        self.click_button.clicked.connect(self.add_click)
        layout.addWidget(self.click_button)
        return layout

    def build_footer(self):
        layout = QHBoxLayout()
        self.mult_button = QPushButton("Mult")
        self.boost_button = QPushButton("Boost")
        self.auto_button = QPushButton("Auto")

        for button in (self.mult_button, self.boost_button, self.auto_button):
            layout.addWidget(button)

        return layout

    def add_click(self):
        self.clicks += 1 * self.multiplier
        self.update_ui()

    def update_ui(self):
        self.score_label.setText(f"Score: {self.clicks}")
        self.multiplier_label.setText(f"{self.multiplier}x")
        self.leaderboard_button.setText(f"Shop ({self.multiplier_price})")

    def open_leaderboard(self):
        PurchaseDialog(self, "Description", 1000, lambda: print("Upgrade")).exec_()

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
