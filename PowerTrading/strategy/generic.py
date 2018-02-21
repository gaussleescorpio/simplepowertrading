"""
This is the generic strategy template
"""

from abc import ABC


class GenericAbstractStrategy(ABC):
    def __init__(self, strategy_name, order_manager):
        """
        :param strategy_name: strategt name
        :param order_manager: order manager object
        """
        self.order_manager = order_manager
        self.strategy_name = strategy_name

    def OnTick(self):
        return NotImplemented

    def OnBar(self, event):
        return NotImplemented

    def send_order(self):
        return NotImplemented

    def cancel_order(self):
        return NotImplemented

    def OnOrder(self):
        return NotImplemented

    def OnTrade(self):
        return NotImplemented


class GenericStrategy(GenericAbstractStrategy):
    def __init__(self, str_name, order_manger):
        super(GenericStrategy, self).__init__(str_name, order_manger)

    def OnBar(self, event):
        print(event)

    def OnTick(self, event):
        print(event)










