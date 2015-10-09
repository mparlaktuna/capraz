__author__ = 'mustafa'

class Good(object):
    """
    good object
    """
    def __init__(self, good_type, amount):
        """
        initialize type, number and truck numbers
        :return:
        """
        self.type = str(good_type)
        self.amount = amount
        self.transfer_time = 0
        self.coming_truck_name = None
        self.going_truck_name = None