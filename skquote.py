# -*- coding:utf-8 -*-
from PyQt6 import QtCore
from PyQt6.QtWidgets import QTreeWidgetItem

#sys
import sys
import time

from skcode import *

#comtypes
from comtypes.client import CreateObject
from comtypes.client import GetEvents
sys.coinit_flags = 0
from pythoncom import CoInitialize 

def create_skquote(module):
    skq = CreateObject(module.SKQuoteLib, interface=module.ISKQuoteLib)
    skqEvents = SKQuoteLibEvents()
    connect = GetEvents(skq, skqEvents)
    return skq, skqEvents, connect

class SKQuoteLibEvents(QtCore.QObject):
    onnotifystocklist = QtCore.pyqtSignal(int, str)
    onnotifyklinedata = QtCore.pyqtSignal(str, str)
    onnotifyquote = QtCore.pyqtSignal(int, int)

    #customize
    stocklist_ready = QtCore.pyqtSignal() 
    def OnConnection(self, nKind, nCode):
        print(f"[SKQuote] OnConnection {nKind} - {nCode}")
        if nKind == 3003:
            self.stocklist_ready.emit()

    def OnNotifyServerTime(self, sHour, sMinute, sSecond, nTotal): 
        print(f"[SKQuote] OnNotifyServerTime - {sHour}:{sMinute}:{sSecond} - {nTotal}")
    
    def OnNotifyStockList(self, sMarketNo, bstrStockData):
        #print(f"[SKQuote]: {SKMarket[sMarketNo]} - {bstrStockData}")
        self.onnotifystocklist.emit(sMarketNo, bstrStockData)
    
    def OnNotifyQuote(self, sMarketNo, sStockIdx): 
        #print("[SKQuote] OnNotifyQuote")
        self.onnotifyquote.emit(sMarketNo, sStockIdx)

    def OnNotifyKLineData(self, bstrStockNo, bstrData): 
        #print(f"[SKQuote] OnNotifyKLineData - {bstrStockNo} - {bstrData}")
        self.onnotifyklinedata.emit(bstrStockNo, bstrData)

    def OnNotifyTicksLong(self, sMarketNo, nIndex, nPtr, nDate, nTimehms, nTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        print("[SKQuote] OnNotifyTicksLong")
