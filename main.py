import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont

import constants
# from constants import *
from game_window import ClickerGame

def main():
    app = QApplication(sys.argv)
    font_id = QFontDatabase.addApplicationFont(constants.FONT_FILE)
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(font_family, 18))

    screen = app.primaryScreen()
    size = screen.size()
    window_width = size.width() // 2
    window_height = size.height() // 2

    # constants.WINDOW_WIDTH = window_width
    # constants.WINDOW_HEIGHT = window_height
    # print("window: ", window_width, " - ", window_height)

    window = ClickerGame(window_width, window_height)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
