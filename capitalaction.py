# -*- coding:utf-8 -*-
from collections import OrderedDict
from collections import deque
from capitalcode import *
from datetime import datetime
from config import *
from pathlib import Path
import pandas as pd
import subprocess
import shutil
import requests
import glob
import csv
import time
import os


#Qt
from PyQt5 import QtCore

try:
    from PyQt5.QtCore import QString
except:
    QString = str

class GetWarrantDoc(QtCore.QObject):
    getwarrantdoc = QtCore.pyqtSignal(bool, str)
    def __init__(self, parent=None):
        super(GetWarrantDoc, self).__init__(parent)

    @QtCore.pyqtSlot()
    def process(self, date):
        url = WarrantBaseURL + date + '.xls'
        filename = WarrantBaseFilename + date + '.xls'

        res = requests.get(url)
        if res.status_code is not 200:
            self.getwarrantdoc.emit(False, date)
            return None

        with open(WarrantPath + filename, 'wb') as xls:
            xls.write(res.content)
        self.getwarrantdoc.emit(True, date)

class SaveStock(QtCore.QObject):
    processing = QtCore.pyqtSignal(str)
    finish = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(SaveStock, self).__init__(parent)
        self.uid = None
        self.pwd = None
        self.stocklist = None

    def setProfile(self, uid, pwd):
        self.uid = uid
        self.pwd = pwd
    
    def setStockList(self, slist):
        print(slist)
        self.stocklist = slist

    @QtCore.pyqtSlot()
    def process(self):
        for idx, group in enumerate(self.stocklist):
            if idx is 32:
                idx += 1
            self.processing.emit(CapitalStockGroup[idx+1])
            cmd = ['python', 'getkline.py', self.uid, self.pwd]
            for stock in group:
                cmd.append(stock)
            r = subprocess.call(cmd)
            print('Exit code:', r)

        self.finish.emit('Finish')
                
class MergeStock(QtCore.QObject):
    processing = QtCore.pyqtSignal(str)
    finish = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

    @QtCore.pyqtSlot()
    def process(self):
        for i in glob.glob(CachePath + '/*.csv'):
            stocknocsv = i.split('\\')[1]
            targetPath = StocksPath + '/' + stocknocsv[:-4] 
            self.processing.emit('merage stock: %s' % stocknocsv[:-4])
            if not Path(targetPath).exists():
                os.makedirs(targetPath)

            #self.marshalCSV(targetPath + '/' + stocknocsv, i)
            self.splitCSV(stocknocsv[:-4])
            os.remove(i)
        self.finish.emit('Merge Process done.')

    def splitCSV(self, stockno):
        filename = CachePath + '/' + stockno + '.csv'
        df = pd.read_csv(filename, names=FIELD, dtype=FIELDTYPES)

        fname = None
        pre_date = None
        fp = None

        for i in df.values:
            date, time = i[0].split(' ')
            date = date.replace('/', '-')
            fname = StocksPath + '/' + stockno + '/' + date + '.1min'

            #already open the file or not
            if pre_date != date:
                #file already exists
                if os.path.exists(fname):
                    print('%s already exists' % fname)
                    continue
                if fp is not None:
                    fp.close()
                fp = open(fname, 'w')

            fp.write('%s, %f, %f, %f, %f, %d\n'% (time, i[1], i[2], i[3], i[4], i[5]))
            pre_date = date

        if fp is not None:
            fp.close()

