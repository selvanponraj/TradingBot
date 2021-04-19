from trading import *
from algo import *
from FindTrendingStocks import findTrendingStocks
from datetime import datetime
from datetime import date
import pytz
import time
import csv
import sqlite3
import pandas as pd
from ib_insync import *

# prepare the trading bot by getting the portfolio, and getting the watchlist

tz_NY = pytz.timezone('America/New_York')
now = datetime.now(tz_NY)
start = now.replace(hour=9, minute=30, second=0, microsecond=0)

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

initPortfolio()
findTrendingStocks(ib)
getWatchList()

# # checks time for stock market opening and runs the cycle function continuously
while start <= now and (datetime.now(tz_NY).hour) < 16:
	cycle(ib)

# while(True):
#     cycle(ib)

# stores day's data into a SQL database
con = sqlite3.connect('BotData.db')
df = pd.read_csv('DayLog.csv')
df.to_sql(str(date.today()), con, if_exists = 'append', index = False)

# resets files for the next day
fObj = open('watchlist.csv', 'w')
fObj.close()

fObj = open('DayLog.csv', 'w')
fObj.write('symbol,time,price,upperBand,lowerBand,bandWidth,rsi,upperSlope,\
	realSlope,lowerSlope,upperI,realI,lowerI,action')
fObj.close()
