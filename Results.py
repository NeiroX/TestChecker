from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QApplication
from PyQt5 import uic
from os.path import isfile
import csv

from Options import JSONFile


class ResultsAll(QWidget):
    def __init__(self, other):
        super().__init__()
        self.file = JSONFile()
        self.loadUI(other)

    def loadUI(self, other):
        uic.loadUi('UIs/ResultsUI.ui', other)
        other.testName.setText(self.file.name)
        other.mainMenu.clicked.connect(lambda: self.mainMenu(other))
        self.uploadTable(other)

    def mainMenu(self, other):
        other.loadUI()

    def uploadTable(self, other):
        QApplication.processEvents()
        if not isfile('Extra Files/results.csv'):
            errorMessage = QMessageBox()
            errorMessage.setIcon(QMessageBox.Information)
            errorMessage.setText('File does not exist')
            return
        with open('Extra Files/results.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            if not reader:
                errorMessage = QMessageBox()
                errorMessage.setIcon(QMessageBox.Information)
                errorMessage.setText('File is empty')
                return
            title = next(reader)
            other.table.setColumnCount(len(title))
            other.table.setHorizontalHeaderLabels(title)
            other.table.setRowCount(0)
            for i, row in enumerate(reader):
                other.table.setRowCount(other.table.rowCount() + 1)
                for j, elem in enumerate(row):
                    other.table.setItem(i, j, QTableWidgetItem(elem))
        other.table.resizeColumnsToContents()
