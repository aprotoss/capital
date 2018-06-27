# -*- coding: utf-8 -*-
#Qt
from capitalui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
try:
    from PyQt5.QtCore import QString
except:
    QString = str

from realtimeviewui import Ui_Form

class RealtimeView(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.setupUi(self)

        self.highLCD.display(1234)

    def setSKStock(self, pSKStock):
        #print('index: %d' % pSKStock.sStockIdx)
        #print('decimal: %d' % pSKStock.sDecimal)
        digit = pSKStock.sDecimal * 10
        self.highLCD.display(pSKStock.nHigh/digit)
        self.openLCD.display(pSKStock.nOpen/digit)
        self.lowLCD.display(pSKStock.nLow/digit)
        self.closeLCD.display(pSKStock.nClose/digit)
        self.tickqtyLCD.display(pSKStock.nTickQty/digit)
        #print(':: %s --> H: %s, O: %s, L: %s, C: %s' % (pSKStock.bstrStockNo, pSKStock.nHigh, pSKStock.nOpen, pSKStock.nLow, pSKStock.nClose))
