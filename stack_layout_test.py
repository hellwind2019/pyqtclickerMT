import sys
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import (
    QWidget, QApplication, QStackedWidget, QHBoxLayout, QPushButton,
    QVBoxLayout, QLabel
)


class MultiplePages(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.init_navigation()
        self.init_pages()

    def init_navigation(self):
        # Top label
        self.label = QLabel("Main")
        self.main_layout.addWidget(self.label)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.f_button = QPushButton("First")
        self.s_button = QPushButton("Second")

        nav_layout.addWidget(self.f_button)
        nav_layout.addWidget(self.s_button)
        self.main_layout.addLayout(nav_layout)

        # Connect buttons
        self.f_button.clicked.connect(lambda: self.switch_page(0))
        self.s_button.clicked.connect(lambda: self.switch_page(1))

    def init_pages(self):
        # Stacked widget to hold pages
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        # Create pages
        first_page = self.create_page("First Layout Page")
        second_page = self.create_page("Second Layout Page")

        # Add to stack
        self.stack.addWidget(first_page)
        self.stack.addWidget(second_page)

        # Default page
        self.stack.setCurrentIndex(0)

    def create_page(self, button_text):
        widget = QWidget()
        layout = QVBoxLayout()
        btn = QPushButton(button_text)
        layout.addWidget(btn)
        widget.setLayout(layout)
        return widget

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    font_id = QFontDatabase.addApplicationFont("assets/CalSans-Regular.ttf")
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(font_family, 18))

    window = MultiplePages()
    window.show()

    sys.exit(app.exec_())
