from PyQt5.QtWidgets import QApplication
from game import Game
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())
