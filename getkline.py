# -*- coding: utf-8 -*-
import os
import io
import sys
import time
import numpy
import pandas as pd
from datetime import timedelta
from pathlib import Path
from config import *

#
#comtypes
#
from comtypes.client import GetModule
from comtypes.client import CreateObject
from comtypes.client import GetEvents
sys.coinit_flags = 0
from pythoncom import PumpWaitingMessages

cache = []

class SKQuoteLibEvents(object):
    def OnNotifyKLineData(self, bstrStockNo, bstrData): 
        cache.append(bstrData.split(','))

def waitMessage(t):
    end_time = time.clock() + t
    while time.clock() < end_time:
        PumpWaitingMessages()

def saveToCSV(stockno):
    filename = StocksPath + '/' + stockno + '.1min'

    #Read KLine file
    df = pd.read_csv(filename, names=KL_FIELD, dtype=KL_FIELDTYPES, parse_dates=['Date'], index_col=['Date'])

    lastdate = df.tail(1).index.date[0]
    print('Lastdata: %s' % lastdate)

    #Read Cache (new data)
    cdf = pd.DataFrame.from_records(cache, columns=KL_FIELD)
    cdf['Date'] = pd.to_datetime(cdf['Date'])
    cdf.index = cdf['Date']
    del cdf['Date']
    cdf[['Open', 'High', 'Low', 'Close']] = cdf[['Open', 'High', 'Low', 'Close']].astype(float)
    cdf['Volume'] = cdf['Volume'].astype(int)

    df = df.append(cdf[lastdate + timedelta(days=1):])
    df.to_csv(filename + '.1min', header=False)

if '__main__'  in __name__:
    if len(sys.argv) < 3:
        print('Usage: %s ID PWD [stock no list]')
        sys.exit()

    module = GetModule(CapitalDLL)
    skcenter = CreateObject(module.SKCenterLib, interface=module.ISKCenterLib)
    skquote = CreateObject(module.SKQuoteLib, interface=module.ISKQuoteLib)
        
    #create com signal Object
    skquoteevents = SKQuoteLibEvents()
        
    quoteConn = GetEvents(skquote, skquoteevents)

    res = skcenter.SKCenterLib_Login(sys.argv[1], sys.argv[2])
    print('Login:  ', res) 
    waitMessage(10)

    res = skquote.SKQuoteLib_EnterMonitor()
    print('skquote Connect:  ', res)
    waitMessage(10)

    for no in sys.argv[3:]:
        res = skquote.SKQuoteLib_RequestKLineAM(no, 0, 1, 0)
        print('skquote %s :  ' % no , res)
        waitMessage(1)
        saveToCSV(no)
        tmp = cache
        cache = []
        del tmp

    res = skquote.SKQuoteLib_LeaveMonitor()
    print('skquote disconnect:  ', res)
    waitMessage(3)

