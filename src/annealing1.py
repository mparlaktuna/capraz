from src.solver import Solver
from src.data_store import DataStore
from src.sequence import Sequence

import timeit
import math
import logging
import itertools
import random
import copy

class Annealing1(object):
    """
    annealing algorithm
    """
    def __init__(self, number_of_iterations, data_set_number, model=Solver, data=DataStore):
        self.number_of_iterations = number_of_iterations
        self.data = data
        self.data_set_number = data_set_number
        self.model = model

        self.sequence_list = []
        self.sequences = {}
        self.current_iteration_number = 0

        self.current_seq = dict()
        self.current_seq['inbound'] = []
        self.current_seq['outbound'] = []
        self.current_seq['error'] = 0

        self.step_mode = False

        self.temperature = 100
        self.temperature_reduction_rate = 0.9

    def solve_data_set(self):
        while self.current_iteration_number < self.number_of_iterations:
            self.step_mode = False
            self.solve()
        self.print_data_set_solution()

    def solve(self):
        self.solve_iteration()

    def solve_iteration(self):
        if self.current_iteration_number == 0:
            if self.model.current_time == 0:
                self.start_time = timeit.default_timer()
                self.print_start()
                self.start1()
                self.print_iteration_start()
                self.model.set_sequence(self.sequences['current'])
            self.solve_step()

            # solve
            # calculate next sequence

        elif self.current_iteration_number < self.number_of_iterations:
            if self.model.current_time == 0:
                self.start_time = timeit.default_timer()
                self.print_iteration_start()
                self.annealing1()
                self.random1()
                self.model.set_sequence(self.sequences['current'])
            self.solve_step()

        elif self.current_iteration_number >= self.number_of_iterations:
            self.print_solution()

    def solve_step(self):
        while not self.model.finish:
            self.print_time_step()
            self.model.next_step()
            if self.step_mode:
                logging.debug('Step Break')
                break

        if self.model.finish:
            logging.debug('Iteration Finished')
            # for truck in itertools.chain(self.model.outbound_trucks.values(), self.model.compound_trucks.values()):
                # truck.calculate_error()
            self.add_errors()
            self.model.reset()
            # add reset
            self.current_iteration_number += 1
            self.end_time = timeit.default_timer()
            solution_time = self.end_time - self.start_time
            logging.info("Iteration {0} finished in {1} seconds".format(self.current_iteration_number, solution_time))
            self.model.finish = False
            self.print_iteration_step()

    def add_errors(self):
        """
        adds absolute values of the errors

        :return:
        """
        total_error = 0
        for truck in itertools.chain(self.model.outbound_trucks.values(), self.model.compound_trucks.values()):
            truck.calculate_error()
            logging.info("Truck {0}, error {1}\n".format(truck.truck_name, truck.error))
            total_error += abs(truck.error)
        logging.info("Error: {0}\n".format(total_error))
        self.sequences['current'].error = total_error
        return total_error

    def iteration_finished(self):
        pass

    def print_solution(self):
        pass

    def print_iteration_start(self):
        pass
        # logging.info('Sequences {0}'.format(self.sequences))

    def print_iteration_step(self):
        logging.info("Iteration number {0}".format(self.current_iteration_number))

    def print_time_step(self):
        pass

    def print_start(self):
        logging.info("Data set number {0}".format(self.data_set_number))

    def print_data_set_solution(self):
        print("Best solution inbound{0}".format(self.sequences['best'].inbound_sequence))
        print("Best solution inbound{0}".format(self.sequences['best'].inbound_sequence))
        print("Best solution error{0}".format(self.sequences['best'].error))

        logging.info("Best solution inbound{0}".format(self.sequences['best'].inbound_sequence))
        logging.info("Best solution outbound{0}".format(self.sequences['best'].outbound_sequence))
        logging.info("Best solution error{0}".format(self.sequences['best'].error))

    def start1(self):
        # do for outbound trucks too

        name = 'recv'
        self.init_sequence = [[] for i in range(self.model.number_of_receiving_doors)]

        unsorted_trucks = []
        # sort trucks
        for truck in itertools.chain(self.model.inbound_trucks.values(), self.model.compound_trucks.values()):
            truck_times = (truck.finish_time, truck.truck_name)
            unsorted_trucks.append(truck_times)

        sorted_trucks = [truck for (time, truck) in sorted(unsorted_trucks)]

        i = 0
        for truck in sorted_trucks:
            self.init_sequence[i].append(truck)
            i += 1
            if i == self.model.number_of_receiving_doors:
                i = 0

        i = 0
        for items in self.init_sequence:
            self.current_seq['inbound'].extend(items)
            self.current_seq['inbound'].extend([i])
            i += 1

        self.current_seq['inbound'].pop()

        # outbound
        self.init_sequence = [[] for i in range(self.model.number_of_shipping_doors)]
        unsorted_trucks = []
        # sort trucks
        for truck in self.model.outbound_trucks.values():
            truck_times = (truck.finish_time, truck.truck_name)
            unsorted_trucks.append(truck_times)

        sorted_trucks = [truck for (time, truck) in sorted(unsorted_trucks)]
        for truck in self.model.compound_trucks.values():
            sorted_trucks.append(truck.truck_name)

        i = 0
        for truck in sorted_trucks:
            self.init_sequence[i].append(truck)
            i += 1
            if i == self.model.number_of_shipping_doors:
                i = 0

        i = 0
        for items in self.init_sequence:
            self.current_seq['outbound'].extend(items)
            self.current_seq['outbound'].extend([i])
            i += 1

        self.current_seq['outbound'].pop()

        logging.info("Start sequence inbound: {0}".format(self.current_seq['inbound']))
        logging.info("Start sequence outbound: {0}".format(self.current_seq['outbound']))

        self.current_sequence = Sequence(self.current_seq['inbound'], self.current_seq['outbound'])
        self.prev_sequence = Sequence(self.current_seq['inbound'], self.current_seq['outbound'])
        self.best_sequence = Sequence(self.current_seq['inbound'], self.current_seq['outbound'])
        self.best_sequence.error = float('inf')
        self.prev_sequence.error = float('inf')

        self.sequences['current'] = self.current_sequence
        self.sequences['best'] = self.best_sequence
        self.sequences['prev'] = self.prev_sequence

    def random1(self):
        """
        generates a random next sequence
        :return:
        """
        self.next_sequence = {}
        self.next_sequence['inbound'] = copy.deepcopy(self.sequences['prev'].inbound_sequence)
        self.next_sequence['outbound'] = copy.deepcopy(self.sequences['prev'].outbound_sequence)

        logging.info("Random1 prev sequence inbound: {0}".format(self.sequences['prev'].inbound_sequence))
        logging.info("Random1 prev sequence outbound: {0}".format(self.sequences['prev'].outbound_sequence))

        truck_type = 'inbound'
        a, b = self.generate_random(self.next_sequence['inbound'])
        indexA = self.next_sequence[truck_type].index(a)
        indexB = self.next_sequence[truck_type].index(b)
        self.next_sequence[truck_type][indexA] = b
        self.next_sequence[truck_type][indexB] = a

        truck_type = 'outbound'
        a, b = self.generate_random(self.next_sequence['outbound'])
        indexA = self.next_sequence[truck_type].index(a)
        indexB = self.next_sequence[truck_type].index(b)
        self.next_sequence[truck_type][indexA] = b
        self.next_sequence[truck_type][indexB] = a
        self.next_sequence['error'] = 0

        logging.info("Random1 next sequence inbound: {0}".format(self.next_sequence['inbound']))
        logging.info("Random1 next sequence outbound: {0}".format(self.next_sequence['outbound']))
        self.sequences['current'].inbound_sequence = self.next_sequence['inbound']
        self.sequences['current'].outbound_sequence = self.next_sequence['outbound']
        self.sequences['current'].error = 0

    def generate_random(self, sequence):
        a = random.choice(sequence)
        b = random.choice(sequence)
        if a == b:
            a, b = self.generate_random(sequence)
        if isinstance(a, int) and isinstance(b, int):
            a, b = self.generate_random(sequence)
        return a, b

    def annealing1(self):
        if self.sequences['current'].error <= self.sequences['prev'].error:
            self.sequences['prev'] = Sequence(self.sequences['current'].inbound_sequence, self.sequences['current'].outbound_sequence)
            self.sequences['prev'].error = self.sequences['current'].error
            if self.sequences['current'].error < self.sequences['best'].error:
                self.sequences['best'] = Sequence(self.sequences['current'].inbound_sequence, self.sequences['current'].outbound_sequence)
                self.sequences['best'].error = self.sequences['current'].error
            logging.info("current error {0}, best error {1}, prev error {2}".format(self.sequences['current'].error, self.sequences['best'].error , self.sequences['prev'].error ))
        else:
            p_accept = math.exp((self.sequences['prev'].error - self.sequences['current'].error) / self.temperature)
            logging.info("p current error {0}, prev error {1}, temperature {2}".format(self.sequences['current'].error, self.sequences['prev'].error, self.temperature))
            logging.info("p accept {0}".format(p_accept))
            if p_accept >= random.random():
                logging.info("p accepted")
                self.sequences['prev'] = Sequence(self.sequences['current'].inbound_sequence, self.sequences['current'].outbound_sequence)
                self.sequences['prev'].error = self.sequences['current'].error

        self.temperature = self.temperature_reduction_rate * self.temperature