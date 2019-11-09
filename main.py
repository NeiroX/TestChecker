from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import sys

from Results import ResultsAll
from Questions import Questions
from Options import JSONFile


class Main(QMainWindow):
    """"
    Класс, содеражщий в себе главное меню
    """

    def __init__(self):  # Инициализация класса
        super().__init__()
        self.file = JSONFile()
        self.loadUI()

    def loadUI(self):  # Функция для загрузки UI
        uic.loadUi('UIs/MenuUI.ui', self)
        self.startButton.clicked.connect(self.start)
        self.resultButton.clicked.connect(self.resultsA)
        self.exitButton.clicked.connect(self.exit)
        self.testName.setText(self.file.name)

    def start(self):  # Функция, запускающая тестирование
        self.questions = Questions(self, 'test')

    def resultsA(self):  # Функция, выводящая таблицу всех результатов
        self.results = ResultsAll(self)

    def exit(self):  # Функция, закрывающая программу
        sys.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
