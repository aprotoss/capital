# -*- coding: utf-8 -*-
from capitalevent import *
from capitalcode import CapitalCode as SCode #STatus Code
from sklib import *
from threading import Thread
import sys
sys.coinit_flags = 0
import win32com
import win32event
import win32com.client
import pythoncom
import time

class Capital(Thread):
    def __init__(self):
        super(Capital, self).__init__()
        #Create COM Objects
        self.skcenter = win32com.client.DispatchWithEvents(CLSID_SKCenterLib, SKCenterLibEventsHandler)
        self.skreply  = win32com.client.DispatchWithEvents(CLSID_SKReplyLib, SKReplyLibEventsHandler)
        self.skquote = win32com.client.DispatchWithEvents(CLSID_SKQuoteLib, SKQuoteLibEventsHandler)
            
        self._running = False

    def run(self):
        print('[Capital] thread start...')
        self._running = True
        while self._running:
            time.sleep(0.1)
            pythoncom.PumpWaitingMessages()
        print('[Capital] thread stop...')

    def stop(self):
        self._running = False

    def setCMD(self, *args):
        res = None
        cls = None
        argv = []

        if args[0][:6] == 'SKCent':
            cls = self.skcenter

        if args[0][:6] == 'SKRepl':
            cls = self.skreply

        if args[0][:6] == 'SKQuot':
            cls = self.skquote

        if cls is None:
            print('Command: %s Error' % args[0])
            return None

        for arg in args[1:]:
            #str
            if arg[0] == '\'' and arg[-1] == '\'':
                argv.append(arg[1:-1])
                continue

            if arg == 'True':
                argv.append(True)
                continue
            
            if arg == 'False':
                argv.append(False)
                continue

            try:
                print('atoi ', arg)
                tmp = int(arg)
                argv.append(tmp)
            except:
                print('Argument convert error: %s' % arg)
                return None
        
        try:
            res = getattr(cls, args[0])(*argv)
        except:
            print('Command: %s Error - are you sure this command is current ?' % args[0])

        ##Reteval Command Result
        msg = SCode[res][1]
        if len(msg) is 0:
            msg = SCode[res][0]
        print(msg)



        




