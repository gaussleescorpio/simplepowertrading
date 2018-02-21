from PowerTrading.backtest_engine import BacktestEngine
from PowerTrading.data_feeder.generic import GenericDFBarEventFeeder
from PowerTrading.events.event_engine import StandardEventEngine
from PowerTrading.strategy.ctaexamplestrategy import CtaSimpleStrategy
from PowerTrading.order_manager import SimOrderManager
import pandas as pd
from matplotlib import pylab as plt

if __name__ == "__main__":
    data = pd.read_csv("/home/gausslee/Documents/test_data.csv")
    data = data.rename(columns={"date": "time"})
    data["adj_close"] = data["close"]
    data.sort_index(ascending=False, inplace=True)
    ee = StandardEventEngine()
    data_feeder = GenericDFBarEventFeeder(df=data, ticker="test_symbol",
                                          event_engine=ee, flexible=True)
    ord_man = SimOrderManager(ticker_list=["test_symbol"])
    strat = CtaSimpleStrategy("test_strat", ord_man)
    bbe = BacktestEngine(data_feeder, ee, strat)
    bbe.start_backtesting()
    bbe.wait_until_stop()
    bbe.results_analysis_single_df()
    print(ord_man.ticker_order_recorder["test_symbol"])
    plt.show()
