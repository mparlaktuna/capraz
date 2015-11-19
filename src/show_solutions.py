__author__ = 'mustafa'

from PyQt5.QtWidgets import QWidget
from solution_results import SolutionResults

class ShowSolutions(QWidget):

    def __init__(self, results=SolutionResults()):
        QWidget.__init__(self)

        self.setGeometry(300, 400, 500, 500)
        self.setWindowTitle('Show Best Solution')
        self.solution_results = results
