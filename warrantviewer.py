# -*- coding: utf-8 -*-
from warrantviewerui import Ui_WarrantViewer
from warrantitem import WarrantItem
from config import *

#Qt
from PyQt5 import QtCore, QtGui, QtWidgets

try:
    from PyQt5.QtCore import QString
except:
    QString = str

import sys
from pathlib import Path

class WarrantViewer(QtWidgets.QMainWindow, Ui_WarrantViewer):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.setupUi(self)
        self.scanWarrantList()

        self.lineEdit.textEdited.connect(self.on_lineedit_textedited_cb)
        self.stockList.itemDoubleClicked.connect(self.on_stocklist_dclicked_cb)
        self.tabWidget.tabCloseRequested.connect(self.on_tabwidget_closerequest_cb)

    def scanWarrantList(self, prefix=''):
        self.stockList.clear()
        path = Path(WarrantPath)
        for wrt in path.glob(prefix + '*.wrt'):
            self.stockList.addItem(str(wrt).split('\\')[-1].split('.')[0])

    def on_lineedit_textedited_cb(self, text):
        self.scanWarrantList(str(text))

    def on_stocklist_dclicked_cb(self, item):
        self.lineEdit.setText(item.text())
        witem = WarrantItem()
        self.tabWidget.addTab(witem, item.text())
        witem.setData(WarrantPath + '/' + item.text() + '.wrt' )

    def on_tabwidget_closerequest_cb(self, index):
        self.tabWidget.removeTab(index)


#main
if '__main__' in __name__:
    app = QtWidgets.QApplication(sys.argv)
    ui = WarrantViewer()
    ui.show()
    sys.exit(app.exec_())
