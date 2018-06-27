# -*- coding: utf-8 -*-
#Qt
from capitalui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
try:
    from PyQt5.QtCore import QString
except:
    QString = str

#sys
from functools import partial
from pathlib import Path
import time
import sys

#SK
from config import *
from skcode import *
from skcenter import SKCenter
from skquote import SKQuote
from skreply import SKReply
from warrant import Warrant
#from plotwidget import PlotWidget
from realtimeview import RealtimeView

class Capital(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.setupUi(self)
        self.createSKObject()
        self.createOthObject()
        self.setupCalendarUI()
        self.connectUICallBacks()
        self.tablist = {}

        ''' Debug '''
        self.stockgroup_num = 0
        ll = [['0000', 'Press the Stock List Button']]
        self.on_center_notifystocklist_cb(0, ll)
        ''' Debug '''

    def __del__(self):
        if self.centerThr:
            self.center.stop()
        if self.replyThr:
            self.reply.stop()
        if self.quoteThr:
            self.quote.stop()
    
    def createSKObject(self):
        #SKCenter
        self.center = SKCenter()
        self.center.message.connect(self.on_message_cb)
        self.centerThr = QtCore.QThread(self)
        self.center.moveToThread(self.centerThr)
        self.centerThr.started.connect(self.center.process)

        #SKReply
        self.reply = SKReply()
        self.reply.message.connect(self.on_message_cb)
        self.replyThr = QtCore.QThread(self)
        self.reply.moveToThread(self.replyThr)
        self.replyThr.started.connect(self.reply.process)

        #SKQuote
        self.quote = SKQuote()
        self.quote.message.connect(self.on_message_cb)
        self.quoteThr = QtCore.QThread(self)
        self.quote.moveToThread(self.quoteThr)
        self.quoteThr.started.connect(self.quote.process)

    def createOthObject(self):
        self.warrant = Warrant()
        self.warrant.message.connect(self.on_message_cb)
        
    def setupCalendarUI(self):
        for date in self.warrant.getHistory():
            d = date.split('-')
            qd = QtCore.QDate(int(d[0]), int(d[1]), int(d[2]))
            dtf = self.calendar.dateTextFormat(qd)
            dtf.setFontUnderline(True)
            dtf.setFontItalic(True)
            self.calendar.setDateTextFormat(qd, dtf)

    def connectUICallBacks(self):
        #Login: center/reply/quote
        self.loginBtn.clicked.connect(self.on_loginbtn_clicked_cb)
        self.centerBtn.clicked.connect(self.on_centerbtn_clicked_cb)
        self.replyBtn.clicked.connect(self.on_replybtn_clicked_cb)
        self.quoteBtn.clicked.connect(self.on_quotebtn_clicked_cb)

        #Stock List
        self.semBtn.clicked.connect(partial(self.on_stocklist_change_cb, 0))
        self.otcBtn.clicked.connect(partial(self.on_stocklist_change_cb, 1))
        self.futuresBtn.clicked.connect(partial(self.on_stocklist_change_cb, 2))
        self.optionBtn.clicked.connect(partial(self.on_stocklist_change_cb, 3))
        self.esmBtn.clicked.connect(partial(self.on_stocklist_change_cb, 4))
        self.quote.notifystocklist.connect(self.on_center_notifystocklist_cb)
        self.treeWidget.customContextMenuRequested.connect(self.on_tree_preparemenu_cb)
        self.treeWidget.itemDoubleClicked.connect(self.on_tree_idclick_cb)

        #Calendar
        self.calendar.clicked.connect(self.on_calendar_selectdate_cb)

        #stocktab
        self.tabWidget.tabCloseRequested.connect(self.on_tab_close_cb)
        self.quote.notifyquote.connect(self.on_onnotifyquote_cb)

#
# CallBacks
#
# -- Login --
    def on_loginbtn_clicked_cb(self, clicked):
        if not self.on_centerbtn_clicked_cb(clicked):
            self.loginBtn.setChecked(False)
            return None
        #time.sleep(1)
        if not self.on_replybtn_clicked_cb(clicked):
            self.loginBtn.setChecked(False)
            return None
        #time.sleep(1)
        if not self.on_quotebtn_clicked_cb(clicked):
            self.loginBtn.setChecked(False)
            return None
        #ToDo: after login, s/w should autoload stock list
        #time.sleep(2)
        #self.semBtn.click()

        #to keep usename and pwd cannot change when login already
        self.userLEdit.setEnabled(not clicked)
        self.pwdLEdit.setEnabled(not clicked)
  
# -- Stock Lists --
    def on_centerbtn_clicked_cb(self, clicked):
        if clicked:
            self.centerThr.start()
            if not self.center.login(self.userLEdit.text(), self.pwdLEdit.text()):
                self.center.stop()
                self.centerBtn.setChecked(False)
                return False
        else:
            self.center.stop()
        self.centerBtn.setChecked(clicked) 
        return True

    def on_replybtn_clicked_cb(self, clicked):
        if clicked:
            self.replyThr.start()
            if not self.reply.connectByID(self.userLEdit.text()):
                self.reply.stop()
                self.replyBtn.setChecked(False)
                return False
        else:
            self.reply.closeByID(self.userLEdit.text())
            self.reply.stop()
        self.replyBtn.setChecked(clicked) 
        return True
        
    def on_quotebtn_clicked_cb(self, clicked):
        if clicked:
            self.quoteThr.start()
            if not self.quote.enterMonitor():
                self.quote.stop()
                self.quoteBtn.setChecked(False)
                return False
        else:
            self.quote.leaveMonitor()
            self.quote.stop()
        self.quoteBtn.setChecked(clicked) 
        return True

    def on_stocklist_change_cb(self, index):
        self.treeWidget.clear()
        self.stockgroup_num = 0
        self.quote.requestStockList(index)
        
    def on_center_notifystocklist_cb(self, sMarketNo, bstrStockData):
        self.treeWidget.setHeaderLabels(['Code', 'Name'])
        self.treeWidget.header().setDefaultSectionSize(100)

        root = QtWidgets.QTreeWidgetItem(self.treeWidget)
        if sMarketNo is 0:
            root.setText(0, '%s (%d)' % (SKStockGroup[self.stockgroup_num], len(bstrStockData)))
        else:
            root.setText(0, 'Group%d (%d)' % (self.stockgroup_num, len(bstrStockData)))

        for item in bstrStockData:
            head = QtWidgets.QTreeWidgetItem(root)
            head.setText(0, item[0])
            head.setText(1, item[1])
        self.treeWidget.addTopLevelItem(root)
        self.stockgroup_num = self.stockgroup_num + 1
        
    def on_tree_preparemenu_cb(self, pos):
        try:
            code = self.treeWidget.itemAt(pos).text(0)
            name = self.treeWidget.itemAt(pos).text(1)
            if len(name) is 0:
                return None

            menu = QtWidgets.QMenu(name, self)
            action = QtWidgets.QAction(name, menu)
            action.setDisabled(True)
            menu.addAction(action)
            menu.addSeparator()
            menu.addAction(code)

            menu.show()
            menu.exec(self.treeWidget.mapToGlobal(pos))
        except:
            return None

    def on_tree_idclick_cb(self, item, column):
        #Group Item, skip it
        if item.data(1, 0) is None:
            return None

        stockno = item.data(0, 0)

        #already exist
        if stockno in self.tablist.keys():
            return None

        #ToDo: Request all line for polt
        self.tablist[stockno] = RealtimeView()
        self.tabWidget.addTab(self.tablist[stockno], stockno)
        self.quote.requestStocks(item.data(0, 0))

# -- calendar -- 
    def on_calendar_selectdate_cb(self, date):
        self.warrant.downloadWarrant(date)

    def on_message_cb(self, message):
        self.msgBrowser.append(message)

# -- Stock Tab --
    def on_tab_close_cb(self, index):
        wid = self.tablist.pop(self.tabWidget.tabText(index))
        del wid
        self.tabWidget.removeTab(index)

    def on_onnotifyquote_cb(self, ret, pSKStock):
        if ret is not 0:
            self.msgBrowser.append('[SKQUOTE] notify quote: %s' % SKCode[nCode][0])
            return None

        self.tablist[pSKStock.bstrStockNo].setSKStock(pSKStock)

#
# Standalone funcation
#
def checkSystemFolder():
    folds = [HistoryPath, CachePath, StocksPath]
    for f in folds:
        p = Path(f)
        if not p.exists():
            p.mkdir(parents=True) 

#main
if '__main__' in __name__:
    checkSystemFolder()
    app = QtWidgets.QApplication(sys.argv)
    ui = Capital()
    ui.show()
    sys.exit(app.exec_())
