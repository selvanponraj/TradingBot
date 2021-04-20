import pandas_datareader.data as web
import pandas as pd
from FindTrendingStocks import findTrendingStocks
from datetime import datetime
from config import *
from algo import *
import os
import time
import csv
from pandas_datareader._utils import RemoteDataError
from ib_insync import *

def getAccountInfo(ib,tag,currency):
	account_value = [v for v in ib.accountValues() if v.tag == tag and v.currency == currency]
	return account_value[0]

# get stocks on the watchlist and portfolio and save them in a set to determine
# which stocks to watch		
def getWatchList():
	trending = []
	fObj = open('watchlist.csv')
	for line in fObj:
		if line != '':
			trending.append(line.strip())
	watchlist = list(portfolio.keys()) + trending
	watchlist = set(watchlist)
	return watchlist

# updates the portfolio.csv file after transactions
def updatePortfolio():
	fObj = open('portfolio.csv', 'w')
	for key in portfolio:
		fObj.write(str(key) + ',' + str(portfolio[key]) + '\n')
	fObj.close()

# cycle function that will repeat (loop), gets stock data and decides what to do
def cycle(ib):
	watchlist = getWatchList()
	for symbol in watchlist:
		try:
			stock = Stock(symbol, 'SMART', 'USD', localSymbol=symbol)
			ib.qualifyContracts(stock)
			move = decide(stock,ib)
			if move == 'sell':
				# create_order(symbol, portfolio[symbol], 'sell', 'market', 'gtc')
				order = MarketOrder('SELL', portfolio[symbol])
				trade = ib.placeOrder(stock, order)
				# Uncomment during market hours
				# while not trade.isDone():
				# 	ib.waitOnUpdate()
				print('Sold ' + symbol + ' at ' + str(getPrice(stock,ib)))
				del portfolio[symbol]
				updatePortfolio()
			elif move == 'buy':
				if float(getAccountInfo(ib,'BuyingPower','GBP').value) < 3000:
					continue;
				# create_order(symbol, 3000 // getPrice(symbol,ib), 'buy', 'market', 'gtc')
				order = MarketOrder('BUY', 3000 // getPrice(stock,ib))
				trade = ib.placeOrder(stock, order)
				# Uncomment during market hours
				# while not trade.isDone():
				# 	ib.waitOnUpdate()
				print('Bought ' + symbol + ' at ' + str(getPrice(stock,ib)))
				portfolio[symbol] = 3000 // getPrice(stock,ib)
				updatePortfolio()
			else:
				continue;
		except RemoteDataError as e:
			print(e)
		except KeyError as a:
			print(a)