from PowerTrading.events.event import TeminateEvent, BarEvent
import pandas as pd
import time


class GenericEventFeeder(object):
    pass


class GenericDFBarEventFeeder(GenericEventFeeder):
    """
    This class is used to wrap a dataframe as a data feeder to the event engine
    """
    def __init__(self, df, ticker, event_engine, flexible=False):
        assert hasattr(event_engine, "register_strategy"), "Not a valid event engine"
        assert isinstance(df, pd.DataFrame), "Not a valid df source"
        self.event_engine = event_engine
        self.ticker = ticker
        self.active = True
        self.data = df
        self.iterator = df.iterrows()
        self.flexible = flexible

    def __iter__(self):
        return self

    def __next__(self):
        try:
            row_data = next(self.iterator)
            row_dict = row_data[1].to_dict()
            bar_event = BarEvent(row_dict, ticker=self.ticker, flexile=self.flexible)
            return bar_event
        except StopIteration:
            raise StopIteration("End of data")

    def stream_data(self):
        """
        Stream the data and push into the event queue
        :return:
        """
        while self.active:
            try:
                event = next(self)
                self.event_engine.insert_event(event)
            except StopIteration:
                self.active = False
                # self.event_engine.insert_event(TeminateEvent())


if __name__ == "__main__":
    import pandas as pd
    from PowerTrading.events.event_engine import StandardEventEngine
    from PowerTrading.strategy.generic import GenericStrategy
    df = pd.DataFrame(columns=["time", "high", "low",
                               "open", "close", "adj_close",
                               "volume"])
    df["time"] = pd.date_range("2014-02-01", "2018-03-01")
    df = df.fillna(0)
    print(df)
    eve_engine = StandardEventEngine()
    data_feeder = GenericDFBarEventFeeder(df, "sym1", eve_engine, False)
    sim_strat = GenericStrategy("test", None)
    print(hasattr(sim_strat, "OnBar"))
    eve_engine.register_strategy(sim_strat, sim_strat.strategy_name)
    eve_engine.start()
    print(eve_engine.strategy_bucket)
    data_feeder.stream_data()


















