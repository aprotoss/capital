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
        self.getstockklineTimer.start(5000)  #5 seconds
        
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


#main
if '__main__' in __name__:
    app = QtWidgets.QApplication(sys.argv)
    ui = Capital()
    ui.show()
    sys.exit(app.exec_())
