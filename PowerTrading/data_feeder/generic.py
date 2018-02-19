from PowerTrading.events import event_engine
from PowerTrading.events import event
import pandas as pd


class GenericEventFeeder(object):
    pass


class GenericDFBarEventFeeder(GenericEventFeeder):
    """
    This class is used to wrap a dataframe as a data feeder to the event engine
    """
    def __init__(self, df, event_engine):
        assert hasattr(event_engine, "register_strategy"), "Not a valid event engine"
        assert isinstance(df, pd.DataFrame), "Not a valid df source"
        self.iterator = df.iterrows()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            row_data = next(self.iterator)
            row_dict = row_data.to_dict(orient="records")
            bar_event = event.BarEvent(row_dict)
        except Exception:







