from bs4 import BeautifulSoup
import requests

import pytest
import logging

import os
from ib_insync import *

def findTrendingStocks(ib):
    symbols = []
    sub = ScannerSubscription(
    instrument='STK',
    locationCode='STK.US.MAJOR',
    scanCode='MOST_ACTIVE')
    
    # tagValues = [
    #     TagValue("changePercAbove", "20"),
    #     TagValue('priceAbove', 5),
    #     TagValue('priceBelow', 50)]

    # the tagValues are given as 3rd argument; the 2nd argument must always be an empty list
    # (IB has not documented the 2nd argument and it's not clear what it does)
    # scanData = ib.reqScannerData(sub, [], tagValues)
    scanData = ib.reqScannerData(sub)

    symbols = [sd.contractDetails.contract.symbol for sd in scanData]
    print(symbols)
    fObj = open('watchlist.csv', 'w')
    for s in symbols:
        fObj.write(s + '\n')
    fObj.close()