# -*- coding: utf-8 -*-
from historyviewerui import Ui_MainWindow
from plotcanvas import PlotCanvas
from config import *

#Qt
from PyQt5 import QtCore, QtGui, QtWidgets

try:
    from PyQt5.QtCore import QString
except:
    QString = str

#system
import sys
import glob

class HistoryViewer(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.setupUi(self)

        #tabWidget
        self.stockTab.tabCloseRequested.connect(self.on_stocktab_close_cb)

        #treeWidget
        self.stockTree.itemDoubleClicked.connect(self.on_stocktree_dclicked_cb)
        self.setStockList(self.parseStockList())

    def parseStockList(self):
        tmp = []
        for s in glob.glob(StocksPath + '/*'):
            tmp.append(s.split('\\')[1])
        return tmp

    def setStockList(self, stocklist):
        tree = self.stockTree
        tree.clear()
        tree.setHeaderLabels(['Stock No.', 'Stock Name'])
        header = tree.header()
        header.setDefaultSectionSize(100)
            
        for item in stocklist:
            root = QtWidgets.QTreeWidgetItem(tree)
            root.setText(0, item)
            tree.addTopLevelItem(root)

    def on_stocktree_dclicked_cb(self, item, column):
        canvas = PlotCanvas(title=item.text(0))
        canvas.setStock(item.text(0))
        idx = self.stockTab.addTab(canvas, item.text(0))
        self.stockTab.setCurrentIndex(idx)
        
    def on_stocktab_close_cb(self, idx):
        wid = self.stockTab.widget(idx)
        self.stockTab.removeTab(idx)
        del wid

#main
if '__main__' in __name__:
    app = QtWidgets.QApplication(sys.argv)
    ui = HistoryViewer()
    ui.show()
    sys.exit(app.exec_())
