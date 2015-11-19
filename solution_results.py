from src.sequence import Sequence


class ComingTruckTimes(object):
    def __init__(self, arrival_time = 0, unloading_time = 0):
        self.arrival_time = arrival_time
        self.unloading_time = unloading_time


class GoingTruckTimes(object):
    def __init__(self, arrival_time = 0, loading_time = 0, error = 0):
        self.arrival_time = arrival_time
        self.loading_time = loading_time
        self.error = error


class SolutionResults(object):
    def __init__(self):
        self.data_set_number = None
        self.iteration_number = None
        self.solution_name = None

        self.number_of_inbound_trucks = 0
        self.number_of_outbound_trucks = 0
        self.number_of_compound_trucks = 0

        self.solution_sequence = Sequence()

        self.coming_truck_times = {}
        self.going_truck_times = {}

    def add_coming_truck(self, truck_name):
        times = self.coming_truck_times()
        self.coming_truck_times[truck_name] = times

    def add_going_truck(self, truck_name):
        times = self.going_truck_times()
        self.going_truck_times[truck_name] = times

    def print_to_file(self):
        pass
