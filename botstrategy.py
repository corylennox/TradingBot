from botlog import BotLog
from botcandlestick import BotCandlestick
from botindicators import BotIndicators
from bottrade import BotTrade
import time


class BotStrategy(object):
    def __init__(self, startingBal):
        self.output = BotLog()
        self.trades = []
        self.candlesticks = []
        self.indicators = BotIndicators()
        self.currentBal = startingBal

    def evaluatePositions(self):
        prices = []
        over_last_n_periods = 15
        lastCandlestick = self.candlesticks[-1]

        for i in range(1, over_last_n_periods + 1):
            prices.append(self.candlesticks[-i].priceAverage)

        if (self.trades and self.trades[-1].status == "CLOSED") or not self.trades:
            # buy
            if lastCandlestick.priceAverage < self.indicators.movingAverage(prices):
                currentTrade = BotTrade(self.trades.__len__() + 1, lastCandlestick.close, lastCandlestick.date, self.currentBal)
                self.trades.append(currentTrade)
                # currentTrade.logBuy()

        if self.trades and self.trades[-1].status == "OPEN":
            lastTrade = self.trades[-1]
            # sell
            if lastCandlestick.priceAverage > self.indicators.movingAverage(prices):
                lastTrade.close(lastCandlestick.close, lastCandlestick.date)
                # lastTrade.logSell()
                self.currentBal = lastTrade.currentBal

    def showPositions(self, startingInvestment, displayTradeDetails):
        investment = startingInvestment
        tradeNum = 1
        for trade in self.trades:
            if trade.exitPrice != '':
                invAtStartOfTrade = investment
                buyTax = investment * -0.0025
                investment = investment + buyTax  # amount of currency bought
                tradeProfit = investment * (float(trade.exitPrice) / float(trade.entryPrice)) - investment
                investment = investment * (float(trade.exitPrice) / float(trade.entryPrice))
                sellTax = investment * -0.0025
                investment = investment + sellTax
                net = investment - invAtStartOfTrade

                if displayTradeDetails:
                    # color code net
                    if net > 0:
                        netStr = "\033[92m$" + str(format(net, ',.2f')) + "\033[0m"
                    else:
                        netStr = "\033[91m$" + str(format(net, ',.2f')) + "\033[0m"

                    print("--------------------" + "Trade #" + str(format(tradeNum, ',')) + " | " +
                          time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(trade.timeTradeStart)) +
                          " - " + time.strftime('%H:%M:%S', time.localtime(trade.timeTradeEnd)) +
                          "--------------------")
                    trade.showTrade()
                    print("\t\t                Buy tax: $" + str(buyTax))
                    print("\t\t               Sell tax: $" + str(sellTax))
                    print("\t\t      Profit from trade: $" + str(tradeProfit))
                    print("\t\t           Before Trade: $" + str(invAtStartOfTrade))
                    print("\t\t            After Trade: $" + str(investment))
                    print("\t\t                    Net: " + netStr)
            tradeNum += 1

        # color code investment
        if investment > startingInvestment:
            endStr = "\033[92m$" + str(format(investment, ',.2f')) + "\033[0m"
        else:
            endStr = "\033[91m$" + str(format(investment, ',.2f')) + "\033[0m"
        print("\nStart: $" + str(format(startingInvestment, ',.2f')))
        print("End: " + endStr)

