import sys
import time
import urllib2
from livebotchart import LiveBotChart
from botstrategy import BotStrategy
from botcandlestick import BotCandlestick

def main(argv):
    chart = LiveBotChart()
    strategy = BotStrategy(50)
    strategy.candlesticks = chart.preliminaryCandlesticks()
    developingCandlestick = BotCandlestick()

    while True:
        try:
            developingCandlestick.tick(chart.getCurrentPrice())
        except urllib2.URLError:
            time.sleep(1)
            developingCandlestick.tick(chart.getCurrentPrice())

        if developingCandlestick.isClosed():
            strategy.candlesticks.append(developingCandlestick)
            strategy.evaluatePositions()
            developingCandlestick = BotCandlestick()

        time.sleep(1)


if __name__ == "__main__":
    main(sys.argv[1:])
