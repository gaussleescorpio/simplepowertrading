from PowerTrading.strategy.generic import GenericStrategy


class CtaSimpleStrategy(GenericStrategy):
    def __init__(self, name, ord_man):
        super(CtaSimpleStrategy, self).__init__(name, ord_man)

    def OnBar(self, event):
        if event.ma5 > event.ma10 and self.order_manager.investory_size <= 0:
            self.order_manager.send_order(1, event.close, 10,
                                          event.ticker, event.time)
        elif event.ma5 < event.ma10 and self.order_manager.investory_size > 0:
            self.order_manager.send_order(-1, event.close, 10,
                                          event.ticker, event.time)

