#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time

from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import pyqtSignal
from stkmultidownloaderui import *
from stkplot import *
from stkdata import *
from skcenter import *
from skreply import *
from skquote import *

SKCOMDLL = "C:\\capitalAPI\\DLL\\x64\\SKCOM.dll"

class stk_multidownloader(QDialog, Ui_Dialog):
    closed = pyqtSignal()  
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.stockslist = []
        self.stockdata = ""

        #basic dialog status
        self.close_pushButton.clicked.connect(self.close_pushButton_clickec_cb)
        self.destroyed.connect(self.close_pushButton_clickec_cb)
        self.rejected.connect(self._show_rejected_cb)

        #Capital
        self.capital_login_button.clicked.connect(self.capital_login_clicked_cb)

        #cb
        self.start_pushButton.clicked.connect(self.start_pushbutton_cliecked_cb)

        self.initial_skcom_object()

    def __del__(self):
        username = self.username_lineedit.text()
        self.skq.SKQuoteLib_LeaveMonitor()
        self.skr.SKReplyLib_SolaceCloseByID(username)

    def _show_rejected_cb(self):
        self.closed.emit()

    def close_pushButton_clickec_cb(self):
        self.closed.emit()

    def initial_skcom_object(self):
        CoInitialize()
        self.module = GetModule(SKCOMDLL)

        #SKCenter
        self.skc, self.skcEvents, self.skcConn = create_skcenter(self.module)
        #SKReply
        self.skr, self.skrEvents, self.skrConn = create_skreply(self.module)
        #SKQuote
        self.skq, self.skqEvents, self.skqConn = create_skquote(self.module)

        # var
        self.stockgroup_num = 0

        # SKCOM cb
        self.skqEvents.stocklist_ready.connect(self.skquote_stocklist_ready_cb)
        self.skqEvents.onnotifystocklist.connect(self.skquote_on_notify_stocklist_cb)
        self.skqEvents.onnotifyklinedata.connect(self.skquote_on_notify_kline_data_cb)
        #self.skqEvents.onnotifyquote.connect(self.skquote_on_notify_quote_cb)

    def capital_login_clicked_cb(self, checked):
        username = self.username_lineedit.text()
        password = self.password_lineedit.text()
        ret = self.skc.SKCenterLib_Login(username, password)
        if ret != 0:
            self.status_textEdit.append(f"Login Failed - {ret}")
            return False       
        self.status_textEdit.append("SKCenter - Login Successed")

        ret = self.skr.SKReplyLib_ConnectByID(username)
        if ret != 0:
            self.status_textEdit.append(f"Reply Connect Failed - {ret}")
            return False
        self.status_textEdit.append("SKReply - Connect Successed")

        ret = self.skq.SKQuoteLib_EnterMonitor()
        if ret != 0:
            self.status_textEdit.append(f"Quote Enter Monitor Failed - {ret}")
            return False
        self.status_textEdit.append("enterMonitor successed!!")
        return True
        
    def start_pushbutton_cliecked_cb(self, checked):
        if not checked:
            return None
        stocks = self.stocklist_plainTextEdit.toPlainText().split(',')
        total_stocks = len(stocks)
        if total_stocks == 0:
            self.status_textEdit.append("Please input stocks !!")
            return None

        preprogress = 1.0/total_stocks 
        for idx, stock in enumerate(stocks):
            name = "xxxx"
            for s in self.stockslist:
                ss = s.split(',')
                if stock == ss[0]:
                    name = ss[1]
                    break

            self.progressBar.setValue(int(preprogress * idx * 100))
            self.status_textEdit.append(f"Request KLine: {stock}-{name} ... !!")
            start = time.time()
            rst = self.skq.SKQuoteLib_RequestKLine(stock, 0, 1)
            if rst != 0:
                self.status_textEdit.append(f"Request KLine: {stock}-{name} failed, skip it!!")
                continue
            self._save_to_file_(f"./stkdata/{stock}-{name}.txt")
            end = time.time()
            self.status_textEdit.append(f"Request KLine: {stock}-{name} Successed ... {end - start} seconds !!")
            self.stockdata = ""

        self.progressBar.setValue(100) #finish

    def skquote_stocklist_ready_cb(self):
        self.skq.SKQuoteLib_RequestStockList(0)
        self.status_textEdit.append("Stock List Ready, You can start to download stock datas")
        self.start_pushButton.setEnabled(True)
        
    def skquote_on_notify_stocklist_cb(self, sMartketNo, bstrStockData):
        self.stockslist += bstrStockData.split(';')
    
    def skquote_on_notify_kline_data_cb(self, bstrStockNo, bstrData):
        #1101
        #2023/07/25 13:30, 37.40, 37.40, 37.40, 37.40, 1328
        self.stockdata += (bstrData + '\n')

    def _save_to_file_(self, filename):
        with open (filename, 'w') as f:
            f.write("Date,Open,High,Low,Close,Volume\n")
            f.write(self.stockdata)




