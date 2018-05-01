# -*- coding: utf-8 -*-
from sklib import *
from capitalcode import CapitalCode as SCode #Status Code
from capitalcode import CapitalMarket

class SKCenterLibEventsHandler(SKCenterLibEvents):
    def OnTimer(self, nTime): 
        stime = str(nTime)
        print('[SKCenter] %s:%s:%s' % (stime[0:2], stime[2:4], stime[4:6]))

class SKOOQuoteLibEventsHandler(SKOOQuoteLibEvents):
    pass

class SKOSQuoteLibEventsHandler(SKOSQuoteLibEvents):
    pass


class SKOrderLibEventsHandler(SKOrderLibEvents):
    pass

class SKQuoteLibEventsHandler(SKQuoteLibEvents):
    def OnConnection(self, nKind, nCode):
        print('[SKQuote] OnConnection: %s - %s' % (SCode[nKind][1], SCode[nCode][1]))

    def OnNotifyServerTime(self, sHour, sMinute, sSecond, nTotal): 
        print('[SKQuote]: time: %2d:%2d:%2d %d' % (sHour, sMinute, sSecond, nTotal))
    
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
