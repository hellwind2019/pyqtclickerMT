from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox, QLineEdit
import requests
class PurchaseDialog(QDialog):
    def __init__(self, parent, description, price, affordable, on_confirm, width, heigth):
        super().__init__(parent)
        self.setWindowTitle("Підтвердження покупки")
        self.setFixedSize(width//2, heigth//2)
        self.setModal(True)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(description))
        layout.addWidget(QLabel(f"Price: {price}"))

        button_layout = QHBoxLayout()
        buy_button = QPushButton("Buy")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(buy_button)
        button_layout.addWidget(cancel_button)

        color : str
        if affordable:
           color = "green"
        else:
            color = "red"
        buy_button.setStyleSheet(f"background-color: {color}; color: white;")


        layout.addLayout(button_layout)
        self.setLayout(layout)

        buy_button.clicked.connect(lambda: (on_confirm(), self.accept()))
        cancel_button.clicked.connect(self.reject)


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Log in")
        self.setModal(True)
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Username field
        username_layout = QHBoxLayout()
        username_label = QLabel("Логін:")
        self.username_input = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)

        # Password field
        password_layout = QHBoxLayout()
        password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        # Buttons
        button_layout = QHBoxLayout()
        login_button = QPushButton("Log In")
        register_button = QPushButton("Sign In")
        cancel_button = QPushButton("Cancel")

        login_button.clicked.connect(self.login)
        register_button.clicked.connect(self.register)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(login_button)
        button_layout.addWidget(register_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Помилка", "Заповніть всі поля!")
            return

        try:
            response = requests.post(
                "http://localhost:8000/register",
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                QMessageBox.information(self, "Успіх", "Реєстрація успішна!")
                self.accept()
            else:
                QMessageBox.warning(
                    self, "Помилка",
                    "Користувач з таким ім'ям вже існує!"
                )

        except requests.RequestException:
            QMessageBox.critical(
                self, "Помилка",
                "Помилка з'єднання з сервером!"
            )
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Fill all fields")
            return

        try:
            response = requests.post(
                "http://localhost:8000/login",
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Login successful")
                self.accept()
            else:
                QMessageBox.warning(
                    self, "Error",
                    "Wrong username or password"
                )

        except requests.RequestException:
            QMessageBox.critical(
                self, "Помилка",
                "Помилка з'єднання з сервером!"
            )



class RegistrationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Реєстрація")
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Username field
        username_layout = QHBoxLayout()
        username_label = QLabel("Логін:")
        self.username_input = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)

        # Password field
        password_layout = QHBoxLayout()
        password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        # Buttons
        button_layout = QHBoxLayout()
        register_button = QPushButton("Зареєструватися")
        cancel_button = QPushButton("Скасувати")

        register_button.clicked.connect(self.register)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(register_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Помилка", "Заповніть всі поля!")
            return

        try:
            response = requests.post(
                "http://localhost:8000/register",
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                QMessageBox.information(self, "Успіх", "Реєстрація успішна!")
                self.accept()
            else:
                QMessageBox.warning(
                    self, "Помилка",
                    "Користувач з таким ім'ям вже існує!"
                )

        except requests.RequestException:
            QMessageBox.critical(
                self, "Помилка",
                "Помилка з'єднання з сервером!"
            )