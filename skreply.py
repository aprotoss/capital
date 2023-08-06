# -*- coding:utf-8 -*-
import sys
import time

from PyQt6 import QtCore
from skcode import *

#comtypes
from comtypes.client import CreateObject
from comtypes.client import GetEvents
sys.coinit_flags = 0
from pythoncom import CoInitialize 

def create_skreply(module):
    skr = CreateObject(module.SKReplyLib, interface=module.ISKReplyLib)
    skrEvents = SKReplyLibEvents()
    connect = GetEvents(skr, skrEvents)
    return skr, skrEvents, connect

class SKReplyLibEvents(QtCore.QObject):
    def OnConnect(self, bstrUserID, nErrorCode):
        print(f"[SKReply] OnConnect: {bstrUserID} - {nErrorCode}")
    
    def OnDisconnect(self, bstrUserID, nErrorCode): 
        print(f"[SKReply] OnDisConnect: {bstrUserID} - {nErrorCode}")

    def OnComplete(self, bstrUserID):
        print(f"[SKReply] OnComplete: {bstrUserID}")
    
    def OnReplyMessage(self,bstrUserID, bstrMessages):
        print(f"[SKReply] OnReplyMessage: {bstrUserID} - {bstrMessages}")
        sConfirmCode = -1
        return sConfirmCode

    def OnReplyClear(self, bstrUserID, bstrMarket):
        print(f"[SKReply] OnReplyClear: {bstrUserID} - {bstrMarket}")

    def OnSolaceReplyDisconnect(self, bstrUserID, nErrorCode): 
        try:
            errcode = SCode[nErrorCode][1]
            if len(errcode) < 1:
                errcode = SCode[nErrorCode][0]
            print(f"[SKReply] {bstrUserID} - solace reply disconnect {nErrorCode} ")
        except:
            print(f"[SKReply] {bstrUserID} - solace reply disconnect ErrorCode out of Range {nErrorCode}")

    def OnSolaceReplyConnection(self, bstrUserID, nErrorCode):
        errcode = SKCode[nErrorCode][1]
        if len(errcode) < 1:
            errcode = SCode[nErrorCode][0]
        print(f"[SKReply] {bstrUserID} - solace reply connect {nErrorCode} ")

    def OnReplyClearMessage(self, bstrUserID):
        print(f"[SKReply] OnReplyClearMessage - {bstrUserID}")
