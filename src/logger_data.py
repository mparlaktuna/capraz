__author__ = 'mustafa'

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class LogData(QWidget):
    """
    shows all data inside data store object
    """
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Logger')
        self.textbox = QTextEdit()
        self.textbox.setReadOnly(True)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.textbox)
        self.setLayout(self.layout)

    def write(self, message):
        self.textbox.moveCursor(QTextCursor.End)
        self.textbox.insertPlainText(message)

