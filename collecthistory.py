# -*- coding: utf-8 -*-
#Qt
from PyQt5 import QtCore, QtGui, QtWidgets
try:
    from PyQt5.QtCore import QString
except:
    QString = str

from collecthistoryui import Ui_MainWindow
from capitalaction import GetWarrantDoc
from capitalaction import WriteStockKLine
from capitalcode import CapitalStockGroup
from agent import Agent
from functools import partial
from config import *

import sys
import datetime

class CollectHistory(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.setupUi(self)
        
        #Agent
        self.agent = Agent()
        self.agentThread = QtCore.QThread(parent=self)
        self.agent.moveToThread(self.agentThread)
        self.agentThread.started.connect(self.agent.process)
        self.agentThread.start()
        
        #Agent Signal
        self.agent.errorMsg.connect(self.errormsg_cb)
        self.agent.successMsg.connect(self.successmsg_cb)
        self.agent.skquoteconnect.connect(self.on_skquoteconnect_cb)
        self.agent.stocklist.connect(self.stocklist_cb)
        self.pre_stocktype = -1
        self.stockgroup_num = 1

        #Login 
        self.connectBtn.clicked.connect(self.capitalLogin)
        
        #stockList
        self.stockTree.itemDoubleClicked.connect(self.on_stocktree_dclicked_cb)
        self.semBtn.clicked.connect(partial(self.on_stocklist_change_cb, 0))
        self.otcBtn.clicked.connect(partial(self.on_stocklist_change_cb, 1))
        self.futuresBtn.clicked.connect(partial(self.on_stocklist_change_cb, 2))
        self.optionBtn.clicked.connect(partial(self.on_stocklist_change_cb, 3))
        self.esmBtn.clicked.connect(partial(self.on_stocklist_change_cb, 4))

        #Calendar 
        self.calendar.clicked.connect(self.selectDate)
        self.getWarrantLabel.setTitle(self.getWarrantLabel.title() + '('+ QtCore.QDate.currentDate().toString('yyyy-MM-dd') + ')')
        self.calendar.setSelectedDate(QtCore.QDate.currentDate())

        #WriteKLine Object
        self.agent.GetStockKLine()

    def selectDate(self, date):
        self.msgBrowser.append('Start Get Warrant Doc ...')
        self.getwarrantThread = QtCore.QThread(self)
        self.getwarrantdocObj = GetWarrantDoc()
        self.getwarrantdocObj.moveToThread(self.getwarrantThread)
        self.getwarrantdocObj.getwarrantdoc.connect(self.getwarrantdoc_cb)
        self.getwarrantThread.started.connect(partial(self.getwarrantdocObj.process, date.toString('yyyy-MM-dd')))
        self.getwarrantThread.start()
    
    def getwarrantdoc_cb(self, res, date):
        if res:
            self.msgBrowser.append('Get Warrant Doc: %s ... Done' % date)
        else:
            self.msgBrowser.append('Get Warrant Doc: %s ... Fail' % date)
    
#############################################################
# HistoryAgent Callback
#############################################################
    def errormsg_cb(self, func, nCode):
        try:
            self.msgBrowser.append(func + ' ' + SCode[nCode][1])
        except:
            self.msgBrowser.append(func + ' - UnKnow Error ' )

    def successmsg_cb(self, res):
        self.msgBrowser.append(res)

    def on_skquoteconnect_cb(self):
        self.stockTree.setEnabled(True)
        self.stocktypeGroup.setEnabled(True)
        self.on_stocklist_change_cb(0)
            
    def stocklist_cb(self, stocklist):
        tree = self.stockTree
        tree.setHeaderLabels(['Stock No.', 'Stock Name'])
        header = tree.header()
        header.setDefaultSectionSize(100)
            
        root = QtWidgets.QTreeWidgetItem(tree)
        if self.pre_stocktype is 0:
            root.setText(0, '%s (%d)' % (CapitalStockGroup[self.stockgroup_num], len(stocklist)))
        else:
            root.setText(0, 'Group%s (%d)' % (self.stockgroup_num, len(stocklist)))

        for item in stocklist:
            head = QtWidgets.QTreeWidgetItem(root)
            head.setText(0, item[0])
            head.setText(1, item[1])
        tree.addTopLevelItem(root)

        self.stockgroup_num = self.stockgroup_num + 1
        
    def on_stocklist_change_cb(self, no):
        if self.pre_stocktype is not no:
            self.stockTree.clear()
            self.pre_stocktype = no
            self.stockgroup_num = 1
        else:
            return None

        self.semBtn.setChecked(False)
        self.otcBtn.setChecked(False)
        self.futuresBtn.setChecked(False)
        self.optionBtn.setChecked(False)
        self.esmBtn.setChecked(False)

        if no is 0:
            self.semBtn.setChecked(True)
        if no is 1:
            self.otcBtn.setChecked(True)
        if no is 2:
            self.futuresBtn.setChecked(True)
        if no is 3:
            self.optionBtn.setChecked(True)
        if no is 4:
            self.esmBtn.setChecked(True)
        self.agent.RequestStockList(no)

    def on_stocktree_dclicked_cb(self, item, column):
        if item.data(1, 0) is None:
            #Group Item, skip it
            return None
        
        self.msgBrowser.append('Start to Request %s(%s) KLine' % (item.data(1, 0), item.data(0, 0)))
        self.agent.requestkline_cb(item.data(0, 0))

#############################################################
# User Interface Callback
#############################################################
    def capitalLogin(self, checked):
        res = self.agent.Login(self.userIDLine.text(), self.passwordLine.text(), checked)
        if not res:
            self.connectBtn.setChecked(False)

if '__main__' in __name__:
    app = QtWidgets.QApplication(sys.argv)
    ui = CollectHistory()
    ui.show()
    sys.exit(app.exec_())
