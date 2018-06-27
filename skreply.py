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
from skcode import *

#comtypes
from comtypes.client import CreateObject
from comtypes.client import GetEvents
sys.coinit_flags = 0
from pythoncom import PumpWaitingMessages
from pythoncom import CoInitialize 

class SKReply(SKThread):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        #Create COM Object
        self.skreply = CreateObject(self.module.SKReplyLib, interface=self.module.ISKReplyLib)
        #create COM Event
        self.skreplyevents = SKReplyLibEvents()
        #To regist COM Event to COM Object
        self.replyConn = GetEvents(self.skreply, self.skreplyevents)

        #Events
        self.skreplyevents.onconnect.connect(self.on_onconnect_cb)
        self.skreplyevents.ondisconnect.connect(self.on_ondisconnect_cb)
        self.skreplyevents.oncomplete.connect(self.on_oncomplete_cb)

    def connectByID(self, userID):
        ret = self.skreply.SKReplyLib_ConnectByID(userID)
        if ret == 0:
            self.message.emit('[SKReply] ConnectByID success')
            return True
        
        self.message.emit('[SKReply %d] %s' % (ret, SKCode[ret][1]))
        return False

    def closeByID(self, userID):
        ret = self.skreply.SKReplyLib_CloseByID(userID)
        if ret == 0:
            self.message.emit('[SKReply] CloseByID success')
            return True

        self.message.emit('[SKReply %d] %s' % (ret, SKCode[ret][1]))
        return False

    def on_onconnect_cb(self, bstrUserID, nErrorCode):
        if nErrorCode == 0:
            self.message.emit('[SKReply] connect success')
        else:
            errcode = SKCode[nErrorCode][1]
            if len(errcode) < 1:
                errcode = SCode[nErrorCode][0]
            self.message.emit('[SKReply %d] %s - connect %s ' % (nErrorCode, bstrUserID, errcode))

    def on_ondisconnect_cb(self, bstrUserID, nErrorCode):
        if nErrorCode == 0:
            self.message.emit('[SKReply] Disconnect success')
        else:
            try:
                errcode = SKCode[nErrorCode][1]
                if len(errcode) < 1:
                    errcode = SCode[nErrorCode][0]
                print('[SKReply] %s - disconnect %s ' % (bstrUserID, errcode))
            except:
                print('[SKReply] %s - disconnect ErrorCode out of Range %d' % (bstrUserID, nErrorCode))

    def on_oncomplete_cb(self, bstrUserID):
        self.message.emit('[SKReply] %s On Complete success' % bstrUserID)

class SKReplyLibEvents(QtCore.QObject):
    onconnect = QtCore.pyqtSignal(str, int)
    ondisconnect = QtCore.pyqtSignal(str, int)
    oncomplete = QtCore.pyqtSignal(str)
    def OnConnect(self, bstrUserID, nErrorCode):
        self.onconnect.emit(bstrUserID, nErrorCode)
    
    def OnDisconnect(self, bstrUserID, nErrorCode): 
        self.ondisconnect.emit(bstrUserID, nErrorCode)

    def OnComplete(self, bstrUserID):
        self.oncomplete.emit(bstrUserID)

    def OnData(self, bstrUserID, bstrData): 
        print('[SKReply] %s - %s' % (bstrUserID, bstrData))
    
    def OnSolaceReplyConnection(self, bstrUserID, nErrorCode): 
        errcode = SKCode[nErrorCode][1]
        if len(errcode) < 1:
            errcode = SCode[nErrorCode][0]
        print('[SKReply] %s - solace reply connect %s ' % (bstrUserID, errcode))

    def OnSolaceReplyDisconnect(self, bstrUserID, nErrorCode): 
        try:
            errcode = SCode[nErrorCode][1]
            if len(errcode) < 1:
                errcode = SCode[nErrorCode][0]
            print('[SKReply] %s - solace reply disconnect %s ' % (bstrUserID, errcode))
        except:
            print('[SKReply] %s - solace reply disconnect ErrorCode out of Range %d' % (bstrUserID, nErrorCode))
