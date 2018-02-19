from threading import Thread
from queue import Queue, Empty
from collections import defaultdict
import warnings
from PowerTrading.events.event import EventType


class StandardEventEngine(object):
    """
    The most standard event engine using a main streaming loop with an extra
    event handling thread
    """
    def __init__(self):
        # setup the event Queue
        self._event_queue = Queue()

        # setup the switch
        self._on = False

        # event handling thread
        self._event_thread = Thread(target=self._run)

        # strategy bucket
        self.strategy_bucket = defaultdict()

        # customerized event-function bucket
        self.custom_bucket = defaultdict()

    def _run(self):
        while self._on:
            try:
                event = self._event_queue.get(block=True, timeout=1)
                self._process(event)
            except Empty:
                pass

    def _process(self, event):
        # check if the event type is standard or not
        if EventType.has_event(event.type):
            if event.type == "BarEvent":
                [strategy.OnBar(event) for strategy in self.strategy_bucket if hasattr(strategy, "OnBar")]
            elif event.type == "TickEvent":
                [strategy.OnTick(event) for strategy in self.strategy_bucket if hasattr(strategy, "OnTick")]
            else:
                warnings.warn("cannot handle this event %s" % event.type)
        else:
            for new_env in self.custom_bucket:
                [handler(new_env) for handler in self.custom_bucket[new_env]]

    def start(self):
        self._on = True
        self._event_thread.start()

    def stop(self):
        """
        used to stop the whole event engine
        """
        self._on = False
        self._event_thread.join()

    def register_strategy(self, strategy, name):
        """
        A strategy is a class which at least includes OnBar or OnTick method.
        :param strategy: a strategy calss
        :return:
        """
        if hasattr(strategy, "OnBar"):
            pass
        elif hasattr(strategy, "OnTick"):
            pass
        else:
            raise ValueError("Invalid strategy")
        assert isinstance(name, str), "strategy name must be string"
        if name in self.strategy_bucket:
            raise KeyError("%s strategy already registered")
        self.strategy_bucket[name] = strategy

    def unregister_strategy(self, name):
        """
        remove the strategy with specified name
        :param name:
        :return:
        """
        assert isinstance(name, str), "target strategy name must be string"
        if name in self.strategy_bucket:
            self.strategy_bucket.pop(name)

    def register_custom_func(self, event, func):
        """
        register the user-defined event and its handler
        :param event:
        :param func:
        :return:
        """
        if event in self.custom_bucket:
            self.custom_bucket[event].append(func)
        else:
            self.custom_bucket[event] = [func]

    def unregister_custom_func(self, event, func):
        """
        unregister the user-defined event and its handler
        :param event:
        :param func:
        :return:
        """
        try:
            self.custom_bucket[event].remove(func)
        except ValueError:
            warnings.warn("cannot delete unregistered func")

    def insert_event(self, event):
        self._event_queue.put(event)