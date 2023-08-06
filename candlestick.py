#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt6 import QtCore, QtGui, QtWidgets

import pyqtgraph as pg

class Candlestick(pg.GraphicsObject):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self._boardcolor = (255, 255, 255, 128)

    def setBoardColor(self, color):
        self._boardcolor = color

    def generateDraw(self, data):
        self.data = data  ## data must have fields: time, open, close, min, max
        ## pre-computing a QPicture object allows paint() to run much more quickly, 
        ## rather than re-drawing the shapes every time.
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen(self._boardcolor))
        w = (self.data[1][0] - self.data[0][0]) / 3.
        for (t, open, close, min, max) in self.data:
            if min != max: 
                p.drawLine(QtCore.QPointF(t, min), QtCore.QPointF(t, max))
            if open > close:
                p.setBrush(pg.mkBrush('g'))
            else:
                p.setBrush(pg.mkBrush('r'))
            p.drawRect(QtCore.QRectF(t-w, open, w*2, close-open))
        p.end()
    
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())
