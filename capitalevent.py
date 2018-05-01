# -*- coding: utf-8 -*-
from sklib import *
from capitalcode import CapitalCode as SCode #Status Code
from capitalcode import CapitalMarket

from PyQt5 import QtCore

try:
    from PyQt5.QtCore import QString
except:
    QString = str

class SKCenterLibEventsHandler(SKCenterLibEvents, QtCore.QObject):
    ontimer = QtCore.pyqtSignal(str)
    def OnTimer(self, nTime): 
        stime = str(nTime)
        self.ontimer.emit('[SKCenter] %s:%s:%s' % (stime[0:2], stime[2:4], stime[4:6]))

class SKOOQuoteLibEventsHandler(SKOOQuoteLibEvents):
    pass

class SKOSQuoteLibEventsHandler(SKOSQuoteLibEvents):
    pass


class SKOrderLibEventsHandler(SKOrderLibEvents):
    pass

class SKQuoteLibEventsHandler(SKQuoteLibEvents, QtCore.QObject):
    #signal
    onconnection = QtCore.pyqtSignal(int, int)
    onnotifyservertime = QtCore.pyqtSignal(str)
    onnotifystocklist = QtCore.pyqtSignal(int, str)

    def OnConnection(self, nKind, nCode):
        print('[SKQuote] OnConnection: %s - %s' % (SCode[nKind][1], SCode[nCode][1]))
        #self.onconnection.emit(nKind, nCode)

    def OnNotifyServerTime(self, sHour, sMinute, sSecond, nTotal): 
        onnotifyservertime = QtCore.pyqtSignal(str)
        #print('[SKQuote] time: %2d:%2d:%2d %d' % (sHour, sMinute, sSecond, nTotal))
        self.onnotifyservertime.emit('[SKQuote] time: %2d:%2d:%2d %d' % (sHour, sMinute, sSecond, nTotal))
    
    def OnNotifyStockList(self, sMarketNo, bstrStockData):
        print('[SKQuote]: %s - %s' % (CapitalMarket[sMarketNo], bstrStockData))

class SKReplyLibEventsHandler(SKReplyLibEvents):
    def OnConnect(self, bstrUserID, nErrorCode):
        errcode = SCode[nErrorCode][1]
        if len(errcode) < 1:
            errcode = SCode[nErrorCode][0]
        print('[SKReply] %s - connect %s ' % (bstrUserID, errcode))
    
    def OnDisconnect(self, bstrUserID, nErrorCode): 
        try:
            errcode = SCode[nErrorCode][1]
            if len(errcode) < 1:
                errcode = SCode[nErrorCode][0]
            print('[SKReply] %s - disconnect %s ' % (bstrUserID, errcode))
        except:
            print('[SKReply] %s - disconnect ErrorCode out of Range %d' % (bstrUserID, nErrorCode))

    def OnData(self, bstrUserID, bstrData): 
        print('[SKReply] %s - %s' % (bstrUserID, bstrData))
    
    def OnSolaceReplyConnection(self, bstrUserID, nErrorCode): 
        errcode = SCode[nErrorCode][1]
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
