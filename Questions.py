from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QInputDialog
from PyQt5 import uic
from random import shuffle
import threading

from Options import JSONFile
from ResultOfTest import ResultOfTest


class Questions(QWidget):
    """Класс для просмотра вопросов и ответа на вопросы с mode='test'
     Иначе же работает в режиме просмотра ответов пользователя """

    def __init__(self, other, mode=None):  # Инициализация класса
        super().__init__()
        self.file = JSONFile()
        self.used = dict()
        self.numberOfQuestions = 0
        self.lenOfTest = len(self.file)
        self.loadUI(other, mode)

    def loadUI(self, other, mode):  # Загрузка UI и авторизация пользователя
        if mode == 'test':
            if self.lenOfTest == 0:  # Проверяет есть ли вопросы в тесте
                errorMessage = QMessageBox()
                errorMessage.setIcon(QMessageBox.Information)
                errorMessage.setText('Questions are not found')
                other.loadUI()  # Возвращение в главное меню
                return

            self.endTimer = threading.Timer(
                int(self.file.time.split(':')[0]) * 60 + int(self.file.time.split(':')[1]),
                lambda x: self.continueQuiz(other,
                                            mode))  # Таймер, заканчивающий тест через заданное время
            self.endTimer.start()
            self.authorisation(other)

        self.numberOfQuestions = 0
        QApplication.processEvents()
        uic.loadUi('UIs/QuestionsUI.ui', other)
        self.radioButtons = [other.firstAnswer, other.secondAnswer, other.thirdAnswer,
                             other.fourthAnswer]  # Список кнопок для выбора ответа
        if self.lenOfTest == 1:
            other.nextButton.hide()
        else:
            other.nextButton.clicked.connect(lambda: self.nextQuestion(other, mode))
        other.previousButton.clicked.connect(lambda: self.previousQuestion(other, mode))
        other.previousButton.hide()
        if mode is None:
            other.continueButton.setText('Result')
            for elem in self.radioButtons:
                elem.setEnabled(False)
        other.continueButton.clicked.connect(
            lambda: self.continueQuiz(other, mode))
        other.timer.hide()
        self.setupQuestions(mode)
        self.loadQuestion(other, mode)

    def authorisation(self, other):  # Получение данных о пользователе
        self.name = QInputDialog.getText(other, "Enter your name",
                                         "What's your name?")[0]
        if not self.name:
            self.name = 'noname'

        self.surname = QInputDialog.getText(other, "Enter your surname",
                                            "What's your surname?")[0]
        if not self.surname:
            self.surname = 'nosurname'

        self.grade = QInputDialog.getText(other, "Enter your grade",
                                          "In what grade do you study?")[0]
        if not self.grade:
            self.grade = 'not determined'

    def nextQuestion(self, other, mode):  # Переход к следующему вопросу
        QApplication.processEvents()
        if mode == 'test':
            self.uploadAnswer()
        self.numberOfQuestions += 1
        if self.numberOfQuestions == self.lenOfTest - 1:
            other.nextButton.hide()
        if self.numberOfQuestions == 1:
            other.previousButton.show()
        self.loadQuestion(other, mode)

    def previousQuestion(self, other, mode):  # Переход к предыдущему вопросу
        QApplication.processEvents()
        if mode == 'test':
            self.uploadAnswer()
        self.numberOfQuestions -= 1
        if self.numberOfQuestions == 0:
            other.previousButton.hide()
        if self.numberOfQuestions <= self.lenOfTest - 1:
            other.nextButton.show()
        self.loadQuestion(other, mode)

    def continueQuiz(self, other, mode):  # Окончание тестирование, переход к результатам
        if mode == 'test':
            self.endTimer.cancel()
            self.uploadAnswer()
        resultOfTest = ResultOfTest(other, self.checkAnswers(), self.file.name,
                                    self.lenOfTest, self.name, self.surname, self.grade)

    def uploadAnswer(self):  # Кэширование ответов и порядка вопросов
        for index in range(4):
            if self.radioButtons[index].isChecked():
                self.used[self.numberOfQuestions][1][index] = True
                break

    def checkAnswers(self):  # Проверка и подсчет правильных ответов
        count = 0
        for index in range(len(self.used.keys())):
            if True in self.used[index][1] and self.used[index][0][
                self.used[index][1].index(True)]['isCorrect']:
                count += 1
                self.used[index].append(True)
            else:
                self.used[index].append(False)
        return count

    def setupQuestions(self, mode):  # Прогрузка порядка ответов и порядка вопросов
        for index in range(self.lenOfTest):
            if mode == 'test':
                answers = self.file.get_answers(index)
                shuffle(answers)
                isButtonSelected = [False] * 4
                self.used[index] = [answers.copy(), isButtonSelected.copy()]

    def loadQuestion(self, other,
                     mode):  # Смена вопросов и ответов в UI.
        # Подсветка правильных и неправильных в режиме просмотра ответов
        QApplication.processEvents()
        answers = self.used[self.numberOfQuestions][0]
        isButtonSelected = self.used[self.numberOfQuestions][1]
        for i in range(4):
            self.radioButtons[i].setText(answers[i]['text'])
            self.radioButtons[i].setChecked(isButtonSelected[i])
            if mode is None:
                self.radioButtons[i].setStyleSheet('default_style_sheet')
                if not self.used[self.numberOfQuestions][2] and isButtonSelected[i]:
                    self.radioButtons[i].setStyleSheet('color: red')
                if answers[i]['isCorrect']:
                    self.radioButtons[i].setStyleSheet('color: green')
        other.questionLabel.setText(self.file.get_question(self.numberOfQuestions))
