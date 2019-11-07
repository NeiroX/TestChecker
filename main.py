from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import sys

from Results import Results
from Questions import Questions


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.loadUI()

    def loadUI(self):
        uic.loadUi('UIs/MenuUI.ui', self)
        self.startButton.clicked.connect(self.start)
        self.resultButton.clicked.connect(self.results)
        self.exitButton.clicked.connect(self.exit)

    def start(self):
        self.questions = Questions(self, 'test')

    def results(self):
        self.results = Results()

    def exit(self):
        sys.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
