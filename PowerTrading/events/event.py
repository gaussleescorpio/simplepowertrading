"""
This file contains the fundamental types of events
"""

from abc import ABC, abstractmethod
from enum import Enum
import logging


class EventType(Enum):
    BarEvent = 0
    TickEvent = 1

    @classmethod
    def has_event(cls, name):
        return any(name == item.name for item in cls)


class Event(ABC):
    def __init__(self, type=None):
        self.type = type.name

    @abstractmethod
    def _create_event(self, data):
        return NotImplemented


class BarEvent(Event):
    def __init__(self, data, ticker):
        super().__init__(type=EventType.BarEvent)
        assert isinstance(data, dict), "data must be dict to create an event"
        self._create_event(data)
        self.ticker = ticker

    def _create_event(self, data):
        try:
            self.time = data["time"]
            self.high = data["high"]
            self.low = data["low"]
            self.open = data["open"]
            self.close = data["close"]
            self.adj_close = data["adj_close"]
            self.volume = data["volume"]
        except KeyError as e:
            logging.debug("input data format is wrong: %s" % str(e))
            raise ValueError("data format is wrong, not a valid bar data format")

    def __repr__(self):
        return str(self)

    def __str__(self):
        format_str = """Ticker name: %s High: %s, Open: %s,
                        Low: %s, Close: %s, adj_close: %s,
                        Volume: %s, Time: %s""" %(self.ticker,
                                                  self.high,
                                                  self.open,
                                                  self.low,
                                                  self.close,
                                                  self.adj_close,
                                                  self.volume,
                                                  self.time)
        return format_str


class TickEvent(Event):
    def __init__(self, data, ticker, level=1):
        super().__init__(type=EventType.TickEvent)
        assert isinstance(data, dict), "data must be dict to create an event"
        self._create_event(data)
        self.ticker = ticker
        self.level = level

    def _create_event(self, data):
        try:
            self.time = data["time"]
            for i in range(self.level):
                setattr(self, "Ask%s" % str(i + 1), data["Ask%s" % str(i + 1)])
                setattr(self, "Bid%s" % str(i + 1), data["Bid%s" % str(i + 1)])
                setattr(self, "Ask%s_Size" % str(i + 1), data["Ask%s_Size" % str(i + 1)])
                setattr(self, "Bid%s_size" % str(i + 1), data["Bid%s_Size" % str(i + 1)])
        except KeyError:
            raise ValueError("check the assigned data if it is a tick data")

    def __repr__(self):
        return str(self)

    def __str__(self):
        format_str = """Ticker: %s at time: %s,
                        Best_Ask: %s, BAsk_Size: %s,
                        Best_Bid: %s, BBid_Size: %s""" % (self.ticker, self.time,
                                                          self.Ask1,
                                                          self.Ask1_Size,
                                                          self.Bid1,
                                                          self.Bid1_Size)
        return format_str
