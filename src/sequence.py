__author__ = 'mustafa'

class Sequence(object):
    """
    sequence class that stores sequences
    """
    def __init__(self, inbound, outbound):
        self.inbound_sequence = inbound
        self.outbound_sequence = outbound
        self.error = 0
