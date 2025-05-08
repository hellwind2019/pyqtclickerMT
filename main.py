import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont

from constants import FONT_FILE
from game_window import ClickerGame

def main():
    app = QApplication(sys.argv)
    font_id = QFontDatabase.addApplicationFont(FONT_FILE)
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(font_family, 18))

    window = ClickerGame()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
