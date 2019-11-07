from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt5 import uic, QtCore
import sys
from random import shuffle
import threading

from Options import JSONFile
from ResultOfTest import ResultOfTest


class Questions(QMainWindow):
    def __init__(self, other):
        super().__init__()
        self.file = JSONFile()
        self.used = dict()
        self.numberOfQuestions = 0
        self.lenOfTest = len(self.file)
        self.loadUI(other)

    def loadUI(self, other):
        if self.lenOfTest == 0:
            errorMessage = QMessageBox()
            errorMessage.setIcon(QMessageBox.Information)
            errorMessage.setText('Questions are not found')
            return

        self.endTimer = threading.Timer(
            int(self.file.time.split(':')[0]) * 60 + int(self.file.time.split(':')[1]),
            self.continueQuiz)  # Таймер, заканчивающий тест через заданное время
        self.endTimer.start()

        # app1 = QtCore.QCoreApplication(sys.argv)
        # self.labelTimer = QtCore.QTimer()
        # self.time = QtCore.QTime(0, int(self.file.time.split(':')[0]),
        #                          int(self.file.time.split(':')[1]))
        # self.labelTimer.timeout.connect(self.updateTimerLabel)
        # self.labelTimer.start(100)
        # sys.exit(app1.exec_())

        QApplication.processEvents()
        uic.loadUi('UIs/QuestionsUI.ui', other)
        self.radioButtons = [other.firstAnswer, other.secondAnswer, other.thirdAnswer,
                             other.fourthAnswer]
        if self.lenOfTest == 1:
            other.nextButton.hide()
        else:
            other.nextButton.clicked.connect(lambda: self.nextQuestion(other))
        other.previousButton.clicked.connect(lambda: self.previousQuestion(other))
        other.previousButton.hide()
        other.continueButton.clicked.connect(lambda: self.continueQuiz(other))
        self.loadQuestion(other)

    def nextQuestion(self, other):
        QApplication.processEvents()
        self.uploadAnswer()
        self.numberOfQuestions += 1
        if self.numberOfQuestions == self.lenOfTest - 1:
            other.nextButton.hide()
        if self.numberOfQuestions == 1:
            other.previousButton.show()
        self.loadQuestion(other)

    def previousQuestion(self, other):
        QApplication.processEvents()
        self.uploadAnswer()
        self.numberOfQuestions -= 1
        if self.numberOfQuestions == 0:
            other.previousButton.hide()
        if self.numberOfQuestions <= self.lenOfTest - 1:
            other.nextButton.show()
        self.loadQuestion(other)

    def continueQuiz(self, other):
        self.endTimer.cancel()
        self.uploadAnswer()
        resultOfTest = ResultOfTest(other, self.checkAnswers(), self.lenOfTest)

    def uploadAnswer(self):
        for index in range(4):
            if self.radioButtons[index].isChecked():
                self.used[self.numberOfQuestions][1][index] = True
                break

    def checkAnswers(self):
        count = 0
        for index in range(self.lenOfTest):
            if True in self.used[index][1] and self.used[index][0][
                self.used[index][1].index(True)]['isCorrect']:
                count += 1
        return count

    def loadQuestion(self, other):
        QApplication.processEvents()
        if self.numberOfQuestions not in self.used:
            answers = self.file.get_answers(self.numberOfQuestions)
            shuffle(answers)
            isButtonSelected = [False] * 4
            self.used[self.numberOfQuestions] = [answers.copy(), isButtonSelected.copy()]
        else:
            answers, isButtonSelected = self.used[self.numberOfQuestions]
        for i in range(4):
            self.radioButtons[i].setText(answers[i]['text'])
            self.radioButtons[i].setChecked(isButtonSelected[i])
        other.questionLabel.setText(self.file.get_question(self.numberOfQuestions))
