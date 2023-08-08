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


    def OnNotifyTicks(self, sMarketNo, nIndex, nPtr, nData, nTimehms, nTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        #[SKQuote] On Notify Ticks: 0 - 26999 - 2757 - 20230807 - 130906 - 846925 - 56000 - 56100 - 56100 - 1 - 0
        print(f"[SKQuote] On Notify Ticks: {sMarketNo} - {nIndex} - {nPtr} - {nData} - {nTimehms} - {nTimemillismicros} - {nBid} - {nAsk} - {nClose} - {nQty} - {nSimulate}")

    def OnNotifyHistoryTicks(self, sMarketNo, nIndex, nPtr, nData, nTimehms, nTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        print("[SKQuote] On Notify History Ticks")

    def OnNotifyBest5(self, sMarketNo, nStockidx, nBestBid1, nBestBidQty1, nBestBid2, nBestBidQty2, nBestBid3, nBestBidQty3, nBestBid4, nBestBidQty4, nBestBid5, nBestBidQty5, nExtendBid, nExtendBidQty, nBestAsk1, nBestAskQty1, nBestAsk2, nBestAskQty2, nBestAsk3, nBestAskQty3, nBestAsk4, nBestAskQty4, nBestAsk5, nBestAskQty5, nExtendAsk, nExtendAskQty, nSimulate):
        # [SKQuote] On Notify Best5: 0 - 26999
        # 56000 - 84
        # 55900 - 195
        # 55800 - 707
        # 55700 - 164
        # 55600 - 244
        # Exten: -999999 - -999999
        # 56100 - 191
        # 56200 - 312
        # 56300 - 200
        # 56400 - 172
        # 56500 - 176
        # -999999 - 56000
        # 0
        print(f"[SKQuote] On Notify Best5: {sMarketNo} - {nStockidx}")
        print(f"{nBestBid1} - {nBestBidQty1}")
        print(f"{nBestBid2} - {nBestBidQty2}")
        print(f"{nBestBid3} - {nBestBidQty3}")
        print(f"{nBestBid4} - {nBestBidQty4}")
        print(f"{nBestBid5} - {nBestBidQty5}")
        print(f"Exten: {nExtendBid} - {nExtendBid}")
        print(f"{nBestAsk1} - {nBestAskQty1}")
        print(f"{nBestAsk2} - {nBestAskQty2}")
        print(f"{nBestAsk3} - {nBestAskQty3}")
        print(f"{nBestAsk4} - {nBestAskQty4}")
        print(f"{nBestAsk5} - {nBestAskQty5}")
        print(f"{nExtendAsk} - {nExtendAskQty}")
        print(f"{nSimulate}")
