#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt6 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import numpy as np
import traceback
import talib
from talib import abstract
from candlestick import *
from bargraph import *

class StkPlot(pg.GraphicsLayoutWidget):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.setWindowTitle('Stk View')
        self._stkdata = None
        self._tick_range = 100
        self.candlestick = None
        self.bar = None
        self.rsiItem = None
        self._sma = 10
        self.plot1 = self.addPlot(title = 'Plot 1', row=0, col=0)
        self.plot2 = self.addPlot(title = 'Plot 2', row=1, col=0)

        self.label = pg.LabelItem(justify="right", col=1)
        self.addItem(self.label)

        self.set_default_color()
        self.set_default_draw()

    def set_default_color(self):
        #palette
        self._color_KLineBoard = (192, 191, 188, 255)
        self._color_SMA = (220, 138, 221, 79)
        self._color_Volume = (28, 113, 216, 128)
        self._color_RSI_up = (248, 228, 92, 255)
        self._color_RSI_down = (87, 227, 137, 255)
        self._color_K = (246, 97, 81, 255)
        self._color_D = (220, 138, 221, 255)
        self._color_BBands_upper = (248, 228, 92, 180)
        self._color_BBands_lower = (255, 163, 72, 180)

    def set_default_draw(self):
        self._draw_KLine = True
        self._draw_SMA = True
        self._draw_RSI = True
        self._draw_Volume = True
        self._draw_KD = True
        self._draw_BBands = True

    def calculate_values(self):
        #KLine // a.k.a Candlestick
        #print(self._stkdata.stk_data)
        self._ticks = self._stkdata.stk_data.tail(self._tick_range)

        #SMA
        s = self._stkdata.SMA(self._sma)
        self._sma_ticks = s[f"SMA_{self._sma}"].tail(self._tick_range).reset_index(drop=True)

        #BBands
        self._bbands_ticks = self._stkdata.BBands(10, 2).reset_index(drop=True)
        self._bbands_upper_ticks = self._bbands_ticks["upper"].tail(self._tick_range).reset_index(drop=True)
        self._bbands_middle_ticks = self._bbands_ticks["middle"].tail(self._tick_range).reset_index(drop=True)
        self._bbands_lower_ticks = self._bbands_ticks["lower"].tail(self._tick_range).reset_index(drop=True)
        
        #Volume
        self._volume = self._stkdata._stkdata['Volume'].tail(self._tick_range).reset_index(drop=True)

        #RSI
        rsi = self._stkdata.RSI().reset_index(drop=True)
        self._rsi_up = rsi["Up"].tail(self._tick_range).reset_index(drop=True)
        self._rsi_down = rsi["Down"].tail(self._tick_range).reset_index(drop=True)
        
        #KD
        kd = self._stkdata.KD()
        self._kd_k = kd["K"].tail(self._tick_range).reset_index(drop=True)
        self._kd_d = kd["D"].tail(self._tick_range).reset_index(drop=True)

    def draw(self):
        if self._stkdata is None:
            return None

        self.calculate_values()

        #set X range
        self.plot1.setXRange(0, self._tick_range)
        self.plot2.setXRange(0, self._tick_range)
        self.plot1.clear()
        self.plot2.clear()

        self.plot1.setTitle('Candlestick')
        self.plot2.setTitle('Volume - RSI - KD')

        #plot 1
        if self._draw_KLine:
            self.draw_candlestick()
        if self._draw_SMA:
            self.draw_SMA_()
        if self._draw_BBands:
            self.draw_BBands_()

        #plot 2
        if self._draw_Volume:
            self.draw_Volume_()

        if self._draw_RSI:
            self.draw_RSI_()

        if self._draw_KD:
            self.draw_KD_()

        #crosshair
        self.setCrossLine()

    #
    # Draw @ Plot 1
    #
    def draw_candlestick(self):
        #example - candlestick
        self.candlestick = Candlestick()
        self.candlestick.setBoardColor(self._color_KLineBoard)
        df = []
        for i, d in enumerate(self._ticks.iloc):
            df.append((i, d['Open'], d['Close'], d['High'], d['Low']))

        maxY = self._ticks["High"].max() 
        minY = self._ticks["Low"].min()

        self.candlestick.generateDraw(df)
        self.plot1.addItem(self.candlestick)
        self.plot1.setYRange(maxY, minY)
    
    def draw_SMA_(self):
        self.plot1.plot(self._sma_ticks, pen=pg.mkPen(self._color_SMA))
        
    def draw_BBands_(self):
        self.plot1.plot(self._bbands_upper_ticks, pen=pg.mkPen(self._color_BBands_upper))
        #middle use SMA to replace
        self.plot1.plot(self._bbands_middle_ticks, pen='w')
        self.plot1.plot(self._bbands_lower_ticks, pen=pg.mkPen(self._color_BBands_lower))
        
        maxY = self._bbands_upper_ticks.max()
        minY = self._bbands_lower_ticks.min()
        self.plot1.setYRange(maxY, minY)

    #
    # Draw @ Plot 2
    #
    def draw_Volume_(self):
        if self._stkdata is None:
            return None
        #example - bargraph
        x = np.arange(self._tick_range)
        y = (self._volume / self._volume.max()) * 100
        self.bar = pg.BarGraphItem(x=x, height=y, width=0.5, brush=self._color_Volume)
        self.plot2.addItem(self.bar)

    def draw_RSI_(self, timeperiodU = 10, timeperiodD = 5):
        #rsi = self._stkdata.RSI().reset_index()
        self.plot2.plot(self._rsi_up, pen=pg.mkPen(self._color_RSI_up))
        self.plot2.plot(self._rsi_down, pen=pg.mkPen(self._color_RSI_down))

    def draw_KD_(self):
        kd = self._stkdata.KD()
        #print(kd)
        self.plot2.plot(self._kd_k, pen=pg.mkPen(self._color_K))
        self.plot2.plot(self._kd_d, pen=pg.mkPen(self._color_D))

    #
    # Auxiliary
    #
    def setCrossLine(self):
        self.move_slot = pg.SignalProxy(self.plot1.scene().sigMouseMoved, rateLimit=60, slot=self.moveSlot)
        self.move_slot = pg.SignalProxy(self.plot2.scene().sigMouseMoved, rateLimit=60, slot=self.moveSlot)
        self.vLine1 = pg.InfiniteLine(angle=90, movable=False)
        self.vLine2 = pg.InfiniteLine(angle=90, movable=False)
        self.plot1.addItem(self.vLine1, ignoreBounds=True)
        self.plot2.addItem(self.vLine2, ignoreBounds=True)

    def moveSlot(self, event=None):
        pos = event[0]
        plot = None
        if self.candlestick is not None:
            plot = self.candlestick
        if self.bar is not None:
            plot = self.bar
        if self.rsiItem is not None:
            plot = self.rsiItem[0]

        index = 0
        if self.plot1.sceneBoundingRect().contains(pos):
            mousePoint = self.plot1.vb.mapSceneToView(pos)
            index = int(mousePoint.x())
        if self.plot2.sceneBoundingRect().contains(pos):
            mousePoint = self.plot2.vb.mapSceneToView(pos)
            index = int(mousePoint.x())

        if -1 < index < self._tick_range:
            self.vLine1.setPos(index)
            self.vLine2.setPos(index)
            #Date: 2023-04-24 00:00:00
            #-------------------------
            self.label.setText(f"<div> <p> Date: {self._ticks.iloc[index][0]} </p>\
                <p>Open : {self._ticks.iloc[index][1]:.3f}</p>\
                <P>High : {self._ticks.iloc[index][2]:.3f}</p>\
                <P>Low  : {self._ticks.iloc[index][3]:.3f}</p>\
                <P>Close: {self._ticks.iloc[index][4]:.3f}</p>\
                <p>Volum: {self._volume.iloc[index]}</p>\
                <p>--------- SMA -----------</p>\
                <p>SMA_{self._sma} {self._sma_ticks.iloc[index]:.3f}\
                <p>--------- BBands --------</p>\
                <p>UPPER: {self._bbands_upper_ticks.iloc[index]:.3f} </p>\
                <p>MIDDL: {self._bbands_middle_ticks.iloc[index]:.3f} </p>\
                <p>LOWER: {self._bbands_lower_ticks.iloc[index]:.3f} </p>\
                <p>--------- KD ------------</p>\
                <p>K: {self._kd_k.iloc[index]:.3f} </p>\
                <p>D: {self._kd_d.iloc[index]:.3f} </p>\
                <p>--------- RSI -----------</p>\
                <p>UP  : {self._rsi_up.iloc[index]:.3f} </p>\
                <p>DOWN: {self._rsi_down.iloc[index]:.3f} </p>\
                </div>")

    #
    # Properties
    #
    @property
    def stkdata(self):
        return self._stkdata
    @stkdata.setter
    def stkdata(self, stkdata):
        self._stkdata = stkdata

    @property
    def tick_range(self):
        return self._tick_range
    @tick_range.setter
    def tick_range(self, rng):
        self._tick_range = rng   

    @property
    def sma(self):
        return self._sma
    @sma.setter
    def sma(self, sma):
        self._sma = sma

    @property
    def color_KLineBoard(self):
        """The color_KLineBoard property."""
        return self._color_KLineBoard
    @color_KLineBoard.setter
    def color_KLineBoard(self, value):
        self._color_KLineBoard = value

    @property
    def color_SMA(self):
        """The color_SMA property."""
        return self._color_SMA
    @color_SMA.setter
    def color_SMA(self, value):
        self._color_SMA = value

    @property
    def color_RSI_up(self):
        """The color_RSI_up property."""
        return self._color_RSI_up
    @color_RSI_up.setter
    def color_RSI_up(self, value):
        self._color_RSI_up = value

    @property
    def color_RSI_down(self):
        """The color_RSI_down property."""
        return self._color_RSI_down
    @color_RSI_down.setter
    def color_RSI_down(self, value):
        self._color_RSI_down = value

    @property
    def color_Volume(self):
        """The color_Volume property."""
        return self._color_Volume
    @color_Volume.setter
    def color_Volume(self, value):
        self._color_Volume = value

    @property
    def color_K(self):
        """The color_K property."""
        return self._color_K
    @color_K.setter
    def color_K(self, value):
        self._color_K = value

    @property
    def color_D(self):
        """The color_D property."""
        return self._color_D
    @color_D.setter
    def color_D(self, value):
        self._color_D = value

    @property
    def color_BBands_upper(self):
        """The color_BBands_upper property."""
        return self._color_BBands_upper
    @color_BBands_upper.setter
    def color_BBands_upper(self, value):
        self._color_BBands_upper = value

    @property
    def color_BBands_lower(self):
        """The color_BBands_lower property."""
        return self._color_BBands_lower
    @color_BBands_lower.setter
    def color_BBands_lower(self, value):
        self._color_BBands_lower = value
        
    @property
    def draw_KLine(self):
        """The draw_KLine property."""
        return self._draw_KLine
    @draw_KLine.setter
    def draw_KLine(self, value):
        self._draw_KLine = value

    @property
    def draw_SMA(self):
        """The draw_SMA property."""
        return self._draw_SMA
    @draw_SMA.setter
    def draw_SMA(self, value):
        self._draw_SMA = value

    @property
    def draw_RSI(self):
        """The draw_RSI property."""
        return self._draw_RSI
    @draw_RSI.setter
    def draw_RSI(self, value):
        self._draw_RSI = value

    @property
    def draw_KD(self):
        """The draw_KD property."""
        return self._draw_KD
    @draw_KD.setter
    def draw_KD(self, value):
        self._draw_KD = value

    @property
    def draw_BBands(self):
        """The draw_BBands property."""
        return self._draw_BBands
    @draw_BBands.setter
    def draw_BBands(self, value):
        self._draw_BBands = value

    @property
    def draw_Volume(self):
        """The draw_Volume property."""
        return self._draw_Volume
    @draw_Volume.setter
    def draw_Volume(self, value):
        self._draw_Volume = value
