#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets

try:
    from PyQt5.QtCore import QString
except:
    QString = str

import pyqtgraph as pg

class BarGraph(pg.BarGraphItem):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

    def mouseClickEvent(self, event):
        print('clicked')

