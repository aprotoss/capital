# -*- coding:utf-8 -*-
import sys
import time
from PyQt6 import QtCore
from skcode import *

#comtypes
from comtypes.client import GetModule
from comtypes.client import CreateObject
from comtypes.client import GetEvents
sys.coinit_flags = 0
from pythoncom import PumpWaitingMessages
from pythoncom import CoInitialize 

def create_skcenter(module):
    skc = CreateObject(module.SKCenterLib, interface=module.ISKCenterLib)
    skcEvents = SKCenterLibEvents()
    connect = GetEvents(skc, skcEvents)
    return skc, skcEvents, connect
        
class SKCenterLibEvents(object):
    def OnTimer(self, nTime): 
        stime = str(nTime)
        print(f"[SKCenter] {stime[:-4]}:{stime[-4:-2]}:{stime[-2:]}")
    
    def OnShowAgreement(self, bstrData): 
        print("SKCenterLibEvents: OnShowAgreement")
