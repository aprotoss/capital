# -*- coding: utf-8 -*-
#Capital
from intracmddialog import intraCMD
from capitalevent import *
from capitalcode import CapitalMarket
from capitalcode import CapitalCode as SCode #Status Code

#Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from capitalui import Ui_MainWindow

#system
from threading import Thread
from ctypes import *
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

class Capital(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Capital, self).__init__(parent)
        self.setupUi(self)

        #Develop Dialog
        self.devDialog = intraCMD(self)
        self.devDialog.cmdTigger.connect(self.setDevCMD)
        self.devDialog.show()
        self.actionIntraCMD.toggled.connect(self.on_intracmd_cb) 
        self.devDialog.hideTigger.connect(self.on_intracmd_cb)

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
            if res is not 0:
                self.connectBtn.setChecked(False)
                return None

            res = self.setCMD('SKReplyLib_ConnectByID', userID)
            self.msgBrowser.append('SKReplyLib_ConnectByID: ' + SCode[res][1])
            if res is not 0:
                self.connectBtn.setChecked(False)
                return None
            
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

    def timerkeeping_cb(self, strTime):
        self.statusbar.showMessage(strTime)
            
#main
if '__main__' in __name__:
    app = QtWidgets.QApplication(sys.argv)
    ui = Capital()
    ui.show()
    sys.exit(app.exec_())
