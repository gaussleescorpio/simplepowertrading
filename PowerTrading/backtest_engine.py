import pandas as pd
from PowerTrading.events.event_engine import StandardEventEngine
from PowerTrading.strategy.generic import GenericStrategy
from PowerTrading.statistics import BacktestStat


class BacktestEngine(object):
    def __init__(self, data_feeder,
                 event_engine, strategy):
        self.d_feeder = data_feeder
        self.ee = event_engine
        self.strat = strategy
        self.ee.register_strategy(strategy, strategy.strategy_name)

    def start_backtesting(self):
        self.ee.start()
        self.d_feeder.stream_data()

    def wait_until_stop(self):
        self.ee.wait_until_stop()

    def results_analysis_single_df(self):
        ret_data = self.d_feeder.data[["time", "close"]].copy()
        trading_signal = pd.DataFrame(self.strat.order_manager.ticker_order_recorder[self.d_feeder.ticker],
                                      columns=["time", "position", "price", "order_size"])
        ret_data["time"] = pd.to_datetime(ret_data["time"])
        trading_signal["time"] = pd.to_datetime(trading_signal["time"])
        # print(trading_signal)
        data = pd.merge(ret_data, trading_signal, on="time", how="outer").reset_index(drop=True)
        # print(data)
        data["position"] = data["position"].fillna(0)
        data.loc[data["price"].isnull(), "price"] = data["close"]
        data["order_size"] = data["order_size"].fillna(0)
        data = data.dropna(axis=1)
        data.set_index("time", drop=True, inplace=True)
        # print(data[data["position"]!=0].index.max())
        # print(data[data["position"]!=0].index.min())
        bt_ret = BacktestStat(price=data["price"], signal=data["position"]*data["order_size"], signalType="shares")
        bt_ret.plotTrades()









