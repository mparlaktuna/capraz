from src.good_store import GoodStore
from copy import deepcopy

import logging


class ShippingDoor(object):
    """
    Shipping doors of the station
    """
    def __init__(self, station, name):
        self.station = station
        self.door_name = name
        self.trpe = 'Shipping'
        self.truck = None
        self.status = ['empty', 'loading', 'waiting']
        self.status_number = 0
        self.good_list = GoodStore()
        self.sequence = []
        self.station = station
        self.waiting_trucks = 0
        self.loading_truck = None
        self.reserved_goods = GoodStore()
        self.finish_time = 0
        self.current_time = 0

    def set_truck_doors(self):
        for truck in self.sequence:
            truck.shipping_door = self
            truck.shipping_door_name = self.door_name

    def current_action(self, current_time):
        self.current_time = current_time
        logging.debug("Reserved goods: {0}".format(self.reserved_goods))
        if self.status_number == 0:
            self.no_truck()
        if self.status_number == 1:
            self.load()
        if self.status_number == 2:
            self.wait_truck_change()

    def next_state(self):
        self.status_number += 1

    def no_truck(self):
        if len(self.sequence) != 0:
            self.loading_truck = self.sequence[0]
            if self.loading_truck.state_list[self.loading_truck.current_state] == 'waiting_to_load':
                self.loading_truck.next_state()
                self.next_state()

    def check_goods(self):
        """
        check if enough in reserved goods
        :return:
        """
        logging.debug("---Check Goods")
        logging.debug("---Reserved goods:")
        for reserved_good in self.reserved_goods.good_list:
            logging.debug("Amount of reserved {0} : {1}".format(reserved_good, self.reserved_goods.total_good(reserved_good)))

        logging.debug("---Station goods:")
        for station_good in self.station.station_goods.good_list:
            logging.debug("Amount in station{0} : {1}".format(station_good, self.station.station_goods.total_good(station_good)))

        enough_goods = True
        for good_name, good_amount in self.loading_truck.going_good_amounts.items():
            good_name = str(good_name)
            if good_amount == self.reserved_goods.total_good(good_name):
                logging.debug('Good {0} ready'.format(good_name))
            else:
                enough_goods = enough_goods and False

        if enough_goods:
            logging.debug('Enough goods')
        return enough_goods

    def reserve_goods(self, good_amounts):
        """
        reserve goods
        :param good_amounts:
        :return:
        """
        logging.debug("---Reserve Goods")
        for good_name, needed_good_amount in good_amounts.items():
            good_name = str(good_name)
            logging.debug("Good name: {0}".format(good_name))
            logging.debug("Needed amount: {0}".format(needed_good_amount))
            if good_name in self.station.station_goods.good_list:
                logging.debug("Good in station: {0}".format(good_name))
                if good_name in self.reserved_goods.good_list.keys():
                    logging.debug("Good reserved before: {0}".format(good_name))
                    needed_good_amount = needed_good_amount - self.reserved_goods.total_good(good_name)
                logging.debug("needed amount {0}: {1}".format(good_name, needed_good_amount))

                if needed_good_amount == 0:
                    continue
                moved_amount = self.station.station_goods.move_good(good_name, needed_good_amount)
                needed_good_amount -= moved_amount
                self.reserved_goods.add_good(good_name, moved_amount)

    def reserve_critical_goods(self, good_amounts):
        self.reserve_goods(good_amounts)
        if self.check_goods():
            return
        else:
            for good_name, needed_good_amount in good_amounts.items():
                good_name = str(good_name)
                if good_name in self.reserved_goods.good_list:
                    needed_good_amount -= self.reserved_goods.total_good(good_name)
                    if needed_good_amount == 0:
                        continue

                moved_amount = 0

                for shipping_door in self.station.shipping_doors.values():
                    if shipping_door == self:
                        break
                    if needed_good_amount == 0:
                        break

                    if good_name in shipping_door.reserved_goods.good_list:
                        moved_amount += shipping_door.reserved_goods.move_good(good_name, needed_good_amount)

                if moved_amount == 0:
                    return

                self.reserved_goods.add_good(good_name, moved_amount)

    def wait_truck_change(self):
        if self.current_time == self.finish_time:
            self.status_number = 0

    def load_goods(self, current_time):
        self.current_time = current_time
        self.loading_truck.going_goods = deepcopy(self.reserved_goods)
        self.reserved_goods = GoodStore()
        self.next_state()
        self.finish_time = current_time + self.loading_truck.changeover_time
        if self.sequence:
            self.sequence.pop(0)

    def load(self):
        pass # wait for truck


