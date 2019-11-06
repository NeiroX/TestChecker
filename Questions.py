from PyQt5.QtWidgets import QWidget
from PyQt5 import uic

from Options import JSONFile


class Questions(QWidget):
    def __init__(self):
        super().__init__()
        self.file = JSONFile()
        self.numberOfQuestions = 0
        self.lenOfTest = len(self.file)

    def loadUI(self):
        uic.loadUi('QuestionsUI.ui')
        if self.lenOfTest == 0:
            pass
        elif self.lenOfTest == 1:
            pass
        else:
            pass
            self.nextQuestion.clicked.connect(self.nextQuestion)

    def nextQuestion(self):
        if self.numberOfQuestions == self.lenOfTest - 1:
            pass
        elif self.numberOfQuestions > 0:
            pass
        elif self.lenOfTest == self.lenOfTest - 2:
            pass
