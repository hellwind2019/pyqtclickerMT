import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QPropertyAnimation, QPoint, QEasingCurve, Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QIcon, QFontDatabase


class ClickerGame(QWidget):
    def __init__(self):
        super().__init__()

        with open("style.css", "r") as f:
            self.setStyleSheet(f.read())
        self.clicks = 0
        self.multiplier = 1
        self.multiplier_price = 10

        self.setWindowTitle("PyQt5 Clicker")
        self.setFixedSize(400, 600)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addLayout(self.init_header_layout())

        self.layout.addStretch(4)

        self.pressButton = QPushButton("Click me!")
        self.pressButton.setObjectName("press_button")
        self.pressButton.clicked.connect(self.add_click)
        self.layout.addWidget(self.pressButton)


        self.setLayout(self.layout)

    def init_header_layout(self):
        layout = QHBoxLayout()

        self.score_label = QLabel("Score: 0")
        self.score_label.setFixedWidth(130)
        self.score_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.score_label)

        self.multiplier_label = QLabel("1x")
        layout.addWidget(self.multiplier_label)

        layout.addStretch(1)

        self.shop_button = QPushButton(f"Shop ({self.multiplier_price})")
        self.shop_button.setObjectName("shop_button")
        self.shop_button.clicked.connect(self.buy_mult)
        layout.addWidget(self.shop_button)
        return layout
    def add_click(self):
        self.clicks += 1 * self.multiplier
        self.score_label.setText(f"Score: {self.clicks}")
    def buy_mult(self):
        if self.clicks > self.multiplier_price:
            self.clicks -= self.multiplier_price
            self.multiplier += 1
            self.multiplier_price = self.multiplier_price* random.randint(2, 4)
            self.multiplier_label.setText(f"{self.multiplier}x")
            self.shop_button.setText(f"Shop ({self.multiplier_price})")
            self.score_label.setText(f"Score: {self.clicks}")

app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("CalSans-Regular.ttf")
font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

# Set the app's default font
app.setFont(QFont(font_family, 20))
window = ClickerGame()
window.show()
sys.exit(app.exec_())
