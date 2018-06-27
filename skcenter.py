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
from config import *
from skcode import *

#comtypes
from comtypes.client import CreateObject
from comtypes.client import GetEvents
sys.coinit_flags = 0
from pythoncom import PumpWaitingMessages
from pythoncom import CoInitialize 

class SKCenter(SKThread):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        #Create COM Object
        self.skcenter = CreateObject(self.module.SKCenterLib, interface=self.module.ISKCenterLib)
        #create COM Event
        self.skcenterevents = SKCenterLibEvents()
        #To regist COM Event to COM Object
        self.centerConn = GetEvents(self.skcenter, self.skcenterevents)

        self.skcenter.SKCenterLib_SetLogPath(SKLogPath)

        #Event
        self.skcenterevents.ontimer.connect(self.on_ontimer_cb)

    def login(self, bstrUserID, bstrPassword):
        ret = self.skcenter.SKCenterLib_Login(bstrUserID, bstrPassword) 
        if ret == 0:
            self.message.emit('[SKCenter] Login success')
            return True
        
        self.message.emit('[SKCenter: %d] %s' % (ret, SKCode[ret][1]))
        return False

    def on_ontimer_cb(self, msg):
        self.message.emit(msg)
        
class SKCenterLibEvents(QtCore.QObject):
    ontimer = QtCore.pyqtSignal(str)
    def OnTimer(self, nTime): 
        stime = str(nTime)
        self.ontimer.emit('[SKCenter] %s:%s:%s' % (stime[:-4], stime[-4:-2], stime[-2:]))
    
    def OnShowAgreement(self, bstrData): 
        print('SKCenterLibEvents: OnShowAgreement')


