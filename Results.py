from PyQt5.QtWidgets import QWidget
from PyQt5 import uic


class Results(QWidget):
    def __init__(self):
        super().__init__()
        self.loadUI()

    def loadUI(self):
        uic.loadUi('UIs/ResultsUI.ui')
