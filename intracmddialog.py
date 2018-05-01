# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from intracmddialogui import Ui_Dialog

try:
    from PyQt5.QtCore import QString
except:
    QString = str

class intraCMD(QtWidgets.QDialog, Ui_Dialog):
    cmdTigger = QtCore.pyqtSignal(str)
    hideTigger = QtCore.pyqtSignal(bool)
    def __init__(self, parent=None):
        super(intraCMD, self).__init__(parent)
        self.setupUi(self)

        self.cmdLine.textChanged.connect(self.textchanged_cb)
        self.enterBtn.clicked.connect(self.enterCMD)

    def enterCMD(self, clicked):
        self.appendCMD2History()

    def textchanged_cb(self):
        cmd = self.cmdLine.toPlainText()
        if len(cmd) < 1:
            return None

        if cmd[-1] != '\n':
            return None

        self.enterCMD(True)

    def appendCMD2History(self):
        cmd = self.cmdLine.toPlainText()

        if len(cmd) < 1:
            return None

        self.cmdLine.clear()
        self.histroyBrowser.append(cmd)
        
        self.cmdTigger.emit(cmd)

    def hideEvent(self, event):
        hide = self.isVisible()
        self.hideTigger.emit(hide)

