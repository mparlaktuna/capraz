from src.sequence import Sequence

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog

from src.data_store import DataStore


class SetSequence(QDialog):

    def __init__(self, data=DataStore):
        QDialog.__init__(self)
        self.data = data

        self.inbound_sequence_list = []
        self.outbound_sequence_list = []

        self.inbound_buttons = []
        self.outbound_buttons = []

        self.inboundlayout = QHBoxLayout()
        self.outboundlayout = QHBoxLayout()

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.inboundlayout)
        self.layout.addLayout(self.outboundlayout)

        self.done_button = QPushButton('Done')
        self.done_button.clicked.connect(self.sequence_done)
        self.layout.addWidget(self.done_button)

        self.setWindowTitle('Set Sequence')
        self.setGeometry(300, 400, 500, 500)
        self.setWindowModality(Qt.ApplicationModal)
        self.setLayout(self.layout)
        self.set_truck_and_doors()
        self.set_buttons()
        self.sequence = Sequence()

    def set_truck_and_doors(self):
        for i in range(self.data.number_of_inbound_trucks):
            text = 'inbound' + str(i)
            self.inbound_sequence_list.append(text)

        for i in range(self.data.number_of_compound_trucks):
            text = 'compound' + str(i)
            self.inbound_sequence_list.append(text)

        for i in range(self.data.number_of_receiving_doors - 1):
            text = str(i)
            self.inbound_sequence_list.append(text)

        for i in range(self.data.number_of_outbound_trucks):
            text = 'outbound' + str(i)
            self.outbound_sequence_list.append(text)

        for i in range(self.data.number_of_compound_trucks):
            text = 'compound' + str(i)
            self.outbound_sequence_list.append(text)

        for i in range(self.data.number_of_shipping_doors - 1):
            text = str(i)
            self.outbound_sequence_list.append(text)

    def set_buttons(self):
        for i in range(len(self.inbound_sequence_list)):
            new_scroll = QComboBox()
            self.inboundlayout.addWidget(new_scroll)
            self.inbound_buttons.append(new_scroll)
            new_scroll.addItems(self.inbound_sequence_list)

        for i in range(len(self.outbound_sequence_list)):
            new_scroll = QComboBox()
            self.outboundlayout.addWidget(new_scroll)
            self.outbound_buttons.append(new_scroll)
            new_scroll.addItems(self.outbound_sequence_list)

    def set_sequence(self):
        self.sequence.inbound_sequence = []
        self.sequence.outbound_sequence = []

        for combobox in self.inbound_buttons:
            self.sequence.inbound_sequence.append(combobox.currentText())

        for combobox in self.outbound_buttons:
            self.sequence.outbound_sequence.append(combobox.currentText())

        return self.sequence

    def sequence_done(self):
        self.accept()




