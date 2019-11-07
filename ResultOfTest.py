from PyQt5.QtWidgets import QWidget
from PyQt5 import uic


class ResultOfTest(QWidget):
    def __init__(self, other, true_answers, lenOfTest):
        super().__init__()
        self.true_answers = true_answers
        self.lenOfTest = lenOfTest
        self.loadUI(other)

    def loadUI(self, other):
        uic.loadUi('UIs/ResultUI.ui', other)
        other.resultLabel.setText(f'{self.true_answers}/{self.lenOfTest}')
        resultInPercent = round(self.true_answers / self.lenOfTest * 100)
        other.percentLabel.setText(f'{resultInPercent}%')
        if resultInPercent >= 85:
            other.markLabel.setText('5')
            other.markLabel.setStyleSheet('color: green')
        elif resultInPercent >= 65:
            other.markLabel.setText('4')
            other.markLabel.setStyleSheet('color: blue')
        elif resultInPercent >= 45:
            other.markLabel.setText('3')
            other.markLabel.setStyleSheet('color: yellow')
        else:
            other.markLabel.setText('2')
            other.markLabel.setStyleSheet('color: red')
        other.mainMenuButton.clicked.connect(lambda x: self.mainMenu(other))
        other.viewAnswersButton.clicked.connect(lambda x: self.viewAnswers(other))

    def mainMenu(self, other):
        other.loadUI()

    def viewAnswers(self, other):
        pass
