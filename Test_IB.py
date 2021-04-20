import datetime
from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1001)

dt = ''
barsList = []

stock = Stock('OPEN', 'SMART', 'USD', localSymbol='OPEN')

ib.qualifyContracts(stock)
bars = ib.reqHistoricalData(
stock, endDateTime='', durationStr='1 D',
barSizeSetting='1 hour', whatToShow='TRADES', useRTH=True)

df = util.df(bars)
print(df)

# print(ib.accountValues())
account_value = [v for v in ib.accountValues() if v.tag == 'BuyingPower' and v.currency == 'GBP']
print(account_value[0].value)
