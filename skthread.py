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
from config import *

#comtypes
from comtypes.client import GetModule
sys.coinit_flags = 0
from pythoncom import PumpWaitingMessages
from pythoncom import CoInitialize 

class SKThread(QtCore.QObject):
    module = GetModule(SKCOMDLL)
    message = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

    @QtCore.pyqtSlot()
    def process(self):
        CoInitialize()
        self._running = True
        while self._running:
            time.sleep(0.1)
            PumpWaitingMessages()
    
    def stop(self):
        self._running = False
