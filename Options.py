from json import load
from os.path import isfile
from PyQt5.QtWidgets import QMessageBox
from random import shuffle


class JSONFile:
    """
    Класс для загрузки .json файла и полезные функции для работы с этим фалом
    """

    def __init__(self):  # Инициализация класса
        self.name = None
        self.time = None
        self.questions = list()
        self.loadJSON()

    def loadJSON(self):  # Загрузка UI и считывание questions.json
        if not isfile('Extra Files/questions.json'):
            errorMessage = QMessageBox()
            errorMessage.setIcon(QMessageBox.Information)
            errorMessage.setText('File does not exist')
            return
        with open('Extra Files/questions.json') as f:
            self.jsonString = load(f)
        if not self.jsonString:
            errorMessage = QMessageBox()
            errorMessage.setIcon(QMessageBox.Information)
            errorMessage.setText('Empty questions.json file')
            return
        self.name = self.jsonString['name']
        self.time = self.jsonString['time']
        self.questions = self.jsonString['questions']
        shuffle(self.questions)

    def get_question(self, number):  # Получение вопроса по номеру
        return self.questions[number]['question']

    def get_answers(self, number):  # Получение ответов на вопрос по номеру
        return self.questions[number]['answers']

    def __len__(self):  # Получение количества вопросов
        return len(self.questions)
