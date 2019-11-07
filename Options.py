from json import load
from os.path import isfile
from PyQt5.QtWidgets import QMessageBox
from random import shuffle


class JSONFile:
    def __init__(self):
        self.name = None
        self.time = None
        self.questions = list()
        self.loadJSON()

    def loadJSON(self):
        if not isfile('questions.json'):
            errorMessage = QMessageBox()
            errorMessage.setIcon(QMessageBox.Information)
            errorMessage.setText('File does not exist')
            return
        with open('questions.json') as f:
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

    def get_question(self, number):
        return self.questions[number]['question']

    def get_answers(self, number):
        return self.questions[number]['answers']

    def __len__(self):
        return len(self.questions)
