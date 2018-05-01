# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from capitalui import Ui_MainWindow

from capital import Capital
from capitalcode import CapitalCode as SCode #Status Code

import sys
import time

try:
    from PyQt5.QtCore import QString
except:
    QString = str

class CapitalMain(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(CapitalMain, self).__init__(parent)
        self.setupUi(self)

        self.capital = Capital()
        self.capital.start()

        self.connectBtn.clicked.connect(self.capitalLogin)

    def capitalLogin(self, checked):
        userID = self.userIDLine.text()
        pwd = self.passwordLine.text()
        if checked:
            res = self.capital.setCMD('SKCenterLib_Login', userID, pwd)
            self.statusbar.showMessage('SKCenterLib_Login: ' + SCode[res][1])
            if res is not 0:
                self.connectBtn.setChecked(False)
                return None

            res = self.capital.setCMD('SKReplyLib_ConnectByID', userID)
            self.statusbar.showMessage('SKReplyLib_ConnectByID: ' + SCode[res][1])
            if res is not 0:
                self.connectBtn.setChecked(False)
                return None
            
            res = self.capital.setCMD('SKQuoteLib_EnterMonitor')
            self.statusbar.showMessage('SKQuoteLib_EnterMonitor: ' + SCode[res][1])
            if res is not 0:
                self.connectBtn.setChecked(False)
                return None
        else:
            res = self.capital.setCMD('SKQuoteLib_LeaveMonitor')
            self.statusbar.showMessage('SKQuoteLib_LeaveMonitor: ' + SCode[res][1])
            if res is not 0:
                self.connectBtn.setChecked(False)
                return None
            
            res = self.capital.setCMD('SKReplyLib_CloseByID',  userID)
            self.statusbar.showMessage('SKReplyLib_closeByID: ' + SCode[res][1])
            if res is not 0:
                self.connectBtn.setChecked(False)
                return None

    def closeEvent(self, event):
        self.capitalLogin(False)
        self.capital.stop()
            
#main
if '__main__' in __name__:
    app = QtWidgets.QApplication(sys.argv)
    ui = CapitalMain()
    ui.show()
    sys.exit(app.exec_())
