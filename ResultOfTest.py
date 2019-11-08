from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import uic
import csv
from os.path import isfile
from datetime import datetime
import pytz


class ResultOfTest(QWidget):
    def __init__(self, other, true_answers, testName, lenOfTest, name='noname', surname='nosurname',
                 cl='not determined'):
        super().__init__()
        self.true_answers = true_answers
        self.lenOfTest = lenOfTest
        self.loadUI(other)
        self.writeResultToCSV(name, surname, cl, testName)

    def loadUI(self, other):
        uic.loadUi('UIs/ResultUI.ui', other)
        other.resultLabel.setText(f'{self.true_answers}/{self.lenOfTest}')
        self.resultInPercent = round(self.true_answers / self.lenOfTest * 100)
        other.percentLabel.setText(f'{self.resultInPercent}%')
        if self.resultInPercent >= 85:
            self.mark = '5'
            other.markLabel.setStyleSheet('color: green')
        elif self.resultInPercent >= 65:
            self.mark = '4'
            other.markLabel.setStyleSheet('color: blue')
        elif self.resultInPercent >= 45:
            self.mark = '3'
            other.markLabel.setStyleSheet('color: yellow')
        else:
            self.mark = '2'
            other.markLabel.setStyleSheet('color: red')
        other.markLabel.setText(self.mark)
        other.mainMenuButton.clicked.connect(lambda x: self.mainMenu(other))
        other.viewAnswersButton.clicked.connect(lambda x: self.viewAnswers(other))

    def writeResultToCSV(self, name, surname, cl, testName):
        if not isfile('Extra Files/results.csv'):
            errorMessage = QMessageBox()
            errorMessage.setIcon(QMessageBox.Information)
            errorMessage.setText('File does not exist')
            return
        title = True
        with open('Extra Files/results.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            if not reader:
                title = False
        with open('Extra Files/results.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile,
                                    fieldnames=["Name", "Surname", "Class", "Time", "Test",
                                                "Result", "Percent", "Mark"])
            if not title:
                writer.writeheader()
            writer.writerow({"Name": name, "Surname": surname, "Class": cl,
                             "Time": datetime.now(pytz.timezone('Europe/Moscow')), "Test": testName,
                             "Result": f'{self.true_answers}/{self.lenOfTest}',
                             "Percent": f'{self.resultInPercent}%', "Mark": self.mark})

    def mainMenu(self, other):
        other.loadUI()

    def viewAnswers(self, other):
        other.questions.loadUI(other, None)
