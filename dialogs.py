from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

class PurchaseDialog(QDialog):
    def __init__(self, parent, description, price, affordable, on_confirm):
        super().__init__(parent)
        self.setWindowTitle("Підтвердження покупки")
        self.setFixedSize(300, 300)
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
