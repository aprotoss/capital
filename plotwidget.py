# -*- coding: utf-8 -*-
#Qt
from capitalui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
try:
    from PyQt5.QtCore import QString
except:
    QString = str
#sys
import pyqtgraph as pg

class PlotWidget(pg.GraphicsLayoutWidget):
    def __init__(self, *argv, **kargv):
        super(__class__, self).__init__(*argv, **kargv)

    def setData(self, data):
        pass
