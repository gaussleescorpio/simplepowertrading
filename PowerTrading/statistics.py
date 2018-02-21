import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class BacktestStat(object):
    """
    Backtest class, simple vectorized one. Works with pandas objects.
    """

    def __init__(self, price, signal, signalType='capital', initialCash=0, roundShares=True):
        """
        Arguments:
        *price*  Series with instrument price.
        *signal* Series with capital to invest (long+,short-) or number of shares.
        *sitnalType* capital to bet or number of shares 'capital' mode is default.
        *initialCash* starting cash.
        *roundShares* round off number of shares to integers
        """
        # check for correct input
        assert signalType in ['capital', 'shares'], "Wrong signal type provided, must be 'capital' or 'shares'"

        # save internal settings to a dict
        self.settings = {'signalType': signalType}

        # first thing to do is to clean up the signal, removing nans and duplicate entries or exits
        self.signal = signal.ffill().fillna(0)

        # now find dates with a trade
        tradeIdx = self.signal.fillna(0) != 0  # days with trades are set to True
        if signalType == 'shares':
            self.trades = self.signal[tradeIdx]  # selected rows where tradeDir changes value. trades are in Shares
        elif signalType == 'capital':
            self.trades = (self.signal[tradeIdx] / price[tradeIdx])
            if roundShares:
                self.trades = self.trades.round()

        # now create internal data structure
        self.data = pd.DataFrame(index=price.index, columns=['price', 'shares', 'value', 'cash', 'pnl'])
        self.data['price'] = price

        self.data['shares'] = self.trades.reindex(self.data.index).fillna(0)
        self.data['value'] = self.data['shares'].cumsum() * self.data['price']

        delta = self.data['shares']  # shares bought sold

        self.data['cash'] = (-delta * self.data['price']).fillna(0).cumsum() + initialCash
        self.data['pnl'] = self.data['cash'] + self.data['value'] - initialCash
        self.data['total_shares'] = self.data['shares'].cumsum()

    @property
    def sharpe(self):
        ''' return annualized sharpe ratio of the pnl '''
        pnl = (self.data['pnl'].diff()).shift(-1)[self.data['shares'] != 0]  # use only days with position.
        return sharpe(pnl)  # need the diff here as sharpe works on daily returns.

    @property
    def odd_sharpe(self):
        profit = self.pnl.iloc[-1]
        max_dd = self.pnl.cummax()
        min_dd = self.pnl - max_dd
        min_dd = min_dd.cummin().min()
        if min_dd == 0:
            return 0
        return profit / min_dd

    @property
    def pnl(self):
        '''easy access to pnl data column '''
        return self.data['pnl']

    def plotTrades(self):
        """
        visualise trades on the price chart
            long entry : green triangle up
            short entry : red triangle down
            exit : black circle
        """
        figs, axes = plt.subplots(3, 1, sharex=True)
        l = ['price']

        p = self.data['price']
        p.plot(style='x-', subplots=True, ax=axes[0])

        # ---plot markers
        # this works, but I rather prefer colored markers for each day of position rather than entry-exit signals
        #         indices = {'g^': self.trades[self.trades > 0].index ,
        #                    'ko':self.trades[self.trades == 0].index,
        #                    'rv':self.trades[self.trades < 0].index}
        #
        #
        #         for style, idx in indices.iteritems():
        #             if len(idx) > 0:
        #                 p[idx].plot(style=style)

        # --- plot trades
        # colored line for long positions
        print(self.data["shares"])
        idx = (self.data['shares'] > 0) #| (self.data['shares'] > 0).shift(1)
        if idx.any():
            p[idx].plot(style='go', subplots=True, ax=axes[0])
            l.append('long')

        # colored line for short positions
        idx = (self.data['shares'] < 0) #| (self.data['shares'] < 0).shift(1)
        if idx.any():
            p[idx].plot(style='ro', subplots=True, ax=axes[0])
            l.append('short')

        axes[0].set_xlim([p.index[0], p.index[-1]])  # show full axis

        axes[0].legend(l, loc='best')
        axes[0].set_title('trades')

        pnl = self.data["pnl"]
        pnl.plot(style='o-', subplots=True, ax=axes[1])
        axes[1].set_title("PNL PLOT")

        shares = self.data["total_shares"]
        shares.plot(style='o-', subplots=True, ax=axes[2])
        axes[2].set_title("TOTAL_SHARES")


def sharpe(pnl):
    if pnl.std() == 0.0:
        return 0.0
    return np.sqrt(250) * pnl.mean() / pnl.std()


def odd_sharpe(pnl):
    profit = pnl.iloc[-1]
    max_dd = pnl.cummax()
    min_dd = pnl - max_dd
    min_dd = min_dd.cummin().min()
    if min_dd == 0:
        return 0
    return profit / abs(min_dd)
