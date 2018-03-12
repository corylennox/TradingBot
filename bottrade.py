import time


class BotTrade(object):
    def __init__(self, tradeNumber, lastCandlestickClose, tradeStart, startingBal):
        self.tradeNumber = tradeNumber
        self.startingBal = startingBal
        self.currentBal = startingBal
        self.status = "OPEN"
        self.entryPrice = lastCandlestickClose
        self.exitPrice = ""
        self.timeTradeStart = tradeStart
        self.timeTradeEnd = ""
        # self.stopLoss = 0
        # if self.stopLoss:
        #     self.stopLoss = lastCandlestickClose - self.stopLoss

    def close(self, lastCandlestickClose, tradeEnd):
        self.status = "CLOSED"
        self.exitPrice = lastCandlestickClose
        self.timeTradeEnd = tradeEnd

    def showTrade(self):
        print("\t\t            Entry Price: " + str(self.entryPrice))
        print("\t\t             Exit Price: " + str(self.exitPrice))
        # tradeStatus = "Entry Price: " + str(self.entryPrice) + " Status: " + str(self.status) + " Exit Price: " + str(
        #     self.exitPrice)

        # if self.status == "CLOSED":
        #     tradeStatus = tradeStatus + " Profit: "
        #     if self.exitPrice > self.entryPrice:
        #         tradeStatus = tradeStatus + "\033[92m"
        #     else:
        #         tradeStatus = tradeStatus + "\033[91m"
        #
        #     tradeStatus = tradeStatus + str(self.exitPrice - self.entryPrice) + "\033[0m"
        #
        # self.output.log(tradeStatus)

    def logBuy(self):
        buyTax = self.currentBal * -.0025

        print("------------------------------------ Trade #" + str(self.tradeNumber) + " ------------------------------------")
        openedStr = "Opened: " + time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(self.timeTradeStart))
        entrStr = "Entr Price: " + str(format(self.entryPrice, '.8f'))
        buyTaxStr = "Buy Tax: $" + str(format(buyTax, '.4f'))

        strings = [openedStr, entrStr, buyTaxStr]
        print "".join(string.rjust(27) for string in strings)

        self.currentBal = self.currentBal + buyTax

    def logSell(self):
        tradeProfit = self.currentBal * (self.exitPrice / self.entryPrice) - self.currentBal
        self.currentBal = self.currentBal * (self.exitPrice / self.entryPrice)
        sellTax = self.currentBal * -0.0025
        self.currentBal = self.currentBal + sellTax
        net = self.currentBal - self.startingBal

        # color code net
        if self.currentBal > self.startingBal:
            netStr = "\033[92m$" + str(format(net, ',.2f')) + "\033[0m"
        else:
            netStr = "\033[91m$" + str(format(net, ',.2f')) + "\033[0m"

        closedStr = "Closed: " + time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(self.timeTradeEnd))
        exitStr = "Exit Price: " + str(format(self.exitPrice, '.8f'))
        sellTaxStr = "Sell Tax: $" + str(format(sellTax, '.4f'))

        strings = [closedStr, exitStr, sellTaxStr]
        profitStr = "Profit: $" + str(format(tradeProfit, '.4f'))
        print "".join(string.rjust(27) for string in strings)
        print(profitStr.rjust(27*3))
        print("Net: " + netStr)
        print("Current Balance: $" + str(self.currentBal))
