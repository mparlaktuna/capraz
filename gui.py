from src.logger_data import LogData
from src.truck_data_window import TruckDataWindow
from src.data_set_window import DataSetWindow
from src.show_data import ShowData
from src.solver import Solver
from src.annealing1 import Annealing1
from src.data_writer import *

import logging
import sys
import pickle

from PySide.QtGui import *
from PySide.QtCore import *


class MainWindow(QWidget):
    """
    Main window with control buttons logger and running output
    """
    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle("Cross Docking Project")

        self.data = DataStore()
        self.set_buttons()

        self.set_logger()
        self.set_layout()

        self.algorithm_list = {'annealing1': Annealing1}
        self.algorithm_name = 'annealing1'

        self.current_data_set_number = 0
        # add these to gui
        self.number_of_iterations = 100

    def set_buttons(self):
        """
        set buttons for the main gui
        :return:
        """
        self.new_data_set_button = QPushButton('New Data Set')
        self.new_data_set_button.clicked.connect(self.new_data_set)

        self.load_data_set_button = QPushButton('Load Data Set')
        self.load_data_set_button.clicked.connect(self.load_data)

        self.save_data_set_button = QPushButton('Save Data Set')
        self.save_data_set_button.clicked.connect(self.save_data)

        self.truck_data_button = QPushButton('Truck Data')
        self.truck_data_button.clicked.connect(self.show_truck_data_window)

        self.system_data_button = QPushButton('System Data')
        self.system_data_button.clicked.connect(self.show_data_set_window)

        self.algorithm_data_button = QPushButton('Algorithm Data')

        self.generate_data_set_button = QPushButton('Generate Data Set')
        self.generate_data_set_button.clicked.connect(self.generate_data_set)

        self.show_data_button = QPushButton('Show Data Set')
        self.show_data_button.clicked.connect(self.show_data_window)

        self.print_gams_button = QPushButton('Print gams output')
        self.print_gams_button.clicked.connect(self.print_gams)

        self.data_set_ready_button = QPushButton('Setup Data Set')
        self.data_set_ready_button.clicked.connect(self.setup_data_set)

        self.solve_step_button = QPushButton('Solve Next Step')
        self.solve_step_button.clicked.connect(self.solve_step)
        self.solve_step_button.setEnabled(False)

        self.solve_iteration_button = QPushButton('Solve Next Iteration')
        self.solve_iteration_button.clicked.connect(self.solve_iteration)
        self.solve_iteration_button.setEnabled(False)

        self.solve_data_set_button = QPushButton('Solve Data Set')
        self.solve_data_set_button.setEnabled(False)

        self.show_logger_button = QPushButton('Show Logger')
        self.show_simulation_button = QPushButton('Show Simulation')
        self.show_data_table = QPushButton('Show Run Time Data Table')

        self.debug_check = QCheckBox('Debug Mode')
        self.debug_check.stateChanged.connect(self.set_logger_output)

        self.data_set_number = QSpinBox()
        self.data_set_number.setMinimum(1)
        self.data_set_number.valueChanged.connect(self.set_data_set_number)

        #
        #
        #
        #
        #
        # self.algorithm_data_button.clicked.connect(self.show_algorithm_data)
        #
        #
        # self.show_data_button.clicked.connect(self.show_data)
        #
        #
        #
        #
        # self.show_logger_button.clicked.connect(self.show_logger)
        # self.show_data_table.clicked.connect(self.show_runtime_table)
        #
        # self.solve_next_data_set_button.clicked.connect(self.data_set_button)
        #
        #
        #

    def set_logger(self):
        """
        setup logger with info output and a channel forward to screen output
        :return:
        """
        self.logger = LogData()
        self.logger_root = logging.getLogger()
        self.logger_root.setLevel(logging.INFO)
        self.logger_ch = logging.StreamHandler(self.logger)
        self.logger_ch.setLevel(logging.INFO)
        self.logger_root.addHandler(self.logger_ch)

    def set_layout(self):
        """
        set layout of the main screen
        :return:
        """
        self.data_set_layout = QGridLayout()
        self.data_set_layout.addWidget(self.new_data_set_button, 1, 1)
        self.data_set_layout.addWidget(self.load_data_set_button, 1, 2)
        self.data_set_layout.addWidget(self.save_data_set_button, 1, 3)
        self.data_set_layout.addWidget(self.debug_check, 1, 4)

        self.data_set_layout.addWidget(self.truck_data_button, 2, 1)
        self.data_set_layout.addWidget(self.system_data_button, 2, 2)
        self.data_set_layout.addWidget(self.algorithm_data_button, 2, 3)

        self.data_set_layout.addWidget(self.generate_data_set_button, 3, 1)
        self.data_set_layout.addWidget(self.show_data_button, 3, 2)
        self.data_set_layout.addWidget(self.print_gams_button, 3, 3)

        self.data_set_layout.addWidget(self.data_set_ready_button, 4, 1)
        self.data_set_layout.addWidget(self.data_set_number, 4, 2)

        self.solver_layout = QGridLayout()
        self.solver_layout.addWidget(self.solve_step_button, 1, 1)
        self.solver_layout.addWidget(self.solve_iteration_button, 1, 2)
        self.solver_layout.addWidget(self.solve_data_set_button, 1, 3)

        self.interaction_layout = QGridLayout()
        self.interaction_layout.addWidget(self.show_logger_button, 1, 1)
        self.interaction_layout.addWidget(self.show_simulation_button, 1, 3)
        self.interaction_layout.addWidget(self.show_data_table, 1, 4)

        self.button_layout = QVBoxLayout()
        self.button_layout.addLayout(self.data_set_layout)
        self.button_layout.addLayout(self.solver_layout)
        # self.button_layout.addLayout(self.interaction_layout)

        self.layout = QGridLayout()
        self.layout.addLayout(self.button_layout, 1, 1)
        self.layout.addWidget(self.logger, 1, 2)

        self.setLayout(self.layout)

    def set_logger_output(self, state):
        """
        setup logger output between info and debug depending on the check box on main screen
        :param state:
        :return:
        """
        if state == Qt.Checked:
            self.logger_root.setLevel(logging.DEBUG)
            self.logger_ch.setLevel(logging.DEBUG)
            logging.info("Debug Mode")
        else:
            self.logger_root.setLevel(logging.INFO)
            self.logger_ch.setLevel(logging.INFO)
            logging.info("Normal Mode")

    def new_data_set(self):
        """
        new data set
        """
        self.data = DataStore()
        logging.debug('New Data Set')

    def load_data(self):
        """
        loads prev saved data
        :return:
        """
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        try:
            self.data = pickle.load(open(file_name, 'rb'))
            logging.info('Loaded file: {0}'.format(file_name))
        except Exception as e:
            logging.info(e)

    def save_data(self):
        """
        saves current data
        :return:
        """
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save file', '/home')
        try:
            pickle.dump(self.data,  open(file_name, 'wb'))
            logging.info('Saved to file: {0}'.format(file_name))
        except Exception as e:
            logging.info(e)

    def show_truck_data_window(self):
        self.truck_data_window = TruckDataWindow(self.data)
        self.truck_data_window.exec_()

    def show_data_set_window(self):
        self.data_set_window = DataSetWindow(self.data)
        self.data_set_window.exec_()

    def show_data_window(self):
        self.data_window = ShowData(self.data)
        self.data_window.exec_()

    def generate_data_set(self):
        # ask if sure

        self.data.arrival_times = []
        self.data.boundaries = []
        self.model = Solver(self.data)

        for i in range(len(self.data.data_set_list)):
            self.model.current_data_set = i
            self.model.set_data()

    def print_gams(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Open file', '/home')
        for i in range(len(self.data.data_set_list)):
            gams_writer(file_name + str(i), i, self.data )

    def set_data_set_number(self):
        self.current_data_set_number = self.data_set_number.value() - 1

    def setup_data_set(self):
        # setup for one data set
        self.model = Solver(self.data)
        self.model.current_data_set = self.current_data_set_number
        self.model.load_data_set()
        self.algorithm = self.algorithm_list[self.algorithm_name](self.number_of_iterations, self.current_data_set_number, self.model, self.data)

        logging.info("Solving using {0} data set {1}".format(self.algorithm_name, self.current_data_set_number + 1))
        logging.info("Nuber of iterations {0}".format(self.number_of_iterations))

        self.solve_step_button.setEnabled(True)
        self.solve_iteration_button.setEnabled(True)
        self.solve_data_set_button.setEnabled(True)

    def solve_step(self):
        self.algorithm.step_mode = True
        self.algorithm.solve()

    def solve_iteration(self):
        self.algorithm.step_mode = False
        self.algorithm.solve()

if __name__ == '__main__':
    myApp = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showMaximized()
    myApp.exec_()
    sys.exit(0)
