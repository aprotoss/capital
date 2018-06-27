# -*- coding:utf-8 -*-
#Qt
from PyQt5 import QtCore
try:
    from PyQt5.QtCore import QString
except:
    QString = str

#sys
import sys
import time

from skthread import SKThread
from skcode import *

#comtypes
from comtypes.client import CreateObject
from comtypes.client import GetEvents
sys.coinit_flags = 0
from pythoncom import PumpWaitingMessages
from pythoncom import CoInitialize 

class SKQuote(SKThread):
    notifystocklist = QtCore.pyqtSignal(int, list)
    notifyquote = QtCore.pyqtSignal(int, object)
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        #Create COM Object
        self.skquote = CreateObject(self.module.SKQuoteLib, interface=self.module.ISKQuoteLib)
        #create COM Event
        self.skquoteevents = SKQuoteLibEvents()
        #To regist COM Event to COM Object
        self.quoteConn = GetEvents(self.skquote, self.skquoteevents)

        #This timer is for quote to request the time server for avoid server disconnect this link
        self.keeptimer = QtCore.QTimer()
        self.keeptimer.setInterval(15000) #15 sec
        self.keeptimer.setSingleShot(False)
        self.keeptimer.timeout.connect(self.on_timer_timeout_cb)

        #Events
        self.skquoteevents.onconnection.connect(self.on_onconnection_cb)
        self.skquoteevents.onnotifyservertime.connect(self.on_onnotifyservertime_cb)
        self.skquoteevents.onnotifystocklist.connect(self.on_onnotifystocklist_cb)
        self.skquoteevents.onnotifyquote.connect(self.on_onnotifyquote_cb)

    def enterMonitor(self):
        ret = self.skquote.SKQuoteLib_EnterMonitor()
        if ret == 0:
            self.message.emit('[SKQuote] Enter Monitor success')
            self.keeptimer.start()
            return True

        self.message.emit('[SKQuote: %d] %s' % (ret, SKCode[ret][1]))
        return False

    def leaveMonitor(self):
        ret = self.skquote.SKQuoteLib_LeaveMonitor()
        if ret == 0:
            self.message.emit('[SKQuote] Leave Monitor success')
            self.keeptimer.stop()
            return True

        self.message.emit('[SKQuote: %d] %s' % (ret, SKCode[ret][1]))
        return False

    def requestStockList(self, index):
        ret = self.skquote.SKQuoteLib_RequestStockList(index)
        if ret == 0:
            self.message.emit('[SKQuote] Request Stock success')
            return True

        self.message.emit('[SKQuote: %d] %s' % (ret, SKCode[ret][1]))
        return False

    def requestStocks(self, bstrStockNo):
        page, ret = self.skquote.SKQuoteLib_RequestStocks(-1, bstrStockNo)
        return ret

    #
    # Events
    #
    def on_onconnection_cb(self, nKind, nCode):
        if nKind == 3003 and nCode == 0:
            self.message.emit('[SKQuote] Connect success')
        elif nCode is not 0:
            self.message.emit('[SKQuote %d] %s' % (nCode, SKCode[nCode][0]))
        
    def on_onnotifyservertime_cb(self, sHour, sMinute, sSecond, nTotal):
        self.message.emit('[SKQuote] server time: %2d:%2d:%2d %d' % (sHour, sMinute, sSecond, nTotal))
        
    def on_onnotifystocklist_cb(self, sMarketNo, bstrStockData):
        sp = []
        for s in bstrStockData.split(';'):
            if len(s) is 0:
                continue
            sp.append(s.split(','))
        self.notifystocklist.emit(sMarketNo, sp)

    def on_timer_timeout_cb(self):
        self.skquote.SKQuoteLib_RequestServerTime()

    def on_onnotifyquote_cb(self, sMarketNo, sIndex):
        pSKStock = self.module.SKSTOCK()
        pSKStock, ret = self.skquote.SKQuoteLib_GetStockByIndex(sMarketNo, sIndex, pSKStock)
        #pSKStock, ret = self.skquote.SKQuoteLib_GetStockByNo(sMarketNo, pSKStock)
        self.notifyquote.emit(ret, pSKStock)

class SKQuoteLibEvents(QtCore.QObject):
    #signal
    onconnection = QtCore.pyqtSignal(int, int)
    onnotifyservertime = QtCore.pyqtSignal(int, int, int, int)
    onnotifystocklist = QtCore.pyqtSignal(int, str)
    onnotifyquote = QtCore.pyqtSignal(int, int)
    onnotifyklinedata = QtCore.pyqtSignal(str, str)

    def OnConnection(self, nKind, nCode):
        self.onconnection.emit(nKind, nCode)

    def OnNotifyServerTime(self, sHour, sMinute, sSecond, nTotal): 
        self.onnotifyservertime.emit(sHour, sMinute, sSecond, nTotal)
    
    def OnNotifyStockList(self, sMarketNo, bstrStockData):
        #print('[SKQuote]: %s - %s' % (SKMarket[sMarketNo], bstrStockData))
        self.onnotifystocklist.emit(sMarketNo, bstrStockData)
    
    def OnNotifyQuote(self, sMarketNo, sStockIdx): 
        #print('[SKQuote] OnNotifyQuote')
        self.onnotifyquote.emit(sMarketNo, sStockIdx)

    def OnNotifyKLineData(self, bstrStockNo, bstrData): 
        #print('[SKQuote] OnNotifyKLineData')
        self.onnotifyklinedata.emit(bstrStockNo, bstrData)
