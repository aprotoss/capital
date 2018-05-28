# -*- coding:utf-8 -*-
from collections import OrderedDict
from collections import deque
from capitalcode import *
from datetime import datetime
from config import *
from pathlib import Path
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

class WriteStockKLine(QtCore.QObject):
    def __init__(self, parent=None):
        super(WriteStockKLine, self).__init__(parent)
        #self.date = datetime.now().strftime("%Y-%m-%d")
        self.fp = OrderedDict()
        self.queue = []
        self._running = False

    def setStockNo(self, stockno):
        directory = CachePath
        if stockno not in self.fp.keys():
            #print('Open a new file %s' % stockno)
            pathobj = Path(directory)
            if not pathobj.exists():
                os.makedirs(directory)

            filename = directory + '/' + stockno + '.csv'
            self.fp[stockno] = open(filename, 'w', encoding='utf-8')
            #self.fp[stockno].write('Date,Open,High,Low,Close,Volume\n')

    def setData(self, data):
        self.queue.append(data)

    @QtCore.pyqtSlot()
    def process(self):
        self._running = True 
        while self._running:
            if len(self.queue) is not 0:
                item = self.queue.pop(0)
                self.fp[item[0]].write(item[1] + '\n')
                self.fp[item[0]].flush()
                del item
            else:
                for key in self.fp:
                    self.fp[key].flush()
                time.sleep(0.01)

            while (len(self.fp) > 10):
                fitem = self.fp.popitem(last=False)
                print('close some fp: %s' % fitem[0])
                fitem[1].close()
                del fitem

        for key in self.fp:
            self.fp[key].close()

    def stop(self):
        self._running = False

class MarshalStock(QtCore.QObject):
    processing = QtCore.pyqtSignal(str)
    finish = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(MarshalStock, self).__init__(parent)

        self.fp = None
        self.fp_date = '0000-00-00'
        self.csvwriter = None

    @QtCore.pyqtSlot()
    def process(self):
        for i in glob.glob(CachePath + '/*.csv'):
            stocknocsv = i.split('\\')[1]
            targetPath = StocksPath + '/' + stocknocsv[:-4] 
            self.processing.emit(stocknocsv[:-4])
            if not Path(targetPath).exists():
                os.makedirs(targetPath)

            self.marshalCSV(targetPath + '/' + stocknocsv, i)
            os.remove(i)
        self.finish.emit('Merge Process done.')

    def marshalCSV(self, targetcsv, stocknocsv):
        #print(stocknocsv)
        pathobj = Path(targetcsv)
        if not pathobj.exists():
            shutil.copy2(stocknocsv, targetcsv)
            return None

        target = open(targetcsv, 'r')
        writer = csv.reader(target) 
    
        lastrow = None
        try:
            lastrow = deque(writer, 1)[0]
        except IndexError:
            lastrow = None

        #print('lastrow   ', lastrow)

        target.close() 
        target = open(targetcsv, 'a', newline='\n')
        writer = csv.writer(target)

        date = None
        if lastrow is None:
            date = datetime.strptime('1900-01-01', '%Y-%m-%d').date()
        else:
            date = datetime.strptime(lastrow[0].split(' ')[0], '%Y/%m/%d').date()

        source = open(stocknocsv, 'r')
        reader = csv.reader(source)

        for row in reader:
            tmp = row[0].split(' ')[0]
            #tmp = row['Date'].split(' ')[0]
            rdate = datetime.strptime(tmp, '%Y/%m/%d').date()
            if date < rdate:
                writer.writerow(row)

        source.close()
        target.close()

class minKLine(QtCore.QObject):
    processing = QtCore.pyqtSignal(str)
    finish = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(minKLine, self).__init__(parent)
        self.mink = 30 

    def setMin(self, mink):
        self.mink = mink

    @QtCore.pyqtSlot()
    def process(self):
        for src in glob.glob(StocksPath + '/*'):
            stockno = src.split('\\')[1]
            self.processing.emit(stockno)
            self.produceMinKLine(src + '/' + stockno + '.csv', src + '/' + stockno + '.%dmin' % self.mink)
        #print('finish')
        self.finish.emit('KLine process done.')

    def produceMinKLine(self, src, tar):
        FIELD =['Date','Open','High','Low','Close','Volume']
        print(src)
        print(tar)

        source = open(src, 'r', newline='\n')
        reader = csv.DictReader(source, fieldnames=FIELD)

        target = open(tar, 'w', newline='\n')
        writer = csv.DictWriter(target, fieldnames=FIELD)

        vTime = None
        vOpen = 0
        vHigh = 0
        vLow = 0
        vClose = 0
        vVolume = 0

        #preTime = datetime.strptime('1900-01-01 00:00', '%Y-%m-%d %H:%M')
        preTime = None

        deltaTime = 0.0
        stepTime = self.mink * 60.0
        for row in reader:
            t =  datetime.strptime(row['Date'], '%Y/%m/%d %H:%M')

            if preTime is not None:
                deltaTime += (t - preTime).total_seconds()
            else:
                deltaTime += 60.0
                vOpen = row['Open']
            
            vTime = row['Date']
            vHigh = max(vHigh, float(row['High']))
            vLow = min(vLow, float(row['Low']))
            vClose = float(row['Close'])
            vVolume += int(row['Volume'])
            preTime = t

            if deltaTime == stepTime: 
                writer.writerow({'Date': vTime, 'Open': vOpen, 'High': vHigh, 'Low': vLow, 'Close': vClose, 'Volume': vVolume})
                preTime = None
                deltaTime = 0
                vHigh = 0
                vLow = 0
                vClose = 0
                vVolume = 0
                
        source.close()
        target.close()

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
                


