from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QApplication
from PyQt5 import uic
from os.path import isfile
import csv

from Options import JSONFile


class ResultsAll(QWidget):
    """Класс, содержащий в себе работу вывода результатов"""

    def __init__(self, other):  # Инициализация класса
        super().__init__()
        self.file = JSONFile()
        self.loadUI(other)

    def loadUI(self, other):  # Загрузка UI
        uic.loadUi('UIs/ResultsUI.ui', other)
        other.testName.setText(self.file.name)
        other.mainMenu.clicked.connect(lambda: self.mainMenu(other))
        self.uploadTable(other)

    def mainMenu(self, other):  # Возвращение в меню
        other.loadUI()

    def uploadTable(self, other):  # Загрузка и ее вывод таблицы
        QApplication.processEvents()
        if not isfile('Extra Files/results.csv'):  # Проверяем есть ли файл в программе
            errorMessage = QMessageBox()
            errorMessage.setIcon(QMessageBox.Information)
            errorMessage.setText('File does not exist')
            return
        with open('Extra Files/results.csv',
                  encoding="utf8") as csvfile:  # Проверяем пустая ли таблица
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            other.table.setColumnCount(8)
            other.table.setHorizontalHeaderLabels(["Name", "Surname", "Class", "Time", "Test",
                                                   "Result", "Percent", "Mark"])
            other.table.setRowCount(0)
            for i, row in enumerate(reader):
                other.table.setRowCount(other.table.rowCount() + 1)
                for j, elem in enumerate(row):
                    other.table.setItem(i, j, QTableWidgetItem(elem))
            other.table.resizeColumnsToContents()
