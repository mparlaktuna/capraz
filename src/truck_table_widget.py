__author__ = 'mustafa'

from PySide.QtGui import *


class TruckTableWidget(QWidget):
    """
    Truck Data Widget
    """
    def __init__(self, number_of_goods, type):
        QWidget.__init__(self)
        self.type = type

        self.truckHLayout = QHBoxLayout(self)
        self.number_of_goods = number_of_goods
        self.goodTable = QTableWidget(1,number_of_goods,self)

        # add the widget elements to the layout
        self.truckHLayout.addWidget(self.goodTable,2)

        self.update_table()

    def update_table(self):

        self.goodTable.setColumnCount(self.number_of_goods)

        self.goodTable.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        if self.type == 'inbound':
            self.goodTable.setVerticalHeaderLabels(['Coming'])
            self.goodTable.setMaximumHeight(50)

        elif self.type == 'outbound':

            self.goodTable.setVerticalHeaderLabels(['Going'])
            self.goodTable.setMaximumHeight(52)

        elif self.type == 'compound':
            self.goodTable.setRowCount(2)
            self.goodTable.setVerticalHeaderLabels(['Coming', 'Going'])
            self.goodTable.setMaximumHeight(88)