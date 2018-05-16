# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import pandas as pd
from numpy import arange, sin, pi

class plotCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=8, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        #self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plotKData(self, df):
        #print(df)
        x = pd.to_datetime(df['Date'])
        y = pd.to_numeric(df['Open'])

        ax = self.figure.add_subplot(111)

        #for tick in ax.get_xticklabels():
        #    tick.set_rotation(23)
        ax.set_xticklabels(x, rotation=23)

        mpf.candlestick2_ochl(ax, df['Open'], df['Close'], df['High'],
                df['Low'], width=0.5, colorup='r', colordown='green', alpha=0.6)
       
#        ax.plot(x, y)
        self.draw()
