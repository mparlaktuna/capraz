import logging

class Sequence(object):
    """
    sequence class that stores sequences
    """
    def __init__(self, inbound = list(), outbound = list()):
        self.inbound_sequence = inbound
        self.outbound_sequence = outbound
        self.error = 0

    def print_sequence(self):
        logging.info("Inbound: {0}".format(self.inbound_sequence))
        logging.info("Outbound: {0}".format(self.outbound_sequence))
        logging.info("Error: {0}".format(self.error))

