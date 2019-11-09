from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import uic
import csv
from os.path import isfile
from datetime import datetime
import pytz
import operator


class ResultOfTest(QWidget):
    """
    Класс, отвечающий за вывод результатов и дальнейших действий пользователя
    """

    def __init__(self, other, true_answers, testName, lenOfTest, name, surname,
                 cl):  # Инициализация класса
        super().__init__()
        self.true_answers = true_answers
        self.lenOfTest = lenOfTest
        self.loadUI(other)
        self.writeResultToCSV(name, surname, cl, testName)

    def loadUI(self, other):  # Загрузка UI и вывод различной статистики
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

    def mainMenu(self, other):  # Возвращение в главное меню
        other.loadUI()

    def writeResultToCSV(self, name, surname, cl,
                         testName):  # Записывает результат пользователя в таблицу
        if not isfile('Extra Files/results.csv'):
            errorMessage = QMessageBox()
            errorMessage.setIcon(QMessageBox.Information)
            errorMessage.setText('File does not exist')
            return
        rows = list()
        with open('Extra Files/results.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                rows.append(row)
        with open('Extra Files/results.csv', 'w', newline='\n') as csvfile:
            writer = csv.writer(
                csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            rows.append([name, surname, cl, datetime.now(pytz.timezone('Europe/Moscow')), testName,
                         f'{self.true_answers}/{self.lenOfTest}', f'{self.resultInPercent}%',
                         self.mark])
            for row in list(sorted(rows, key=operator.itemgetter(4, 7))):
                writer.writerow(row)

    def viewAnswers(self, other):  # Открывает ответы пользователя
        other.questions.loadUI(other, None)
