# -*- coding: utf-8 -*-
from agent import Agent
from capitalui import Ui_MainWindow
from intracmddialog import intraCMD
from capitalcode import CapitalCode as SCode #Status Code
from capitalaction import *
from config import *

#Qt
from PyQt5 import QtCore, QtGui, QtWidgets

try:
    from PyQt5.QtCore import QString
except:
    QString = str

#system
import sys
import time
import threading

class Capital(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.agent = Agent()
        self.agentThread = QtCore.QThread(parent=self)
        self.agent.moveToThread(self.agentThread)
        self.agentThread.started.connect(self.agent.process)
        self.agentThread.start()

        self.agent.errorMsg.connect(self.errormsg_cb)
        self.agent.successMsg.connect(self.successmsg_cb)
        self.agent.timerkeeping.connect(self.timerkeeping_cb)
        self.agent.skquoteconnect.connect(self.skquoteconnect_cb)
        self.agent.stocklist.connect(self.stocklist_cb)

        #History - warrant
        self.actionWarrant.triggered.connect(self.on_actionwarrant_cb)

        #History - Stock
        self.actionStockKLine.triggered.connect(self.on_actionstockkline_cb)

        #Develop Dialog
        self.devDialog = intraCMD(self)
        self.devDialog.cmdTigger.connect(self.setDevCMD)
        self.devDialog.hide()
        self.actionIntraCMD.toggled.connect(self.on_intracmd_cb) 
        self.devDialog.hideTigger.connect(self.on_intracmd_cb)
        
        #Get Stock KLine Timer
        self.getstockklineTimer = QtCore.QTimer(self)
        self.getstockklineTimer.setSingleShot(False)
#        self.getstockklineTimer.timeout.connect(self.agent.getstockklinetimer_cb)
        self.getstockklineTimer.timeout.connect(self.getstockklinetimer_cb)
        self.agent.klinefinish.connect(self.getstockklinefinish_cb)

        #Login 
        self.connectBtn.clicked.connect(self.capitalLogin)



#######
# HistoryAgent Callback
######
    def errormsg_cb(self, func, nCode):
        try:
            self.msgBrowser.append(func + ' ' + SCode[nCode][1])
        except:
            self.msgBrowser.append(func + ' - UnKnow Error ' )

    def successmsg_cb(self, res):
        self.msgBrowser.append(res)
        
    def timerkeeping_cb(self, sTime):
        self.statusbar.showMessage(sTime)
        
    def stocklist_cb(self, stocklist):
        tree = self.semTree
        tree.clear()
        tree.setHeaderLabels(['Stock No.', 'Stock Name'])
        header = tree.header()
        header.setDefaultSectionSize(100)
        
        for skey in stocklist:
            root = QtWidgets.QTreeWidgetItem(tree)
            root.setText(0, '%s (%d)' % (skey, len(stocklist[skey])))
            for item in stocklist[skey]:
                head = QtWidgets.QTreeWidgetItem(root)
                head.setText(0, item[0])
                head.setText(1, item[1])
            tree.addTopLevelItem(root)
#######
# User Interface Callback
######
    def capitalLogin(self, checked):
        res = self.agent.Login(self.userIDLine.text(), self.passwordLine.text(), checked)
        if not res:
            self.connectBtn.setChecked(False)

        if not checked:
            self.getstockklineTimer.stop()

    def skquoteconnect_cb(self):
        if self.connectBtn.isChecked():
            self.msgBrowser.append('Load the Stocklist')
            self.agent.RequestStockList(0)

    #Action: Get Warrant Doc
    def on_actionwarrant_cb(self):
        self.msgBrowser.append('Start Get Warrant Doc ...')
        self.getwarrant_thread = QtCore.QThread(self)
        self.getwarrantdoc_obj = GetWarrantDoc()
        self.getwarrantdoc_obj.moveToThread(self.getwarrant_thread)
        self.getwarrantdoc_obj.getwarrantdoc.connect(self.getwarrantdoc_cb)
        self.getwarrant_thread.started.connect(self.getwarrantdoc_obj.process)
        self.getwarrant_thread.start()
        
    def getwarrantdoc_cb(self, res, date):
        if res:
            self.msgBrowser.append('Get Warrant Doc: %s ... Done' % date)
        else:
            self.msgBrowser.append('Get Warrant Doc: %s ... Fail' % date)
    

    #Action: Stock KLine
    def on_actionstockkline_cb(self):
        if not self.connectBtn.isChecked():
            self.msgBrowser.append('Stock KLine: Login first')
            return None

        if self.getstockklineTimer.isActive():
            self.msgBrowser.append('Stock KLine: Already running')
            return None
        
        res = self.agent.GetStockKLine()
        self.getstockklineTimer.start(250)  #250 msecond
        
    def getstockklinetimer_cb(self):
        self.agent.getstockklinetimer_cb()

    def getstockklinefinish_cb(self):
        self.getstockklineTimer.stop()

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
        self.agent.setCMD(*argv)

    def on_intracmd_cb(self, toggled):
        if toggled:
            self.devDialog.show()
            self.actionIntraCMD.setChecked(True)
        else:
            self.devDialog.hide()
            self.actionIntraCMD.setChecked(False)


#        self.actionStock.toggled.connect(self.on_actionstock_cb)
#
#
#        #stocklist
#        self.stockList.current.agentnged.connect(self.on_stocklist_.agentngepage_cb)
#        self.semTree.itemDoubleClicked.connect(self.on_tree_itemclicked_cb)
#        self.otcTree.itemDoubleClicked.connect(self.on_tree_itemclicked_cb)
#        self.futuresTree.itemDoubleClicked.connect(self.on_tree_itemclicked_cb)
#        self.optionTree.itemDoubleClicked.connect(self.on_tree_itemclicked_cb)
#        self.esmTree.itemDoubleClicked.connect(self.on_tree_itemclicked_cb)
#
#        #stocktab
#        self.skstockTab.tabCloseRequested.connect(self.on_tabclosereq_cb)
#
#        #COM Object
#        self.setInitCOM()
#        self._comRunning = False
#        Thread(target=self.comThreadRun, args = ())
#        self.connectBtn.clicked.connect(self.capitalLogin)
#    

#    
#    #ToDo: 
#    def on_actionstock_cb(self):
#        if self._login:
#            self.scollect = stockCollect()
#            self.scollect.start()
#        
#    def closeEvent(self, event):
#        if self.connectBtn.isChecked():
#            self.capitalLogin(False)
#        self._comRunning = False
#        self.devDialog.close()
#


#
#    def on_stocklist_.agentngepage_cb(self, page):
#        #print('page: %d ' % page)
#        res = self.skquote.SKQuoteLib_RequestStockList(page)
#        self.stocklist_num = 0
#
#
#    def onconnection_cb(self, nKind, nCode):
#        #time.sleep(1.5)
#        if nKind == 3003 and nCode == 0:
#            self.stockList.setEnabled(True)
#            self.on_stocklist_.agentngepage_cb(0)
#            
#    def stocklist_cb(self, market, stockData):
#        if self.stockList.currentIndex() is not market:
#            print('[Capital] StockList Index and Market is not match')
#            return None
#
#        tree = self.stockList.currentWidget().children()[0]
#

#            
#    def on_tree_itemclicked_cb(self, item, column):
#        if item.data(1, 0) is None:
#            #Group Item, skip it.
#            return None
#
#        psPageNo = -1
#        psPageNo, res = self.skquote.SKQuoteLib_RequestStocks(-1, item.data(0, 0))
#        self.msgBrowser.append(('SKQuoteLib_GetStockByNo: ' + SCode[res][1] + ' PageNo: %d') % psPageNo) 
#        if res is not 0:
#            return None
#            
#        stockinfo = stockInformation()
#        self.skstockTab.addTab(stockinfo, item.data(0, 0))
#        stockinfo.show()
#        #self.quoteStockTab[pSKStock.bstrStockNo][0] = stockinfo
#
#        timer = QtCore.QTimer()
#        timer.setSingleShot(True)
#        timer.timeout.connect(self.klineTimeout_cb)
#        self.quoteStockTab[item.data(0, 0)] = [psPageNo, stockinfo, [], timer]
#
#        res = self.skquote.SKQuoteLib_RequestKLine(item.data(0, 0), 0, 1)
#        if res is not 0:
#            return None
#    
#    def on_tabclosereq_cb(self, idx):
#        stockNo = self.skstockTab.tabText(idx)
#        tmp = self.quoteStockTab[stockNo]
#        
#        #reset quote by pageNo
#        self.skquote.SKQuoteLib_RequestStocks(tmp[0], None)
#        del tmp
#        self.quoteStockTab[stockNo] = []
#        self.skstockTab.removeTab(idx)
#        
#    def onnotifyquote_cb(self, sMarketNo, sStockIdx):
#        pSKStock = self.module.SKSTOCK()
#        pSKStock, res = self.skquote.SKQuoteLib_GetStockByIndex(sMarketNo, sStockIdx, pSKStock)
#        self.msgBrowser.append('SKQuoteLib_GetStockByNo: ' + SCode[res][1])
#        if res is not 0:
#            return None
#
#        self.skstock_add_to_tab(pSKStock)
#    
#    def onnotifyklinedata_cb(self, sStockNo, sData):
#        timer = self.quoteStockTab[sStockNo][3]
#        data = sData.split(',')
#        self.quoteStockTab[sStockNo][2].append(data)
#
#        timer.stop()
#        timer.start(50)
#
#        
#    def skstock_add_to_tab(self, pSKStock):
#        stockinfo = self.quoteStockTab[pSKStock.bstrStockNo][1]
#        tbrowser = stockinfo.getTextBrowser()
#        tbrowser.clear()
#
#        #tbrowser.append('Index: %d' % pSKStock.sStockidx)
#        tbrowser.append('Decimal: %d' % pSKStock.sDecimal)
#        tbrowser.append('Type: %d' % pSKStock.sTypeNo)
#        tbrowser.append('Market: ' + pSKStock.bstrMarketNo)
#        tbrowser.append('Stock: ' + pSKStock.bstrStockNo)		
#        tbrowser.append('Company: ' + pSKStock.bstrStockName)	
#        tbrowser.append('---------------------------------------')
#        tbrowser.append('High: %d' % pSKStock.nHigh)
#        tbrowser.append('Open: %d' % pSKStock.nOpen)
#        tbrowser.append('Low : %d' % pSKStock.nLow)
#        tbrowser.append('Clos: %d' % pSKStock.nClose)
#
#        tbrowser.append('TickQty: %d' % pSKStock.nTickQty)
#
#        tbrowser.append('Ref Cost: %d' % pSKStock.nRef)
#
#        tbrowser.append('Bid: %d' % pSKStock.nBid)
#        tbrowser.append('Bc : %d' % pSKStock.nBc)
#        tbrowser.append('Ask: %d' % pSKStock.nAsk)
#        tbrowser.append('Ac : %d' % pSKStock.nAc)
#
#        tbrowser.append('TBc: %d' % pSKStock.nTBc)
#        tbrowser.append('TAc: %d' % pSKStock.nTAc)
#
#        tbrowser.append('FutureOI: %d' % pSKStock.nFutureOI)
#
#        tbrowser.append('Total Qty: %d' % pSKStock.nTQty)
#        tbrowser.append('Yesterday Qty: %d' % pSKStock.nYQty)
#
#        tbrowser.append('Up: %d' % pSKStock.nUp)
#        tbrowser.append('Down: %d' % pSKStock.nDown)
#        if pSKStock.nSimulate is 0:
#            tbrowser.append('Simulate: Normal')
#        elif pSKStock.nSimulate is 1:
#            tbrowser.append('Simulate: trial calculation')
#        
#    def klineTimeout_cb(self):
#        for key in self.quoteStockTab:
#            data = self.quoteStockTab[key][2]
#            stockinfo = self.quoteStockTab[key][1]
#            stockinfo.plotStockData(data)
#main
if '__main__' in __name__:
    app = QtWidgets.QApplication(sys.argv)
    ui = Capital()
    ui.show()
    sys.exit(app.exec_())
