import sys, getopt
import time

from botchart import BotChart
from botstrategy import BotStrategy


def main(argv):
    showTradeDetails = False
    startingBal = 100
    endTime = time.time()
    startTime = endTime - 3600 * 24 * 2
    period = 900  # period values can be 300, 900, 1800, 7200, 14400, and 86400
    usdtPairs = ["USDT_REP",
                 "BTC_REP"]
    btcPairs = ["USDT_BCH",
                "USDT_BTC",
                "USDT_DASH",
                "USDT_ETC",
                "USDT_ETH",
                "USDT_LTC",
                "USDT_NXT",
                "USDT_REP",
                "USDT_STR",
                "USDT_XMR",
                "USDT_XRP",
                "USDT_ZEC",
                "BTC_REP",
                "BTC_XMR"]

    pairs = btcPairs
    for pair in pairs:
        chart = BotChart(pair, period, endTime, startTime)
        strategy = BotStrategy(startingBal)

        i = 0
        for candlestick in chart.getPoints():
            strategy.candlesticks.append(candlestick)
            if i > 24:
                strategy.evaluatePositions()
            i += 1

        strategy.showPositions(startingBal, showTradeDetails)
        print("Start: " + time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(chart.startTime)))
        print("End  : " + time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(chart.endTime)))
        print("Currency: " + chart.pair)

if __name__ == "__main__":
    main(sys.argv[1:])
