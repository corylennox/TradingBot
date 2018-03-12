from poloniex import poloniex
import time
from botcandlestick import BotCandlestick


class BotChart(object):
    def __init__(self, pair, period, endTime, startTime, backtest=True):
        self.pair = pair
        self.period = period
        self.endTime = endTime
        self.startTime = startTime
        self.data = []


        self.conn = poloniex('key goes here', 'Secret goes here')

        if backtest:
            poloData = self.conn.api_query("returnChartData",
                                           {"currencyPair": self.pair, "start": self.startTime - 12 * 900, "end": self.endTime,
                                            "period": self.period})
            for datum in poloData:
                if datum['open'] and datum['close'] and datum['high'] and datum['low'] and datum['date']:
                    self.data.append(
                        BotCandlestick(self.period, datum['open'], datum['close'], datum['high'], datum['low'],
                                       datum['weightedAverage'], datum['date']))

    def getPoints(self):
        return self.data

    def getCurrentPrice(self):
        currentValues = self.conn.api_query("returnTicker")
        lastPairPrice = {}
        lastPairPrice = currentValues[self.pair]["last"]
        return lastPairPrice