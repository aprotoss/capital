# -*- coding: utf-8 -*-
import os
import sys
import time

#comtypes
#from sklib import *
from config import *
from comtypes.client import GetModule
from comtypes.client import CreateObject
from comtypes.client import GetEvents
sys.coinit_flags = 0
from pythoncom import PumpWaitingMessages

filename = None
fp = None

class SKQuoteLibEvents(object):
    def OnNotifyKLineData(self, bstrStockNo, bstrData): 
        #print('SKQuoteLibEvents: OnNotifyKLineData')
        fp.write(bstrData + '\n')

def waitMessage(t):
    end_time = time.clock() + t
    while time.clock() < end_time:
        PumpWaitingMessages()

if '__main__'  in __name__:
    if len(sys.argv) < 3:
        print('Usage: %s ID PWD {stock no list}')
        sys.exit()

    module = GetModule(CapitalDLL)
    skcenter = CreateObject(module.SKCenterLib, interface=module.ISKCenterLib)
    skquote = CreateObject(module.SKQuoteLib, interface=module.ISKQuoteLib)
        
    #create com signal Object
    #skcenterevents = SKCenterLibEvents()
    skquoteevents = SKQuoteLibEvents()
        
    #centerConn = GetEvents(skcenter, skcenterevents)
    quoteConn = GetEvents(skquote, skquoteevents)

    res = skcenter.SKCenterLib_Login(sys.argv[1], sys.argv[2])
    print('Login:  ', res) 
    waitMessage(10)

    res = skquote.SKQuoteLib_EnterMonitor()
    print('skquote Connect:  ', res)
    waitMessage(10)

    for no in sys.argv[3:]:
        if fp is not None:
            fp.close()

        filename = CachePath + '/' + no + '.csv'
        fp = open(filename, 'w')
        res = skquote.SKQuoteLib_RequestKLineAM(no, 0, 1, 0)
        print('skquote %s :  ' % no , res)
        waitMessage(2)

    res = skquote.SKQuoteLib_LeaveMonitor()
    print('skquote disconnect:  ', res)
    waitMessage(3)

    if fp is not None:
        fp.close()
