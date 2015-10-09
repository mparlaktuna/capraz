__author__ = 'robotes'

class ReceivingDoor(object):
    """
    Receiving doors of the station
    """
    def __init__(self,station, name):
        self.door_name = name
        self.type = 'Receiving'
        self.door_number = 0
        self.truck = 0
        self.truck_sequence = 0
        self.status = ['empty', 'deploying', 'waiting']
        self.status_number = 0
        self.good_list = []
        self.sequence = []
        self.station = station
        self.waiting_trucks = 0
        self.deploying_truck = None
        self.finish_time = 0
        self.current_time = 0

    def set_truck_doors(self):
        for truck in self.sequence:
            truck.receiving_door = self
            truck.receiving_door_name = self.door_name

    def current_action(self, current_time):
        self.current_time = current_time
        if self.status_number == 0:
            self.no_truck()
        if self.status_number == 1:
            self.deploying()
        if self.status_number == 2:
            self.wait_truck_change()

    def next_state(self):
        self.status_number += 1

    def wait(self):
        pass

    def no_truck(self):
        if len(self.sequence) != 0:
            next_truck = self.sequence[0]
            self.deploying_truck = next_truck
            if next_truck.state_list[next_truck.current_state] == 'waiting':
                self.sequence[0].next_state()
                self.next_state()

    def wait_truck_change(self):
        if self.current_time == self.finish_time:
            self.status_number = 0

    def deploy_goods(self, goods, current_time):
        self.current_time = current_time
        self.station.add_goods(goods, current_time)
        self.finish_time = current_time + self.deploying_truck.changeover_time
        self.next_state()
        self.sequence.pop(0)

    def deploying(self):
        pass # wait for truck

