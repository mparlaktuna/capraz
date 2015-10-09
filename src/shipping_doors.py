__author__ = 'robotes'
import logging

from src.good import Good
from copy import deepcopy

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
        self.good_list = []
        self.sequence = []
        self.station = station
        self.waiting_trucks = 0
        self.loading_truck = None
        self.reserved_goods = {}
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
        for reserved_good in self.reserved_goods.values():
            for good in reserved_good:
                logging.debug("{0} : {1}".format(good.type, good.amount))

        logging.debug("---Station goods:")
        for station_good in self.station.station_goods.values():
            for good in station_good:
                logging.debug("{0} : {1}".format(good.type, good.amount))

        enough_goods = False
        for good_name, good_amount in self.loading_truck.going_good_amounts.items():
            total = 0
            good_name = str(good_name)
            logging.debug("Checking amount ")
            if good_name in self.reserved_goods.keys():
                enough_goods = True
                for reserved_good in self.reserved_goods[good_name]:
                    total += reserved_good.amount
                logging.debug("Total good in station {0}".format(total))
                logging.debug("Needed goods {0}".format(good_amount))
                if good_amount > total:
                    enough_goods = False
                logging.debug("Enough goods {0}".format(enough_goods))
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
            if good_name in self.station.station_goods.keys():
                logging.debug("Good in station: {0}".format(good_name))
                station_goods =  self.station.station_goods[good_name]
                if good_name in self.reserved_goods.keys():
                    logging.debug("Good reserved before: {0}".format(good_name))
                    for reserved_good in self.reserved_goods[good_name]:
                        needed_good_amount = needed_good_amount - reserved_good.amount
                logging.debug("needed amount {0}: {1}".format(good_name, needed_good_amount))

                if needed_good_amount == 0:
                    continue
                logging.debug("station goods {0}".format(station_goods))
                deleted_indices = []
                for i, station_good in enumerate(station_goods):
                    logging.debug('loop number: {}'.format(i))
                    if needed_good_amount == 0:
                        logging.debug('break')
                        break

                    transfered_good_amount = 0
                    if station_good.amount > needed_good_amount:
                        logging.debug("needed less")
                        station_good.amount = station_good.amount - needed_good_amount
                        transfered_good_amount = needed_good_amount
                        needed_good_amount = 0

                    elif station_good.amount == needed_good_amount:
                        logging.debug("needed equal")
                        transfered_good_amount = needed_good_amount
                        logging.debug("needed amount {0}: {1}".format(good_name, station_good.amount))
                        deleted_indices.append(i)
                        needed_good_amount = 0

                    elif station_good.amount < needed_good_amount:
                        logging.debug("needed greater")
                        transfered_good_amount = station_good.amount
                        needed_good_amount = needed_good_amount - station_good.amount
                        logging.debug("station amount {0}: {1}".format(good_name, station_good.amount))
                        logging.debug("needed amount {0}: {1}".format(good_name, needed_good_amount))
                        deleted_indices.append(i)

                    logging.debug("station goods 2 {0}".format(station_goods))
                    new_good = Good(good_name, transfered_good_amount)

                    logging.debug("transferred amount :{0}".format(transfered_good_amount))
                    if good_name in self.reserved_goods.keys():
                        self.reserved_goods[good_name].append(new_good)
                    else:
                        self.reserved_goods[good_name] = []
                        self.reserved_goods[good_name].append(new_good)

                self.station.station_goods[good_name] = [m for n, m in enumerate(station_goods) if n not in deleted_indices]
                logging.debug("station goods 3 {0}".format(station_goods))



    def reserve_critical_goods(self, good_amounts):
        self.reserve_goods(good_amounts)
        if self.check_goods():
            return
        else:
            for good_name, needed_good_amount in good_amounts.items():
                good_name = str(good_name)
                if good_name in self.reserved_goods.keys():
                    for reserved_goods in self.reserved_goods.values():
                        for reserved_good in reserved_goods:
                            needed_good_amount = needed_good_amount - reserved_good.amount
                    if needed_good_amount == 0:
                        continue

                transfered_good_amount = 0

                for shipping_door in self.station.shipping_doors.values():
                    if needed_good_amount == 0:
                        break

                    if good_name in shipping_door.reserved_goods.keys():
                        other_reserved_goods = shipping_door.reserved_goods[good_name]
                        for i, other_reserved_good in enumerate(other_reserved_goods):
                            if other_reserved_good.amount > needed_good_amount:
                                other_reserved_good.amount = other_reserved_good.amount - needed_good_amount
                                needed_good_amount = 0
                                transfered_good_amount = needed_good_amount

                            elif other_reserved_good.amount == needed_good_amount:
                                transfered_good_amount = needed_good_amount
                                needed_good_amount = 0
                                other_reserved_goods.pop(i)

                            elif other_reserved_good.amount < needed_good_amount:
                                transfered_good_amount = other_reserved_good.amount
                                needed_good_amount = needed_good_amount - other_reserved_good.amount
                                other_reserved_goods.pop(i)

                if transfered_good_amount == 0:
                    return

                new_good = Good(good_name, transfered_good_amount)
                if good_name in self.reserved_goods.keys():
                    self.reserved_goods[good_name].append(new_good)
                else:
                    self.reserved_goods[good_name] = []
                    self.reserved_goods[good_name].append(new_good)

    def wait_truck_change(self):
        if self.current_time == self.finish_time:
            self.status_number = 0

    def load_goods(self, current_time):
        self.current_time = current_time
        self.loading_truck.going_goods = deepcopy(self.reserved_goods)
        self.reserved_goods = {}
        self.next_state()
        self.finish_time = current_time + self.loading_truck.changeover_time
        if self.sequence:
            self.sequence.pop(0)

    def load(self):
        pass # wait for truck


