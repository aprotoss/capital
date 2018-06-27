# -*- coding: utf-8 -*-
#Qt
from capitalui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
try:
    from PyQt5.QtCore import QString
except:
    QString = str

#sys
from config import *
from pathlib import Path
from functools import partial
import requests
import json
import csv

class Warrant(QtCore.QObject):
    message = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

    def downloadWarrant(self, date):
        sdate = date.toString('yyyy-MM-dd')
        self.message.emit('[Warrant] start to get warrant: %s' % sdate)
        self.getthread = QtCore.QThread(self)
        self.getwarrantthread = GetWarrantThread()
        self.getwarrantthread.moveToThread(self.getthread)
        self.getwarrantthread.message.connect(self.on_message_cb)
        self.getthread.started.connect(partial(self.getwarrantthread.process, sdate))
        self.getthread.start()

    def getHistory(self):
        wtlog = Path(WarrantPath + '/' + 'wthistory.log')
        log = None
        if wtlog.exists(): 
            log = open(wtlog, 'r')
            log_data = log.read()
            log.close()
        else:
            return []

        return json.loads(log_data)
        
    def on_message_cb(self, msg):
        self.message.emit(msg)

class GetWarrantThread(QtCore.QObject):
    message = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

    @QtCore.pyqtSlot()
    def process(self, date):
        url = WarrantBaseURL + date + '.xls'
        filename = WarrantBaseFilename + date + '.xls'

        res = requests.get(url)
        if res.status_code is not 200:
            self.message.emit('[Warrant] get warrant: %s fail' % date)
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
        self.message.emit('[Warrant] get warrant %s success' % date)

    def splitWarrent(self, target, date):
        print('Open Target: %s' % target)
        self.message.emit('[Warrant] start to marshal warrant %s with history' % target)
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
            self.message.emit('[warrant] %s already save in file' % target)
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
