# -*- coding: utf-8 -*-
from capitalevent import *
from capitalcode import CapitalCode as SCode #Status Code

from comtypes.client import GetModule
from comtypes.client import CreateObject
from comtypes.client import GetEvents

from threading import Thread
from ctypes import *
import sys
import time

sys.coinit_flags = 0
import pythoncom
from pythoncom import CoInitialize 
from pythoncom import CoInitializeEx
from pythoncom import CoUninitialize

class Capital(Thread):
    def __init__(self):
        super(Capital, self).__init__()
        self._running = False

    def setInitial(self):
        #Create COM Objects
        module = GetModule('./CapitalApi_2.13.11/API/x86/SKCOM.dll')
        self.skcenter = CreateObject(module.SKCenterLib, interface=module.ISKCenterLib)
        self.skreply = CreateObject(module.SKReplyLib, interface=module.ISKReplyLib)
        self.skquote = CreateObject(module.SKQuoteLib, interface=module.ISKQuoteLib)
        self.module = module
        
        self.skcenterevents = SKCenterLibEventsHandler()
        self.skreplyevents = SKReplyLibEventsHandler()
        self.skquoteevents = SKQuoteLibEventsHandler()

        self.centerConn = GetEvents(self.skcenter, self.skcenterevents)
        self.replyConn = GetEvents(self.skreply, self.skreplyevents)
        self.quoteConn = GetEvents(self.skquote, self.skquoteevents)

    def run(self):
        print('[Capital] thread start...')
        CoInitialize()
        self.setInitial()
        self._running = True
    
        while self._running:
            time.sleep(0.1)
            pythoncom.PumpWaitingMessages()
        print('[Capital] thread stop...')

    def stop(self):
        self._running = False
        CoUninitialize()

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

        return res


#    def setCMD(self, *args):
#        res = None
#        cls = None
#        struct = None
#        argv = []
#
#        if args[0][:6] == 'SKCent':
#            cls = self.skcenter
#
#        if args[0][:6] == 'SKRepl':
#            cls = self.skreply
#
#        if args[0][:6] == 'SKQuot':
#            cls = self.skquote
#        
#        if args[0][:6] == 'SKOOQu':
#            cls = self.skooquote
#        
#        if args[0][:6] == 'SKOSQu':
#            cls = self.skosquote
#        
#        if args[0][:6] == 'SKOrde':
#            cls = self.skorder
#
#        if cls is None:
#            print('Command: %s Error' % args[0])
#            return None
#
#        for arg in args[1:]:
#            #str
#            if arg[0] == '\'' and arg[-1] == '\'':
#                argv.append(arg[1:-1])
#                continue
#
#            #True
#            if arg == 'True':
#                argv.append(True)
#                continue
#            
#            #False
#            if arg == 'False':
#                argv.append(False)
#                continue
#
#            #*strcut
#            if arg[0] == '*':
#              struct = SKSTOCK()  
#              argv.append(pointer(struct))
#              continue
#
#            try:
#                print('atoi ', arg)
#                tmp = int(arg)
#                argv.append(tmp)
#            except:
#                print('Argument convert error: %s' % arg)
#                return None
#        
#        try:
#            res = getattr(cls, args[0])(*argv)
#        except:
#            print('Command: %s Error - are you sure this command is current ?' % args[0])
#
#        ##Reteval Command Result
#        msg = SCode[res][1]
#        if len(msg) is 0:
#            msg = SCode[res][0]
#        print(msg)
#
#        if struct is not None:
#            print(struct)
#
#    def test(self):
#        st = self.module.SKSTOCK()
#        o, res = self.skquote.SKQuoteLib_GetStockByNo('2303', st)
#        print(st)
#        print(res)
#        print(o)
#        #print(st.sStockidx)
#        print(st.bstrStockName)
#        print(st.nHigh)
#        print(st.nOpen)
#        print(st.nLow)
#        print(st.nClose)
#            
