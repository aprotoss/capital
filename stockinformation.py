# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from stockinformationui import Ui_Form
from plotcanvas import plotCanvas
import numpy as np
import pandas as pd

try:
    from PyQt5.QtCore import QString
except:
    QString = str

class stockInformation(QtWidgets.QDialog, Ui_Form):
    def __init__(self, parent=None):
        super(stockInformation, self).__init__(parent)
        self.setupUi(self)
        self.createCanvas()

    def createCanvas(self):
        widget = self.getStockCanvas()
        canvas = plotCanvas(widget, width=5, height=4)
        self.canvas = canvas

    def getTextBrowser(self):
        return self.stockTBrowser

    def getStockCanvas(self):
        return self.stockCanvas

    def plotStockData(self, data):
        df = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
        self.canvas.plotKData(df)
        print(df)
