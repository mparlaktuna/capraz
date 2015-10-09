__author__ = 'robotes'

from src.receiving_door import ReceivingDoor
from src.shipping_doors import ShippingDoor
import itertools
import logging

class Station(object):
    """
    Station for the goods to come in and go out.
    """
    def __init__(self, transfer_time):
        """
        Initialize the station by creating doors and types
        :return:
      """

        self.receiving_doors = {}
        self.shipping_doors = {}
        self.not_ready_goods = {}
        self.station_goods = {}
        self.good_transfer_time = transfer_time

    def add_receiving_door(self):
        """
        creates a receiving door
        :return:
        """
        name = 'recv' + str(len(self.receiving_doors))
        door = ReceivingDoor(self, name)
        self.receiving_doors[name] = door

    def clear_door_sequences(self):
        for doors in itertools.chain(self.receiving_doors.values(), self.shipping_doors.values()):
            doors.sequence = []

    def remove_receiving_door(self):
        """
        removes a receiving door from the station
        :return:
        """
        name = 'recv' + str(len(self.receiving_doors)-1)
        del self.receiving_doors[name]

    def add_shipping_door(self):
        """
        creates a shipping door
        :return:
        """
        name = 'ship' + str(len(self.shipping_doors))
        door = ShippingDoor(self, name)
        self.shipping_doors[name] = door

    def remove_shipping_door(self):
        """
        removes a receiving door from the station
        :return:
        """
        name = 'ship' + str(len(self.shipping_doors)-1)
        del self.shipping_doors[name]

    def check_states(self):
        logging.debug("station goods")
        for goods in self.station_goods.values():
            for good in goods:
                logging.debug("type: {0}, amount: {1}".format(good.type, good.amount))

        for doors in itertools.chain(self.receiving_doors.values()):
            if doors.good_list:
                self.add_goods(doors.good_list)

    def add_goods(self, goods, current_time):
        for good in goods:
            good.transfer_time = current_time + self.good_transfer_time
            if good.type in self.not_ready_goods.keys():
                self.not_ready_goods[good.type].append(good)
            else:
                self.not_ready_goods[good.type] = []
                self.not_ready_goods[good.type].append(good)
        #     if good.type in self.not_ready_goods.keys():
        #         self.not_ready_goods[good.type].append(good)
        #     else:
        #         self.not_ready_goods[good.type] = []
        #         self.not_ready_goods[good.type].append(good)

    def check_good_transfer(self, current_time):
        """
        check if goods are ready to transfer
        :return:
        """
        for goods in self.not_ready_goods.values():
            for good in goods:
                if good.transfer_time == current_time:
                    if good.type in self.station_goods.keys():
                        self.station_goods[good.type].append(good)
                    else:
                        self.station_goods[good.type] = []
                        self.station_goods[good.type].append(good)
                    total_good = 0
                    logging.debug("Station: Unloading goods from truck")
                    self.log_goods()

    def log_goods(self):
        total_good = 0
        for good_type in self.station_goods.values():
            for good_amounts in good_type:
                total_good +=  good_amounts.amount
            # logging.debug("--Station: good type:{0}, amount:{1}".format(good_type[0].type, total_good))

    def remove_goods(self, goods):
        for good in goods:
            max_item = None
            moved_good = 0
            error = good.amount - moved_good
            while error > 0 :
                for items in self.station_goods[good.type]:
                    next_item = items
                    if max_item is None or max_item.amount < next_item.amount:
                        max_item = next_item
                if max_item.amount < error:
                    moved_good += max_item.amount
                    max_item.amount = 0
                elif max_item.amount >= error:
                    moved_good += error
                    max_item.amount -= error
                error = good.amount - moved_good
        logging.debug("Station: Loading goods to truck")
        self.log_goods()
