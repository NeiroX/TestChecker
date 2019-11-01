from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
from PyQt5 import uic
import sys


class QuestionWindow(object):
    def setupUI(self, MainWindow):
        MainWindow.setTitle()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UIs/MenuUI.ui', self)
        self.startButton.clicked.connect(self.start)
        self.exitButton.clicked.connect(self.exit)

    def start(self):
        uic.loadUi('UIs/QuestionsUI.ui', self)

    def exit(self):
        sys.exit(0)


app = QApplication(sys.argv)
ex = Main()
ex.show()
sys.exit(app.exec_())
