from poloniex import poloniex
import time
from botcandlestick import BotCandlestick

class LiveBotChart(object):
    def __init__(self):
        self.pair = "BTC_REP"
        self.period = 300
        self.endTime = time.time()
        self.startTime = self.endTime - 3600 * 2
        self.data = []
        self.prices = []

        self.conn = poloniex('key goes here', 'Secret goes here')

    def getPoints(self):
        return self.data

    def getCurrentPrice(self):
        currentValues = self.conn.api_query("returnTicker")
        lastPairPrice = currentValues[self.pair]["last"]
        return lastPairPrice

    def preliminaryCandlesticks(self):
        poloData = self.conn.api_query("returnChartData",
                                       {"currencyPair": self.pair, "start": self.startTime, "end": self.endTime,
                                        "period": self.period})
        for datum in poloData:
            if datum['open'] and datum['close'] and datum['high'] and datum['low'] and datum['date']:
                self.data.append(
                    BotCandlestick(self.period, datum['open'], datum['close'], datum['high'], datum['low'],
                                   datum['weightedAverage'], datum['date']))

        return self.data
