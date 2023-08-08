#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import glob, os

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTableWidgetItem, QTreeWidgetItem
from stkappui import *
from stkplot import *
#SKCOM API
from skcom import *
from stkdata import *
from skcenter import *
from skreply import *
from skquote import *
from stkmultidownloader import *

#comtypes
from comtypes.client import GetModule
sys.coinit_flags = 0
from pythoncom import CoInitialize

# Subclass QMainWindow to customize your application's main window
class stk_app(QMainWindow, Ui_MainWindow):
    skc = None
    skcEvents = None
    skcConn = None
    skr = None
    skrEvents = None
    skrConn = None
    skq = None
    skqEvents = None
    skqConn = None

    tabCurrentIndex = 0
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.scan_stkdata_folder()

        # element: "code": [name, fullname, stkplot, stkdata]
        self.tab_list = {}

        #register callback
        self.stkdata_tableview.cellClicked.connect(self.stkdata_tableview_clicked_cb)
        self.stkview_tab.tabCloseRequested.connect(self.stkview_tab_closerequest_cb)
        self.stkview_tab.currentChanged.connect(self.stkview_tab_current_changed_cb)
        self.capital_login_button.clicked.connect(self.capital_login_clicked_cb)
        self.stocklist_treeWidget.itemClicked.connect(self.stocklist_treewidget_item_clicked_cb)
        self.stocklist_tool_box.currentChanged.connect(self.stocklist_tool_box_currentChanged_cb)
        
        #  plotbox - callback
        self.plotbox_save_button.clicked.connect(self.plotbox_save_button_cb)
        self.mins_1_k_button.toggled.connect(self.mins_1_k_button_cb)
        self.mins_5_k_button.toggled.connect(self.mins_5_k_button_cb)
        self.mins_60_k_button.toggled.connect(self.mins_60_k_button_cb)
        self.mins_270_k_button.toggled.connect(self.mins_270_k_button_cb)
        self.tick_range_spinbox.valueChanged.connect(self.tick_range_spinbox_valueChanged_cb)
        self.turningwave_button.clicked.connect(self.turningwave_button_clicked_cb)
        self.sma5_checkBox.stateChanged.connect(self.sma5_checkBox_statechanged_cb)
        self.sma10_checkBox.stateChanged.connect(self.sma10_checkBox_statechanged_cb)
        self.sma20_checkBox.stateChanged.connect(self.sma20_checkBox_statechanged_cb)
        self.sma60_checkBox.stateChanged.connect(self.sma60_checkBox_statechanged_cb)

        # Menu
        self.actionFullscreen.triggered.connect(self.action_fullscreen_triggered_cb)
        ## System
        self.actionMultiDownloader.triggered.connect(self.action_multidownloader_triggered_cb)

        #initial SKCOMLib
        self.initial_skcom_object()

    def __del__(self):
        username = self.username_lineedit.text()
        self.skq.SKQuoteLib_LeaveMonitor()
        self.skr.SKReplyLib_SolaceCloseByID(username)

    def scan_stkdata_folder(self):
        # enter stkdata folder
        os.chdir("./stkdata")  
        files = glob.glob("*.txt")
        self.stkdata_tableview.setRowCount(len(files))
        for idx, file in enumerate(files):
            data = file.split('.')[0].split('-')
            self.stkdata_tableview.setItem(idx, 0, QTableWidgetItem(data[0]))
            self.stkdata_tableview.setItem(idx, 1, QTableWidgetItem(data[1]))
        #go-back to origianl folder
        os.chdir("../")  

    def create_new_stkview_tab(self, code, name):
        filename = f"./stkdata/{code}-{name}.txt"
        fullname = f"{code}-{name}"
        stkdata = StkData()
        stkdata.stk_id = fullname
        stkdata.read_csv(filename)
        stkplot = StkPlot()
        stkplot.stkdata = stkdata
        stkplot.draw()
        tab = self.stkview_tab.addTab(stkplot, fullname)
        self.tab_list[code] = [name, fullname, stkplot, stkdata]
        self.stkview_tab.setCurrentIndex(tab)

    #select a stock to show the plot <this is history stock data>
    def stkdata_tableview_clicked_cb(self, row, column):
        code = f"{self.stkdata_tableview.item(row, 0).text()}"
        name = f"{self.stkdata_tableview.item(row, 1).text()}"
        if code not in self.tab_list:
            self.create_new_stkview_tab(code, name)

    def stkview_tab_closerequest_cb(self, index):
        fullname = self.stkview_tab.tabText(index)
        code = fullname.split('-')[0]
        self.stkview_tab.removeTab(index)
        del self.tab_list[code]
    
    def stkview_tab_current_changed_cb(self, index):
        tab = self.stkview_tab
        self.tabCurrentIndex = tab.tabText(index).split('-')[0]
        selected = self.KLine_group.checkedButton().text()
        if selected == "1 mins":
            self.mins_1_k_button_cb(True)
        elif selected == "5 mins":
            self.mins_5_k_button_cb(True)
        elif selected == "60 mins":
            self.mins_60_k_button_cb(True)
        elif selected == "Day":
            self.mins_270_k_button_cb(True)

    def capital_login_clicked_cb(self, checked):
        username = self.username_lineedit.text()
        password = self.password_lineedit.text()
        ret = self.skc.SKCenterLib_Login(username, password)
        if ret != 0:
            self.statusbar.showMessage(f"Login Failed - {ret}")
            return False       
        self.statusbar.showMessage("SKCenter - Login Successed", 3000)

        ret = self.skr.SKReplyLib_ConnectByID(username)
        if ret != 0:
            self.statusbar.showMessage(f"Reply Connect Failed - {ret}")
            return False
        self.statusbar.showMessage("SKReply - Connect Successed", 3000)

        ret = self.skq.SKQuoteLib_EnterMonitor()
        if ret != 0:
            self.statusbar.showMessage(f"Quote Enter Monitor Failed - {ret}")
            return False
        self.statusbar.showMessage("enterMonitor successed!!", 3000)
        return True
    
    def stocklist_treewidget_item_clicked_cb(self, item, column):
        #This is not a stock number
        if item.childCount() != 0:
            return None
        #self.cache_list[item.text(0)] = item.text(1)
        code = item.text(0)
        name = item.text(1)
        
        if code in self.tab_list:
            return None

        fullname = f"{code}-{name}"
        stkdata = StkData()
        stkdata.stk_id = fullname
        stkplot = StkPlot()
        stkplot.stkdata = stkdata
        tab = self.stkview_tab.addTab(stkplot, fullname)
        self.stkview_tab.setCurrentIndex(tab)
        self.tab_list[code] = [name, fullname, stkplot, stkdata]
        #History
        # self.statusbar.showMessage(f"Request KLine data: {item.text(0)}")
        # rst = self.skq.SKQuoteLib_RequestKLine(code, 0, 1)
        # if rst != 0:
        #     self.statusbar.showMessage(f"Request KLine: {item.text(0)} failed !!", 5000)
        #     return None 
        #
        # self.statusbar.showMessage("Request KLine: {item.text(0)} Successed !!", 3000)
        # stkplot.draw()
        #Not make sure yet.
        page, rst = self.skq.SKQuoteLib_RequestStocks(-1, item.text(0))
        if rst == 0:
            print("SKQuoteLib_RequestStocks successed !!")
        else:
            print("SKQuoteLib_RequestStocks failed !!")

        page, rst = self.skq.SKQuoteLib_RequestTicks(-1, item.text(0))
        if rst == 0:
            print("SKQuoteLib_RequestStocks successed !!")
        else:
            print("SKQuoteLib_RequestStocks failed !!")
        
    def stocklist_tool_box_currentChanged_cb(self, index):
        if index == 0:
            self.scan_stkdata_folder()
    
    def plotbox_save_button_cb(self, checked):
        if len(self.tab_list) == 0:
            return None
        tab = self.tab_list[self.tabCurrentIndex]
        # element: "code": [name, fullname, stkplot, stkdata]
        print(self.KLine_group.checkedButton().text())
        tab[3].save_csv(f"./stkdata/{tab[1]}.txt")
        self.statusbar.showMessage(f"Save - {tab[1]} - Done", 5000)
        
    def mins_1_k_button_cb(self, checked):
        if not checked or len(self.tab_list) == 0:
            return None
        self._mins_k_switch_("T")
    
    def mins_5_k_button_cb(self, checked):
        if not checked or len(self.tab_list) == 0:
            return None
        self._mins_k_switch_("5T")
    
    def mins_60_k_button_cb(self, checked):
        if not checked or len(self.tab_list) == 0:
            return None
        self._mins_k_switch_("60T")
    
    def mins_270_k_button_cb(self, checked):
        if not checked or len(self.tab_list) == 0:
            return None
        self._mins_k_switch_("1D")

    def _mins_k_switch_(self, ktype):
        tab = self.tab_list[self.tabCurrentIndex]
        tab[3].switch_K_type(ktype)
        tab[2].draw()
        
    def tick_range_spinbox_valueChanged_cb(self, arg__1):
        if len(self.tab_list) == 0:
            return None
        tab = self.tab_list[self.tabCurrentIndex]
        if arg__1 > len(tab[3].stk_data):
            self.tick_range_spinbox.setValue(len(tab[3].stk_data))
            return None
        tab[2].tick_range = arg__1
        tab[2].draw()

    def sma5_checkBox_statechanged_cb(self, arg__1):
        if len(self.tab_list) == 0:
            return None
        tab = self.tab_list[self.tabCurrentIndex]
        if arg__1 == 0:
            tab[2].draw_SMA5 = False
        if arg__1 == 2:
            tab[2].draw_SMA5 = True
        tab[2].draw()
        
    def sma10_checkBox_statechanged_cb(self, arg__1):
        if len(self.tab_list) == 0:
            return None
        tab = self.tab_list[self.tabCurrentIndex]
        if arg__1 == 0:
            tab[2].draw_SMA10 = False
        if arg__1 == 2:
            tab[2].draw_SMA10 = True
        tab[2].draw()
    
    def sma20_checkBox_statechanged_cb(self, arg__1):
        if len(self.tab_list) == 0:
            return None
        tab = self.tab_list[self.tabCurrentIndex]
        if arg__1 == 0:
            tab[2].draw_SMA20 = False
        if arg__1 == 2:
            tab[2].draw_SMA20 = True
        tab[2].draw()
    
    def sma60_checkBox_statechanged_cb(self, arg__1):
        if len(self.tab_list) == 0:
            return None
        tab = self.tab_list[self.tabCurrentIndex]
        if arg__1 == 0:
            tab[2].draw_SMA60 = False
        if arg__1 == 2:
            tab[2].draw_SMA60 = True
        tab[2].draw()
    
    def action_fullscreen_triggered_cb(self, checkable):
        if checkable:
            self.showFullScreen()
        else:
            self.showNormal()
    
    def action_multidownloader_triggered_cb(self, checkable):
        self.stkmdl = stk_multidownloader(self)
        self.stkmdl.setWindowTitle("Multi-Downloader")
        self.stkmdl.closed.connect(self.action_multidownloader_closed_cb)
        self.statusbar.showMessage("Multi-Downloader running")
        self.stkmdl.exec()
    
    def action_multidownloader_closed_cb(self):
        self.actionMultiDownloader.setCheckable(False)
        self.statusbar.showMessage("Multi-Downloader stopped", 3000)
        self.stkmdl.close()
        try:
            del(self.stkmdl)
        except:
            print("~~ No Object ~~")
        self.scan_stkdata_folder()


    ###################################
    # SKCOM 
    ###################################
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
        self.skqEvents.onnotifyquote.connect(self.skquote_on_notify_quote_cb)
        #self.skqEvents.onnotifyticks
    
        #Every new Group retrieved, this function will be called again
        #use stockgroup_num to point the group name from stockgroup_num
    def skquote_on_notify_stocklist_cb(self, sMarketNo, bstrStockData):
        count = 0
        root = QTreeWidgetItem(self.stocklist_treeWidget)
        for s in bstrStockData.split(';'):
            if len(s) == 0:
                continue
            item = s.split(',')          
            head = QTreeWidgetItem(root)
            head.setText(0, item[0])
            head.setText(1, item[1])
            count += 1

        # this is Group Stock, Stock Group Name in skcode
        if sMarketNo == 0:
            root.setText(0, f"{SKStockGroup[self.stockgroup_num]} ({count})")
        else:
            root.setText(0, "Group{self.stockgroup_num} ({count})")
        self.stocklist_treeWidget.addTopLevelItem(root)
        self.stockgroup_num += 1
        
    def skquote_stocklist_ready_cb(self):
        self.skq.SKQuoteLib_RequestStockList(0)
    
    def skquote_on_notify_kline_data_cb(self, bstrStockNo, bstrData):
        #1101
        #2023/07/25 13:30, 37.40, 37.40, 37.40, 37.40, 1328
        s = bstrData.split(',')
        data = [s[0], float(s[1]), float(s[2]), float(s[3]), float(s[4]), int(s[5])]
        stkdata = self.tab_list[bstrStockNo][3]
        stkdata.concat_row(data)
    
    def skquote_on_notify_quote_cb(self, sMarketNo, sStockIdx):
        psks = self.module.SKSTOCK()
        psks, ret = self.skq.SKQuoteLib_GetStockByIndex(sMarketNo, sStockIdx, psks)
        print(f"[skquote_on_notify_quote_cb] ret = {ret}")
        print(f"{psks.bstrStockName} - {psks.nHigh}, {psks.nOpen}, {psks.nClose}")

    #show message to statusbar 
    def on_statusbar_message_cb(self, message):
        self.statusbar.showMessage(message, 3000)
                                                      
if __name__ == "__main__":
    app = QApplication(sys.argv)
    stkapp = stk_app()
    stkapp.show()

    app.exec()
