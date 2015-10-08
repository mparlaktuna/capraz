__author__ = 'mustafa'

from PySide.QtGui import *
from PySide.QtCore import * 

from src.truck_table_widget import TruckTableWidget
from src.data_store import DataStore

class TruckDataWindow(QDialog):
    """
    Data window widget
    """
    def __init__(self, data=DataStore()):
        QDialog.__init__(self)
        self.data = data
        self.inboundView = []
        self.outboundView = []
        self.compoundView = []
        self.setWindowTitle('Truck Data Window')

        self.setupComponents()
        self.setGeometry(300, 400, 500, 500)
        self.setWindowModality(Qt.ApplicationModal)


    def setupComponents(self):
        """
        Setup all the components, statusbar, menubar, toolbar
        :return:
        """
        self.setupButtons()
        self.setupLayout()
        self.prev_data()
        self.setup_connections()
        self.data_change()

    def setupButtons(self):

        self.numberGoodLabel = QLabel("Number of good types")
        self.numberGoodLabel.setMaximumWidth(150)
        self.numberGoodsSpin = QSpinBox()
        self.numberGoodsSpin.setMinimum(1)
        self.numberGoodsSpin.setMaximumWidth(70)

        self.numberReceiveDoorLabel = QLabel("Number of receiver doors")
        self.numberReceiveDoorLabel.setMaximumWidth(150)
        self.numberReceiveDoorSpin = QSpinBox()
        self.numberReceiveDoorSpin.setMinimum(0)
        self.numberReceiveDoorSpin.setMaximumWidth(70)

        self.numberShippingDoorLabel = QLabel("Number of shipping doors")
        self.numberShippingDoorLabel.setMaximumWidth(150)
        self.numberShippingDoorSpin = QSpinBox()
        self.numberShippingDoorSpin.setMinimum(0)
        self.numberShippingDoorSpin.setMaximumWidth(70)

        self.numberInbound = QLabel("Number of inbound trucks")
        self.numberInbound.setMaximumWidth(150)
        self.numberInboundSpin = QSpinBox()
        self.numberInboundSpin.setMinimum(0)

        self.numberOutbound = QLabel("Number of outbound trucks")
        self.numberOutbound.setMaximumWidth(150)
        self.numberOutboundSpin = QSpinBox()
        self.numberOutboundSpin.setMinimum(0)

        self.numberCompound = QLabel("Number of compound trucks")
        self.numberCompound.setMaximumWidth(150)
        self.numberCompoundSpin = QSpinBox()
        self.numberCompoundSpin.setMinimum(0)

        self.doneButton = QPushButton("Done")

    def setupLayout(self):
        """
        Setup the layout for the data window
        :return:
        """
        self.mainVBox = QVBoxLayout()
        self.truckForm = QFormLayout()
        self.doorForm = QFormLayout()
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(False)
        self.hBoxMainData = QHBoxLayout()
        self.vBoxTruckData = QVBoxLayout()

        self.vInboundTruck = QVBoxLayout()

        self.vOutBoundTruck = QVBoxLayout()
        self.vCompoundTruck = QVBoxLayout()
        self.inboundLabel = QLabel('Inbound Trucks')
        self.outboundLabel = QLabel('Outbound Trucks')
        self.compoundLabel = QLabel('Compound Trucks')

        self.vInboundTruck.addWidget(self.inboundLabel)
        self.vOutBoundTruck.addWidget(self.outboundLabel)
        self.vCompoundTruck.addWidget(self.compoundLabel)

        self.good_widget = QWidget()
        self.good_layout = QVBoxLayout()
        self.good_widget.setLayout(self.good_layout)

        self.good_layout.addLayout(self.vInboundTruck)
        self.good_layout.addLayout(self.vOutBoundTruck)
        self.good_layout.addLayout(self.vCompoundTruck)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.good_widget)

        self.truckForm.addRow(self.numberInbound, self.numberInboundSpin)
        self.truckForm.addRow(self.numberOutbound, self.numberOutboundSpin)
        self.truckForm.addRow(self.numberCompound, self.numberCompoundSpin)
        self.doorForm.addRow(self.numberReceiveDoorLabel, self.numberReceiveDoorSpin)
        self.doorForm.addRow(self.numberShippingDoorLabel, self.numberShippingDoorSpin)
        self.doorForm.addRow(self.numberGoodLabel, self.numberGoodsSpin)

        self.hBoxMainData.addLayout(self.truckForm)
        self.hBoxMainData.addLayout(self.doorForm)
        self.hBoxMainData.addWidget(self.doneButton)
        self.mainVBox.addLayout(self.hBoxMainData)

        self.mainVBox.addWidget(self.scroll)
        self.setLayout(self.mainVBox)

    def setup_connections(self):
        self.numberGoodsSpin.valueChanged.connect(self.data_change)
        self.numberInboundSpin.valueChanged.connect(self.data_change)
        self.numberOutboundSpin.valueChanged.connect(self.data_change)
        self.numberCompoundSpin.valueChanged.connect(self.data_change)
        self.numberShippingDoorSpin.valueChanged.connect(self.data_change)
        self.numberReceiveDoorSpin.valueChanged.connect(self.data_change)
        self.doneButton.clicked.connect(self.truck_done)

    def truck_done(self):
        self.save_data()
        self.accept()

    def save_data(self):
        self.data.calculate_truck_data()
        self.data.inbound_goods = []
        self.data.outbound_goods = []
        self.data.compound_going_goods = []
        self.data.compound_coming_goods = []
        missing_data = False

        for inbound_truck in self.inboundView:
            goods = []
            for i in range(0, self.numberGoodsSpin.value()):
                data = inbound_truck.goodTable.item(0,i)
                if data:
                    goods.append(int(data.text()))
                else:
                    missing_data = True

            self.data.inbound_goods.append(goods)

        for outbound_truck in self.outboundView:
            goods = []
            for i in range(0, self.numberGoodsSpin.value()):
                data = outbound_truck.goodTable.item(0, i)
                if data:
                    goods.append(int(data.text()))
                else:
                    missing_data = True
            self.data.outbound_goods.append(goods)

        for compound_truck in self.compoundView:
            goods = []
            for i in range(0, self.numberGoodsSpin.value()):
                data = compound_truck.goodTable.item(0, i)
                if data:
                    goods.append(int(data.text()))
                else:
                    missing_data = True
            self.data.compound_coming_goods.append(goods)

            goods = []
            for i in range(0, self.numberGoodsSpin.value()):
                data = compound_truck.goodTable.item(1, i)

                if data:
                    goods.append(int(data.text()))
                else:
                    missing_data = True
            self.data.compound_going_goods.append(goods)

    def prev_data(self):
        """
        load previous data
        :type self: object
        :return:
        """
        self.numberGoodsSpin.setValue(self.data.number_of_goods)
        self.numberInboundSpin.setValue(self.data.number_of_inbound_trucks)
        self.numberOutboundSpin.setValue(self.data.number_of_outbound_trucks)
        self.numberCompoundSpin.setValue(self.data.number_of_compound_trucks)
        self.numberShippingDoorSpin.setValue(self.data.number_of_shipping_doors)
        self.numberReceiveDoorSpin.setValue(self.data.number_of_receiving_doors)
        
        self.update_good_table()

        for i in range(self.data.number_of_inbound_trucks):
            name = 'inbound' + str(i)
            self.inboundView.append(TruckTableWidget(self.numberGoodsSpin.value(), 'inbound'))
            self.vInboundTruck.addWidget(self.inboundView[-1])
            self.update_good_table()
            for k in range(self.data.number_of_goods):
                new_item = QTableWidgetItem()
                new_item.setText(str(self.data.inbound_goods[i][k]))
                self.inboundView[-1].goodTable.setItem(0, k, new_item)

        for i in range(self.data.number_of_outbound_trucks):
            name = 'outbound' + str(i)
            self.outboundView.append(TruckTableWidget(self.numberGoodsSpin.value(), 'outbound'))
            self.vOutBoundTruck.addWidget(self.outboundView[-1])
            self.update_good_table()
            for k in range(self.data.number_of_goods):
                new_item = QTableWidgetItem()
                new_item.setText(str(self.data.outbound_goods[i][k]))
                self.outboundView[-1].goodTable.setItem(0,k,new_item)

        for i in range(self.data.number_of_compound_trucks):
            name = 'compound' + str(i)
            self.compoundView.append(TruckTableWidget(self.numberGoodsSpin.value(), 'compound'))
            self.vCompoundTruck.addWidget(self.compoundView[-1])
            self.update_good_table()
            for k in range(self.data.number_of_goods):
                new_coming_item = QTableWidgetItem()
                new_coming_item.setText(str(self.data.compound_coming_goods[i][k]))
                self.compoundView[-1].goodTable.setItem(0, k, new_coming_item)
                new_going_item = QTableWidgetItem()
                new_going_item.setText(str(self.data.compound_going_goods[i][k]))
                self.compoundView[-1].goodTable.setItem(1, k, new_going_item)

    def data_change(self):
        self.data.number_of_goods = self.numberGoodsSpin.value()
        self.data.number_of_receiving_doors = self.numberReceiveDoorSpin.value()
        self.data.number_of_shipping_doors = self.numberShippingDoorSpin.value()
        self.data.number_of_inbound_trucks = self.numberInboundSpin.value()
        self.data.number_of_outbound_trucks = self.numberOutboundSpin.value()
        self.data.number_of_compound_trucks = self.numberCompoundSpin.value()
        self.data.number_of_shipping_doors = self.numberShippingDoorSpin.value()
        self.data.number_of_receiving_doors = self.numberReceiveDoorSpin.value()

        if self.numberInboundSpin.value() > len(self.inboundView):
            self.inboundView.append(TruckTableWidget(self.numberGoodsSpin.value(), 'inbound'))
            self.vInboundTruck.addWidget(self.inboundView[-1])

        if self.numberInboundSpin.value() < len(self.inboundView):
            delete_widget = self.inboundView.pop()
            delete_widget.deleteLater()

        if self.numberOutboundSpin.value() > len(self.outboundView):
            self.outboundView.append(TruckTableWidget( self.numberGoodsSpin.value(), 'outbound'))
            self.vOutBoundTruck.addWidget(self.outboundView[-1])

        if self.numberOutboundSpin.value() < len(self.outboundView):
            delete_widget = self.outboundView.pop()
            delete_widget.deleteLater()

        if self.numberCompoundSpin.value() > len(self.compoundView):
            self.compoundView.append(TruckTableWidget(self.numberGoodsSpin.value(),'compound'))
            self.vCompoundTruck.addWidget(self.compoundView[-1])

        if self.numberCompoundSpin.value() < len(self.compoundView):
            delete_widget = self.compoundView.pop()
            delete_widget.deleteLater()

        self.save_data()
        self.update_good_table()

    def update_good_table(self):
        for truck_widget in self.inboundView:
            truck_widget.number_of_goods = self.numberGoodsSpin.value()
            truck_widget.update_table()

        for truck_widget in self.outboundView:
            truck_widget.number_of_goods = self.numberGoodsSpin.value()
            truck_widget.update_table()

        for truck_widget in self.compoundView:
            truck_widget.number_of_goods = self.numberGoodsSpin.value()
            truck_widget.update_table()
