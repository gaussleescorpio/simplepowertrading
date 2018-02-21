"""
This is order manager which is in charge of sending, recording and cancelling order.
"""

from collections import defaultdict
import logging


class AbstractOrderManager(object):
    def send_order(self, *args, **kwargs):
        return NotImplemented

    def cancel_order(self, *args, **kwargs):
        return NotImplemented


class SimOrderManager(AbstractOrderManager):
    def __init__(self, ticker_list=[]):
        self.ticker_order_recorder = defaultdict()
        self.investory_size = 0
        for ticker in ticker_list:
            self.ticker_order_recorder[ticker] = []

    def send_order(self, position, price, order_size, ticker, time):
        """
        :param position: 1 or -1 represents buy or sell
        :param price:
        :param order_size:
        :param ticker:
        :param time:
        :return:
        """
        if ticker in self.ticker_order_recorder:
            self.ticker_order_recorder[ticker].append([time, position, price, order_size])
            self.investory_size += position
        else:
            logging.warning("This order for %s cannot be settled, it is not in the ticker list" % ticker)



