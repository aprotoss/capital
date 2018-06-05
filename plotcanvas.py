# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from config import *

import pandas as pd
import pyqtgraph as pg
import numpy as np
from datetime import datetime
from numpy import arange, sin, pi

class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  ## data must have FIELD = ['Date','Open','High','Low','Close','Volume']
        self.showlength = 270 # 60 * 4.5hr (for one day K-Line)
        self.generatePicture()


    def setShowLength(self, length):
        self.showlength = length

    def generatePicture(self):
        ## pre-computing a QPicture object allows paint() to run much more quickly,
        ## rather than re-drawing the shapes every time.
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w', width=0.1))
        #w = (self.data[1][0] - self.data[0][0]) / 3.
        w1 = 0.05
        w2 = 0.33
        for idx, da in enumerate(self.data[-(self.showlength):]):

            if da[1] > da[4]:
                p.setBrush(pg.mkBrush('g'))
            elif da[1] == da[4]:
                p.setBrush(pg.mkBrush('w'))
            else:
                p.setBrush(pg.mkBrush('r'))

            p.drawRect(QtCore.QRectF(idx-w1, da[3], 0.1, da[2] - da[3]))
            p.drawRect(QtCore.QRectF(idx-w2, da[1], w2*2, da[4] - da[1]))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())

FIELD = ['Date','Open','High','Low','Close','Volume']
FIELDTYPES = {'Date': str, 'Open': np.float16, 'High':
        np.float16, 'Low': np.float16, 'Close': np.float16, 'Volume': np.int32}

#class plotWidget(QtWidgets.QGraphicsView):
class PlotCanvas(pg.PlotWidget):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, *argv, **kargv):
        super(__class__, self).__init__(*argv, **kargv)

    def plotKData(self, mins='1'):
        filename = StocksPath + '/' + self.stockno + '/' + self.stockno
        if mins not in ['1', '5', '30']:
            return None

        if mins == '1':
            filename += '.csv'
        else:
            filename += '.%smin' % mins

        print(filename)
        df = pd.read_csv(filename, names=FIELD, dtype=FIELDTYPES,
                parse_dates=['Date'])
            
        item = CandlestickItem(df.as_matrix(FIELD))
        self.addItem(item)

        hLimit = df['High'][df['High'].idxmax()]
        lLimit = df['Low'][df['Low'].idxmin()]

        self.disableAutoRange()
        self.setLimits(minXRange=10, maxXRange=300, yMin=(lLimit-2),
                yMax=(hLimit+2))

    def setStock(self, no):
        self.stockno = no
        self.plotKData('1')

