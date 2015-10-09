__author__ = 'mustafa'

from PySide.QtGui import *
from PySide.QtCore import *
from src.data_writer import print_data

class ShowData(QDialog):
    """
    shows all data inside data store object
    """
    def __init__(self, data):
        QDialog.__init__(self)
        self.data = data
        self.setWindowTitle('Data')
        self.setWindowModality(Qt.ApplicationModal)
        self.textbox = QTextEdit()
        self.textbox.setReadOnly(True)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.textbox)
        self.setLayout(self.layout)
        text = print_data(self.data)
        self.textbox.setText(text)