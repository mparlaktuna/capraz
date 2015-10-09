from src.good import Good
import logging


class GoodStore(object):
    def __init__(self):
        self.good_list = {}
        self.total_goods = 0

    def remove_good(self, good_type):
        """ create exception """
        del self.good_list[good_type]

    def remove_all_goods(self):
        self.good_list = {}

    def calculate_total(self, type):
        pass

    def check_zero_goods(self):
        for good_type in self.good_list.keys():
            for good in self.good_list[good_type]:
                if good.amount == 0:
                    self.good_list[good_type].remove(good)
                if good.amount < 0:
                    logging.debug("error amount below zero {0}".format(good_type))
            if not self.good_list:
                self.remove_good(good_type)

    def total(self):
        total = 0
        for goods in self.good_list.values():
            for good in goods:
                total += good.amount
        return total

    def total_good(self, good_type):
        total = 0
        if good_type in self.good_list:
            for good in self.good_list[good_type]:
                total += good.amount
        return total

    def add_good(self, good_type, amount):
        if good_type in self.good_list:
            new_good = Good(good_type, amount)
            self.good_list[good_type].append(new_good)
        else:
            new_good = Good(good_type, amount)
            self.good_list[good_type] = [new_good]

    def move_good(self, good_type, amount):
        self.check_zero_goods()
        moved_amount = 0
        if good_type in self.good_list:
            for good in self.good_list[good_type]:
                if good.amount >= amount:
                    logging.debug('Good {0} enough'.format(good_type))
                    good.amount -= amount
                    moved_amount += amount
                    amount = 0
                elif good.amount < amount:
                    moved_amount += good.amount
                    amount -= moved_amount
                    good.amount = 0
                    logging.debug('Good {0} not enough to reserve, moved {1}'.format(good_type, moved_amount))
            self.check_zero_goods()
            logging.debug('Good {0} moved total {1}'.format(good_type, moved_amount))
        return moved_amount

    def log_goods(self):
        for good_name in self.good_list.keys():
            logging.debug('Good name {0}, amount {1}'.format(good_name, self.total_good(good_name)))


