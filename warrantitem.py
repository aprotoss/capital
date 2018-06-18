#-*- coding: utf-8 -*-
from config import *
from warrantitemui import Ui_Form
from datetime import date
import pandas as pd
import pyqtgraph as pg

#Qt
from PyQt5 import QtCore, QtGui, QtWidgets

try:
    from PyQt5.QtCore import QString
except:
    QString = str

class WarrantItem(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.setupUi(self)

        #event
        self.cboxs = {'Date': self.dateCBox, 'Vendor': self.vendorCBox, 'Type': self.typeCBox}
        for cbox in self.cboxs:
            self.cboxs[cbox].activated.connect(self.on_datecbox_ctc_cb)
        self.tableView.doubleClicked.connect(self.on_tableview_dclick_cb)

    def setData(self, filename):
        df = pd.read_csv(filename, names=WTFIELD, dtype=WTFIELDTYPES)

        tmplist = df['Date'].value_counts().index
        self.dateCBox.addItem('--')
        self.dateCBox.addItems(tmplist.values)

        tmplist = df['Vendor'].value_counts().index
        self.vendorCBox.addItem('--')
        self.vendorCBox.addItems(tmplist.values)

        tmplist = df['Type'].value_counts().index
        self.typeCBox.addItem('--')
        self.typeCBox.addItems(tmplist.values)

        self.df = df
        self.tableView.setModel(PandasModel(self.df))

    def on_datecbox_ctc_cb(self, text):
        df = self.df
        for cbox in self.cboxs:
            label = self.cboxs[cbox].currentText()
            if label == '--':
                continue
            df = df[df[cbox] == label]

        self.tableView.setModel(PandasModel(df))

    def on_tableview_dclick_cb(self, index):
        model = self.tableView.model()
        idx = model.index(index.row(), 0)
        code = model.data(idx)
        self.graphicsView.clear()
        self.drawGraph(self.df[self.df['Code'] == code])

    def drawGraph(self, df):
        #data = df.as_matrix(WTFIELD)
        stringaxis = pg.AxisItem(orientation='bottom')
        xlist = []
        for idx, data in enumerate(df.as_matrix(['Date'])):
            xlist.append((idx, data))

        stringaxis.setTicks([xlist])

        p1 = self.graphicsView.addPlot(0, 0,  title='I.V.', axisItems={'bottom': stringaxis})

        p1item = pg.PlotCurveItem()
        p1item.setData(y=df['IV'].tolist())
        p1.addItem(p1item)
        p1.disableAutoRange()


class PandasModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None

#class W#arrantItem(pg.PlotWidget):
#class WarrantItem(pg.GraphicsLayoutWidget):
#    def __init__(self, *argv, **kargv):
#        super(__class__, self).__init__(*argv, **kargv)
#        self.addItem(self.generateTable(), 0, 0)
#
#    def setItem(self, filename):
#        df = pd.read_csv(filename, names=WTFIELD, dtype=WTFIELDTYPES)
#
#        name_list = df['Name'].value_counts().index
#
#        proxy = QtGui.QGraphicsProxyWidget()
#        table = pg.TableWidget()
#        proxy.setWidget(table)
#        self.addItem(proxy, 0, 0)
#
#        table.setData(df.values)
#
#        for i in name_list:
#            print(i)
#
#    def generateButton(self, label='Default'):
#        proxy = QtGui.QGraphicsProxyWidget()
#        button = QtGui.QPushButton(label)
#        proxy.setWidget(button)
#        return proxy
#
#    def generateTable(self):
#        proxy = QtGui.QGraphicsProxyWidget()
#        table = pg.TableWidget()
#        proxy.setWidget(table)
#        return proxy

