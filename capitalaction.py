# -*- coding:utf-8 -*-
from collections import OrderedDict
from collections import deque
from capitalcode import *
from datetime import datetime
from config import *
from pathlib import Path
import pandas as pd
import numpy as np
import subprocess
import shutil
import requests
import time
import json
import csv
import os

#Qt
from PyQt5 import QtCore

try:
    from PyQt5.QtCore import QString
except:
    QString = str

class GetWarrantDoc(QtCore.QObject):
    getwarrantdoc = QtCore.pyqtSignal(bool, str)
    processing = QtCore.pyqtSignal(str)
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

        with open(CachePath + '/' + filename, 'wb') as xls:
            xls.write(res.content)

        #split cache warrant file to warrant file with stocks filenames
        cpath = Path(CachePath)
        for xls in cpath.glob('*.xls'):
            date = str(xls).split('_')[-1].split('.')[0]
            #print(date)
            self.splitWarrent(xls, date)
            xls.unlink()
        self.getwarrantdoc.emit(True, date)

    def splitWarrent(self, target, date):
        print('Open Target: %s' % target)
        self.processing.emit('To marshal warrant: %s' % target)
        wtlog = Path(WarrantPath + '/' + 'wthistory.log')
        log = None
        if wtlog.exists(): 
            log = open(wtlog, 'r')
            log_data = log.read()
            log.close()
        else:
            log_data = '[]'
        jlog = json.loads(log_data)

        if date in jlog:
            self.processing.emit('Warrant: %s already save in file' % target)
            return None

        df = pd.read_excel(target, skiprows=5, header=0, names=WFIELD)
        df['Date'] = date
        stock_list = df['Stock'].value_counts().index
    
        for i in stock_list:
            sdf = df.loc[df['Stock'] == i]
            tdf = None
    
            p = Path(WarrantPath + '/' + i + '.wrt')
            if p.exists():
                tdf = pd.read_csv(str(p), names=WTFIELD)
                tdf = tdf.append(sdf)
            else:
                tdf = sdf
            tdf = tdf.replace('-', np.nan)
            tdf = tdf.sort_values('Date')
            tdf.to_csv(str(p), index=False, header=False)

        jlog.append(date)
        log = open(wtlog, 'w')
        json.dump(jlog, log, sort_keys=True, indent=4)

class SaveStock(QtCore.QObject):
    processing = QtCore.pyqtSignal(str)
    finish = QtCore.pyqtSignal()
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
            self.processing.emit('Save Group: %s ' % CapitalStockGroup[idx+1])
            cmd = ['python', 'getkline.py', self.uid, self.pwd]
            for stock in group:
                cmd.append(stock)
            r = subprocess.call(cmd)
            print('Exit code:', r)

        self.finish.emit()
