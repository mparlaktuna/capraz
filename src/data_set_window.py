__author__ = 'robotes'

from src.data_store import DataStore

from PySide.QtGui import *
from PySide.QtCore import *

import logging

class DataSetWindow(QDialog):
    """
    Data set window widget
    """
    def __init__(self, data=DataStore()):
        QDialog.__init__(self)
        self.data = data
        self.setWindowTitle('Data Set Window')
        self.setWindowModality(Qt.ApplicationModal)        
        self.setupComponents()
        self.setupButtons()
        self.setupComponents()
        self.setupConnections()
        self.setup_layout()
        self.load_data()


    def setupConnections(self):

        self.numberOfDataSpin.valueChanged.connect(self.update_tables)

    def setupComponents(self):
        self.dataTable = QTableWidget(1, 3)

    def setupButtons(self):
        self.loadingTimeLabel = QLabel("Loading Time")
        self.loadingTimeEdit = QLineEdit()

        self.changeoverTimeLabel = QLabel("Truck Changeover Time")
        self.changeoverTimeEdit = QLineEdit()

        self.makespanFactorLabel = QLabel("Effect of the arrival times on makespan")
        self.makespanFactorEdit = QLineEdit()

        self.transferTimeLabel = QLabel("Truck Transferr Time")
        self.transferTimeEdit = QLineEdit()

        self.inboundArrivalTimeLabel = QLabel("Inbound Arrival Time")
        self.inboundArrivalTimeEdit = QLineEdit()

        self.outboundArrivalTimeLabel = QLabel("Outbound Arrival Time")
        self.outboundArrivalTimeEdit = QLineEdit()

        self.goodTransferTimeLabel = QLabel("Good Transfer Time")
        self.goodTransferTimeEdit = QLineEdit()

        self.doneButton = QPushButton('Done')
        self.doneButton.clicked.connect(self.save_data)

        self.numberOfDataLabel = QLabel("Number of data sets")
        self.numberOfDataSpin = QSpinBox()
        self.numberOfDataSpin.setMinimum(1)

    def setup_layout(self):

        self.dataSetForm = QFormLayout()
        self.vTableLayout = QVBoxLayout()
        self.mainLayout = QHBoxLayout()
        
        self.dataSetForm.addRow(self.loadingTimeLabel, self.loadingTimeEdit)
        self.dataSetForm.addRow(self.changeoverTimeLabel, self.changeoverTimeEdit)
        self.dataSetForm.addRow(self.makespanFactorLabel, self.makespanFactorEdit)
        self.dataSetForm.addRow(self.transferTimeLabel, self.transferTimeEdit)
        self.dataSetForm.addRow(self.inboundArrivalTimeLabel, self.inboundArrivalTimeEdit)
        self.dataSetForm.addRow(self.outboundArrivalTimeLabel, self.outboundArrivalTimeEdit)
        self.dataSetForm.addRow(self.goodTransferTimeLabel, self.goodTransferTimeEdit)
        self.dataSetForm.addRow(self.numberOfDataLabel, self.numberOfDataSpin)
        self.dataSetForm.addRow(self.doneButton)

        self.vTableLayout.addWidget(self.dataTable)

        self.mainLayout.addLayout(self.dataSetForm)
        self.mainLayout.addLayout(self.vTableLayout)
        
        self.setLayout(self.mainLayout)

    def update_tables(self):

        self.dataTable.setRowCount(self.numberOfDataSpin.value())

    def save_data(self):

        self.data.changeover_time = float(self.changeoverTimeEdit.text())
        self.data.loading_time = float(self.loadingTimeEdit.text())
        self.data.makespan_factor = float(self.makespanFactorEdit.text())
        self.data.transfer_time = float(self.transferTimeEdit.text())
        self.data.good_transfer_time = float(self.goodTransferTimeEdit.text())
        self.data.inbound_arrival_time = float(self.inboundArrivalTimeEdit.text())
        self.data.outbound_arrival_time = float(self.outboundArrivalTimeEdit.text())

        data_set = []
        for value in range(self.numberOfDataSpin.value()):
            alpha_data = self.dataTable.item(value, 0)
            beta_data = self.dataTable.item(value, 1)
            tightness_data = self.dataTable.item(value, 2)
            data_set.append([float(alpha_data.text()), float(beta_data.text()), float(tightness_data.text())])

        self.data.data_set_list = data_set
        logging.debug("data set: {0}".format(self.data.data_set_list))
        # self.data.create_data_set()
        self.close()

    def load_data(self):

        self.loadingTimeEdit.setText(str(self.data.loading_time))
        self.changeoverTimeEdit.setText(str(self.data.changeover_time))
        self.makespanFactorEdit.setText(str(self.data.makespan_factor))
        self.transferTimeEdit.setText(str(self.data.transfer_time))
        self.goodTransferTimeEdit.setText(str(self.data.good_transfer_time))
        self.inboundArrivalTimeEdit.setText(str(self.data.inbound_arrival_time))
        self.outboundArrivalTimeEdit.setText(str(self.data.outbound_arrival_time))

        self.numberOfDataSpin.setValue(len(self.data.data_set_list))

        self.update_tables()

        for i, data_set in enumerate(self.data.data_set_list):
            new_item = QTableWidgetItem()
            new_item.setText(str(data_set[0]))
            self.dataTable.setItem(i, 0, new_item)
            new_item = QTableWidgetItem()
            new_item.setText(str(data_set[1]))
            self.dataTable.setItem(i, 1, new_item)
            new_item = QTableWidgetItem()
            new_item.setText(str(data_set[2]))
            self.dataTable.setItem(i, 2, new_item)
