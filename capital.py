# -*- coding: utf-8 -*-
#Capital
from intracmddialog import intraCMD
from capitalevent import *
from capitalcode import CapitalMarket
from capitalcode import CapitalStockGroup
from capitalcode import CapitalCode as SCode #Status Code

#Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from capitalui import Ui_MainWindow

#system
from threading import Thread
from ctypes import *
import threading
import sys
import time

#comtypes
from comtypes.client import GetModule
from comtypes.client import CreateObject
from comtypes.client import GetEvents
sys.coinit_flags = 0
from pythoncom import PumpWaitingMessages
from pythoncom import CoInitialize 
from pythoncom import CoInitializeEx
from pythoncom import CoUninitialize

try:
    from PyQt5.QtCore import QString
except:
    QString = str

#lock = threading.Lock()

class Capital(QtWidgets.QMainWindow, Ui_MainWindow):
    stocklist_num = 0
    quoteStockTab = {}
    def __init__(self, parent=None):
        super(Capital, self).__init__(parent)
        self.setupUi(self)

        #Develop Dialog
        self.devDialog = intraCMD(self)
        self.devDialog.cmdTigger.connect(self.setDevCMD)
        self.devDialog.hide()
        self.actionIntraCMD.toggled.connect(self.on_intracmd_cb) 
        self.devDialog.hideTigger.connect(self.on_intracmd_cb)

        #stocklist
        self.stockList.currentChanged.connect(self.on_stocklist_changepage_cb)
        self.semTree.itemDoubleClicked.connect(self.on_tree_itemclicked_cb)
        self.otcTree.itemDoubleClicked.connect(self.on_tree_itemclicked_cb)
        self.futuresTree.itemDoubleClicked.connect(self.on_tree_itemclicked_cb)
        self.optionTree.itemDoubleClicked.connect(self.on_tree_itemclicked_cb)
        self.esmTree.itemDoubleClicked.connect(self.on_tree_itemclicked_cb)

        #stocktab
        self.skstockTab.tabCloseRequested.connect(self.on_tabclosereq_cb)

        #COM Object
        self.setInitCOM()
        self._comRunning = False
        Thread(target=self.comThreadRun, args = ())

        self.connectBtn.clicked.connect(self.capitalLogin)
    
    def closeEvent(self, event):
        if self.connectBtn.isChecked():
            self.capitalLogin(False)
        self._comRunning = False
        self.devDialog.close()

    def setDevCMD(self, cmd):
        argv = []
        args = cmd.split()
        
        argv.append(args[0])
        
        for arg in args[1:]:
            print(arg)
            if arg[0] == '\'' and arg[-1] == '\'':
                argv.append(arg[1:-1])
                continue
            if arg == 'True':
                argv.append(True)
                continue
            if arg == 'False':
                argv.append(False)
                continue

            argv.append(int(arg))

        self.setCMD(*argv)

    def on_intracmd_cb(self, toggled):
        if toggled:
            self.devDialog.show()
            self.actionIntraCMD.setChecked(True)
        else:
            self.devDialog.hide()
            self.actionIntraCMD.setChecked(False)

    def on_stocklist_changepage_cb(self, page):
        #print('page: %d ' % page)
        res = self.skquote.SKQuoteLib_RequestStockList(page)
        self.stocklist_num = 0

#############################################################
#COM objects Control
#############################################################
    def setInitCOM(self):
        #Create COM Objects
        module = GetModule('./CapitalApi_2.13.11/API/x86/SKCOM.dll')
        self.skcenter = CreateObject(module.SKCenterLib, interface=module.ISKCenterLib)
        self.skreply = CreateObject(module.SKReplyLib, interface=module.ISKReplyLib)
        self.skquote = CreateObject(module.SKQuoteLib, interface=module.ISKQuoteLib)
        self.module = module
        
        self.skcenterevents = SKCenterLibEventsHandler()
        self.skreplyevents = SKReplyLibEventsHandler()
        self.skquoteevents = SKQuoteLibEventsHandler()

        #signals
        self.skcenterevents.ontimer.connect(self.timerkeeping_cb)
        self.skquoteevents.onnotifyservertime.connect(self.timerkeeping_cb)
        self.skquoteevents.onnotifystocklist.connect(self.stocklist_cb)
        self.skquoteevents.onconnection.connect(self.onconnection_cb)
        self.skquoteevents.onnotifyquote.connect(self.onnotifyquote_cb)

        self.centerConn = GetEvents(self.skcenter, self.skcenterevents)
        self.replyConn = GetEvents(self.skreply, self.skreplyevents)
        self.quoteConn = GetEvents(self.skquote, self.skquoteevents)
    
    def comThreadRun(self):
        print('[Capital] thread start...')
        CoInitialize()
        self.setInitial()
        self._comRunning = True
    
        while self._comRunning:
            time.sleep(0.1)
            PumpWaitingMessages()
        print('[Capital] thread stop...')
    
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

        argv = args[1:]
        res = getattr(cls, args[0])(*argv)

        #self.statusbar.showMessage('[CMD] %s: %s' % (args[0], SCode[res][0]))
        self.msgBrowser.append('[CMD] %s: %s' % (args[0], SCode[res][0]))

        #lock.release()
        return res
    #
    #COM Object commands
    #
    def capitalLogin(self, checked):
        userID = self.userIDLine.text()
        pwd = self.passwordLine.text()
        if checked:
            res = self.setCMD('SKCenterLib_Login', userID, pwd)
            self.msgBrowser.append('SKCenterLib_Login: ' + SCode[res][1])
            if res is not 0 and res is not 2003:
                self.connectBtn.setChecked(False)
                return None
            time.sleep(2)

            res = self.setCMD('SKReplyLib_ConnectByID', userID)
            self.msgBrowser.append('SKReplyLib_ConnectByID: ' + SCode[res][1])
            if res is not 0:
                self.connectBtn.setChecked(False)
                return None
            time.sleep(2)
            
            res = self.setCMD('SKQuoteLib_EnterMonitor')
            self.msgBrowser.append('SKQuoteLib_EnterMonitor: ' + SCode[res][1])
            if res is not 0:
                self.connectBtn.setChecked(False)
                return None
        else:
            res = self.setCMD('SKQuoteLib_LeaveMonitor')
            self.msgBrowser.append('SKQuoteLib_LeaveMonitor: ' + SCode[res][1])
            if res is not 0:
                self.connectBtn.setChecked(False)
                return None
            
            res = self.setCMD('SKReplyLib_CloseByID',  userID)
            self.msgBrowser.append('SKReplyLib_closeByID: ' + SCode[res][1])
            if res is not 0:
                self.connectBtn.setChecked(False)
                return None
            
            self.stockList.setEnabled(False)

    def timerkeeping_cb(self, strTime):
        self.statusbar.showMessage(strTime)

    def onconnection_cb(self, nKind, nCode):
        #time.sleep(1.5)
        if nKind == 3003 and nCode == 0:
            self.stockList.setEnabled(True)
            self.on_stocklist_changepage_cb(0)
            
    def stocklist_cb(self, market, stockData):
        if self.stockList.currentIndex() is not market:
            print('[Capital] StockList Index and Market is not match')
            return None

        tree = self.stockList.currentWidget().children()[0]

        if self.stocklist_num is 0:
            tree.clear()
            tree.setHeaderLabels(['Stock No.', 'Stock Name'])
            header = tree.header()
            header.setDefaultSectionSize(100)
        self.stocklist_num += 1
        stock = stockData.split(';')
        root = QtWidgets.QTreeWidgetItem(tree)
        if market is 0:
            root.setText(0, '%s (%d)' % (CapitalStockGroup[self.stocklist_num], len(stock)))
        else:
            root.setText(0, 'Group %d (%d)' % self.stocklist_num)

        for s in stock:
            if len(s) is 0:
                continue
            sp = s.split(',')
            head = QtWidgets.QTreeWidgetItem(root)
            head.setText(0, sp[0])
            head.setText(1, sp[1])
        tree.addTopLevelItem(root)
            
    def on_tree_itemclicked_cb(self, item, column):
        if item.data(1, 0) is None:
            #Group Item, skip it.
            return None

        psPageNo = -1
        psPageNo, res = self.skquote.SKQuoteLib_RequestStocks(-1, item.data(0, 0))
        self.msgBrowser.append(('SKQuoteLib_GetStockByNo: ' + SCode[res][1] + ' PageNo: %d') % psPageNo) 
        if res is not 0:
            return None
        self.quoteStockTab[item.data(0, 0)] = [psPageNo, None]
    
    def on_tabclosereq_cb(self, idx):
        stockNo = self.skstockTab.tabText(idx)
        tmp = self.quoteStockTab[stockNo]
        
        #reset quote by pageno
        self.skquote.SKQuoteLib_RequestStocks(tmp[0], None)
        del tmp[1]
        self.quoteStockTab[stockNo] = []
        self.skstockTab.removeTab(idx)
        
    def onnotifyquote_cb(self, sMarketNo, sStockIdx):
        pSKStock = self.module.SKSTOCK()
        pSKStock, res = self.skquote.SKQuoteLib_GetStockByIndex(sMarketNo, sStockIdx, pSKStock)
        self.msgBrowser.append('SKQuoteLib_GetStockByNo: ' + SCode[res][1])
        if res is not 0:
            return None

        self.skstock_add_to_tab(pSKStock)
        
    def skstock_add_to_tab(self, pSKStock):
        tbrowser = self.quoteStockTab[pSKStock.bstrStockNo][1]
        if tbrowser is None:
            tbrowser = QtWidgets.QTextBrowser(self.skstockTab)
            self.skstockTab.addTab(tbrowser, pSKStock.bstrStockNo)
            tbrowser.show()
            tbrowser.setReadOnly(True)
            self.quoteStockTab[pSKStock.bstrStockNo][1] = tbrowser

        tbrowser.clear()

        #tbrowser.append('Index: %d' % pSKStock.sStockidx)
        tbrowser.append('Decimal: %d' % pSKStock.sDecimal)
        tbrowser.append('Type: %d' % pSKStock.sTypeNo)
        tbrowser.append('Market: ' + pSKStock.bstrMarketNo)
        tbrowser.append('Stock: ' + pSKStock.bstrStockNo)		
        tbrowser.append('Company: ' + pSKStock.bstrStockName)	
        tbrowser.append('---------------------------------------')
        tbrowser.append('High: %d' % pSKStock.nHigh)
        tbrowser.append('Open: %d' % pSKStock.nOpen)
        tbrowser.append('Low : %d' % pSKStock.nLow)
        tbrowser.append('Clos: %d' % pSKStock.nClose)

        tbrowser.append('TickQty: %d' % pSKStock.nTickQty)

        tbrowser.append('Ref Cost: %d' % pSKStock.nRef)

        tbrowser.append('Bid: %d' % pSKStock.nBid)
        tbrowser.append('Bc : %d' % pSKStock.nBc)
        tbrowser.append('Ask: %d' % pSKStock.nAsk)
        tbrowser.append('Ac : %d' % pSKStock.nAc)

        tbrowser.append('TBc: %d' % pSKStock.nTBc)
        tbrowser.append('TAc: %d' % pSKStock.nTAc)

        tbrowser.append('FutureOI: %d' % pSKStock.nFutureOI)

        tbrowser.append('Total Qty: %d' % pSKStock.nTQty)
        tbrowser.append('Yesterday Qty: %d' % pSKStock.nYQty)

        tbrowser.append('Up: %d' % pSKStock.nUp)
        tbrowser.append('Down: %d' % pSKStock.nDown)
        if pSKStock.nSimulate is 0:
            tbrowser.append('Simulate: Normal')
        elif pSKStock.nSimulate is 1:
            tbrowser.append('Simulate: trial calculation')
            
#main
if '__main__' in __name__:
    app = QtWidgets.QApplication(sys.argv)
    ui = Capital()
    ui.show()
    sys.exit(app.exec_())
