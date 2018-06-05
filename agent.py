# -*- coding: utf-8 -*-
#Capital
from capitalevent import *
from capitalcode import CapitalStockGroup

from config import *

#Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from capitalui import Ui_MainWindow

try:
    from PyQt5.QtCore import QString
except:
    QString = str

#system
import csv
import sys
import select 
import time
import requests
from datetime import datetime

#comtypes
from comtypes.client import GetModule
from comtypes.client import CreateObject
from comtypes.client import GetEvents
sys.coinit_flags = 0
from pythoncom import PumpWaitingMessages
from pythoncom import CoInitialize 
from pythoncom import CoInitializeEx
from pythoncom import CoUninitialize

class Agent(QtCore.QObject):
    #Signal
    errorMsg = QtCore.pyqtSignal(str, int)
    successMsg = QtCore.pyqtSignal(str)
    
    timerkeeping = QtCore.pyqtSignal(str)
    skquoteconnect = QtCore.pyqtSignal()
    stocklist = QtCore.pyqtSignal(list)
    klinefinish = QtCore.pyqtSignal()

    #Stock Values
    _stocklist = {}

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self._running = False
        self._skquote_connect = False
        
        #COM Object
        self.setInitCOM()

    @QtCore.pyqtSlot()
    def process(self):
        CoInitialize()
        self._running = True
        while self._running:
            time.sleep(0.1)
            PumpWaitingMessages()

    #setCMD: for COM Object command 
    def setCMD(self, *args):
        #global lock
        #lock.acquire()
        res = None
        cls = None
        
        if args[0][:6] == 'SKCent':
            cls = self.skcenter

        if args[0][:6] == 'SKRepl':
            cls = self.skreply

        if args[0][:6] == 'SKQuot':
            cls = self.skquote
       
        if args[0][:6] == 'SKOOQu':
            cls = self.skooquote
        
        if args[0][:6] == 'SKOSQu':
            cls = self.skosquote
        
        if args[0][:6] == 'SKOrde':
            cls = self.skorder

        try:
            argv = args[1:]
            res = getattr(cls, args[0])(*argv)
        except:
            self.errorMsg.emit('set CMD: %s' % args[0], 1)

        return res
#
# Normal Command
#
    def Login(self, userID, pwd, out):
        if out is True:
            res = self.setCMD('SKCenterLib_Login', userID, pwd)
            if not (res is 0 or res == 2003):
                self.errorMsg.emit('SKCenterLib_Login', res)
                return False
            time.sleep(2)

            res = self.setCMD('SKReplyLib_ConnectByID', userID)
            if res is not 0:
                self.errorMsg.emit('SKReplyLib_ConnectByID', res)
                return False
            time.sleep(2)
            
            res = self.setCMD('SKQuoteLib_EnterMonitor')
            if res is not 0:
                self.errorMsg.emit('SKQuoteLib_EnterMonitor', res)
                return False

            self.successMsg.emit('Login --- OK')
            return True
        else:
            res = self.setCMD('SKQuoteLib_LeaveMonitor')
            if res is not 0:
                self.errorMsg.emit('SKQuoteLib_LeaveMonitor', res)
                return False
             
            res = self.setCMD('SKReplyLib_CloseByID',  userID)
            if res is not 0:
                self.errorMsg.emit('SKQuoteLib_CloseByID', res)
                return False
            try:
                self.getstockklineClass.stop()
            except:
                pass
            self.successMsg.emit('Logout --- OK')
            return True

    def Logoout(self):
        self.Login(None, None, False)

    def stop(self):
        self._running = False

    def RequestStockList(self, page):
        res = self.skquote.SKQuoteLib_RequestStockList(page)
        if res is not 0:
            print(res)
            self.errorMsg.connect('RequestStockList', res)

    #Action: GetStockKLine
    def GetStockKLine(self):
        try:
            if self.getstockklineThread.isRunning():
                self.errorMsg.emit('stockkline already exist', False)
                return False
        except:
            #threads
            self.stockpoint = [1, 0]

            #self.getstockklineThread = QtCore.QThread()
            #self.getstockklineClass = WriteStockKLine()
            #self.getstockklineClass.moveToThread(self.getstockklineThread)
            #self.getstockklineThread.started.connect(self.getstockklineClass.process)
            #self.getstockklineThread.start()

        return True

    def getstockklinetimer_cb(self):
        sp = self.stockpoint
        no = self._stocklist[CapitalStockGroup[sp[0]]][sp[1]]

        if sp[0] == 33:  #skip warrant
            sp[0] = sp[0] + 1
       
        self.getstockklineClass.setStockNo(no[0])
        res = self.skquote.SKQuoteLib_RequestKLineAM(no[0], 0, 1, 0)
        self.successMsg.emit('Start to Get Stock %s - %s(%s) K-Line' % (CapitalStockGroup[sp[0]], no[1], no[0]))

        sp[1] = sp[1] + 1
        if sp[1] >= len(self._stocklist[CapitalStockGroup[sp[0]]]):
            sp[0] = sp[0] + 1
            sp[1] = 0

        if sp[0] > 34:
            self.getstockklineClass.stop()
            del self.getstockklineClass
            del self.getstockklineThread
            self.successMsg.emit('Get Stocks Finish')


    def requestkline_cb(self, sStockNo):
        self.getstockklineClass.setStockNo(sStockNo)
        res = self.skquote.SKQuoteLib_RequestKLine(sStockNo, 0, 1)
        if res is not 0:
            return None

#############################################################
#COM objects Control
#############################################################
    def setInitCOM(self):
        #Create COM Objects
        module = GetModule(CapitalDLL)
        self.skcenter = CreateObject(module.SKCenterLib, interface=module.ISKCenterLib)
        self.skreply = CreateObject(module.SKReplyLib, interface=module.ISKReplyLib)
        self.skquote = CreateObject(module.SKQuoteLib, interface=module.ISKQuoteLib)
        self.module = module
        
        #create com signal Object
        self.skcenterevents = SKCenterLibEventsHandler()
        self.skreplyevents = SKReplyLibEventsHandler()
        self.skquoteevents = SKQuoteLibEventsHandler()

        #regist to COM Object
        self.centerConn = GetEvents(self.skcenter, self.skcenterevents)
        self.replyConn = GetEvents(self.skreply, self.skreplyevents)
        self.quoteConn = GetEvents(self.skquote, self.skquoteevents)

        #signals - skcenter
        self.skcenterevents.ontimer.connect(self.timerkeeping_cb)

        #signals - skquote
        self.skquoteevents.onnotifyservertime.connect(self.timerkeeping_cb)
        self.skquoteevents.onnotifystocklist.connect(self.stocklist_cb, QtCore.Qt.QueuedConnection)
        self.skquoteevents.onconnection.connect(self.onconnection_cb)
        self.skquoteevents.onnotifyquote.connect(self.onnotifyquote_cb)
        self.skquoteevents.onnotifyklinedata.connect(self.onnotifyklinedata_cb, QtCore.Qt.QueuedConnection)
        
    def timerkeeping_cb(self, strTime):
        self.timerkeeping.emit(strTime)
        
    #Action: Stock List
    def stocklist_cb(self, market, stockData):
        sp = []
        for s in stockData.split(';'):
            if len(s) is 0:
                continue
            sp.append(s.split(','))
        self.stocklist.emit(sp)

    def onconnection_cb(self, nKind, nCode):
        if nKind == 3003 and nCode == 0:
            self._skquote_connect = True
            self.skquoteconnect.emit()
        elif nCode is not 0:
            self.errorMsg.emit('onconnection_cb', nCode)
    
    def onnotifyquote_cb(self, sMarketNo, sStockIdx):
        pSKStock = self.module.SKSTOCK()
        pSKStock, res = self.skquote.SKQuoteLib_GetStockByIndex(sMarketNo, sStockIdx, pSKStock)

        if res is not 0:
            self.errorMsg.emit('onnotifyquote_cb', res)
            return None
        print(self.module.OnUpDateDataRow(pSKStock))
    
    #Action: K-Line
    def onnotifyklinedata_cb(self, sStockNo, sData):
        self.getstockklineClass.setData([sStockNo, sData])
        
