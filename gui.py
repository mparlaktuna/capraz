__author__ = 'mustafa parlaktuna'

import logging
import sys

from PySide.QtGui import *

from src.logger_data import LogData

class MainWindow(QWidget):
    """
    Main window with control buttons logger and running output
    """
    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle("Cross Docking Project")

        self.set_buttons()
        self.logger = LogData()

        self.set_layout()


    def set_buttons(self):
        self.new_data_set_button = QPushButton('New Data Set')
        self.load_data_set_button = QPushButton('Load Data Set')
        self.save_data_set_button = QPushButton('Save Data Set')

        self.truck_data_button = QPushButton('Truck Data')
        self.system_data_button = QPushButton('System Data')
        self.algorithm_data_button = QPushButton('Algorithm Data')

        self.generate_data_set_button = QPushButton('Generate Data Set')
        self.show_data_button = QPushButton('Show Data Set')
        self.print_gams_button = QPushButton('Print gams output')

        self.data_set_ready_button = QPushButton('Data Set Ready')

        self.solve_step_button = QPushButton('Solve Next Step')
        self.solve_iteration_button = QPushButton('Solve Next Iteration')
        self.solve_next_data_set_button = QPushButton('Solve Next Data Set')

        self.show_logger_button = QPushButton('Show Logger')
        self.show_simulation_button = QPushButton('Show Simulation')
        self.show_data_table = QPushButton('Show Run Time Data Table')

        self.data_set_number = QSpinBox()
        self.data_set_number.setMinimum(0)

        # self.new_data_set_button.clicked.connect(self.new_data_set)
        # self.load_data_set_button.clicked.connect(self.load_data)
        # self.save_data_set_button.clicked.connect(self.save_data)
        #
        # self.truck_data_button.clicked.connect(self.show_truck_data)
        # self.system_data_button.clicked.connect(self.show_system_data)
        # self.algorithm_data_button.clicked.connect(self.show_algorithm_data)
        #
        # self.generate_data_set_button.clicked.connect(self.generate_data_set)
        # self.show_data_button.clicked.connect(self.show_data)
        # self.print_gams_button.clicked.connect(self.print_gams)
        #
        # self.data_set_ready_button.clicked.connect(self.data_set_ready)
        #
        # self.show_logger_button.clicked.connect(self.show_logger)
        # self.show_data_table.clicked.connect(self.show_runtime_table)
        #
        # self.solve_next_data_set_button.clicked.connect(self.data_set_button)
        # self.solve_iteration_button.clicked.connect(self.iteration_button)
        # self.solve_step_button.clicked.connect(self.step_button)
        # self.data_set_number.valueChanged.connect(self.set_data_set_number)

    def set_layout(self):
        self.data_set_layout = QGridLayout()
        self.data_set_layout.addWidget(self.new_data_set_button, 1 ,1)
        self.data_set_layout.addWidget(self.load_data_set_button, 1 ,2)
        self.data_set_layout.addWidget(self.save_data_set_button, 1 ,3)

        self.data_set_layout.addWidget(self.truck_data_button, 2 ,1)
        self.data_set_layout.addWidget(self.system_data_button, 2 ,2)
        self.data_set_layout.addWidget(self.algorithm_data_button, 2 ,3)

        self.data_set_layout.addWidget(self.generate_data_set_button, 3, 1)
        self.data_set_layout.addWidget(self.show_data_button, 3, 2)
        self.data_set_layout.addWidget(self.print_gams_button, 3, 3)

        self.data_set_layout.addWidget(self.data_set_ready_button, 4, 1)

        self.solver_layout = QGridLayout()
        self.solver_layout.addWidget(self.solve_step_button, 1, 1)
        self.solver_layout.addWidget(self.solve_iteration_button, 1, 2)
        self.solver_layout.addWidget(self.solve_next_data_set_button, 1, 3)
        self.solver_layout.addWidget(self.data_set_number, 1, 4)

        self.interaction_layout = QGridLayout()
        self.interaction_layout.addWidget(self.show_logger_button, 1, 1)
        self.interaction_layout.addWidget(self.show_simulation_button, 1, 3)
        self.interaction_layout.addWidget(self.show_data_table, 1, 4)

        self.button_layout = QVBoxLayout()
        self.button_layout.addLayout(self.data_set_layout)
        self.button_layout.addLayout(self.solver_layout)
        self.button_layout.addLayout(self.interaction_layout)

        self.layout = QGridLayout()
        self.layout.addLayout(self.button_layout, 1, 1)
        self.layout.addWidget(self.logger, 1, 2)

        self.setLayout(self.layout)
        self.pause_bool = False

if __name__ == '__main__':
    logging.basicConfig(format='%(message)s',  level=logging.INFO)
    myApp = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showMaximized()
    myApp.exec_()
    sys.exit(0)
