# -*- coding:utf-8 -*-
from collections import OrderedDict
from datetime import datetime
from config import *
import requests
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
            if not os.path.exists(directory):
                os.makedirs(directory)

            filename = directory + '/' + stockno + '.csv'
            self.fp[stockno] = open(filename, 'w', encoding='utf-8')
            self.fp[stockno].write('Date,Open,High,Low,Close,Volume\n')

    def setData(self, data):
        self.queue.append(data)

    @QtCore.pyqtSlot()
    def process(self):
        self._running = True 
        while self._running:
            if len(self.queue) is not 0:
                item = self.queue.pop(0)
                self.fp[item[0]].write(item[1] + '\n')
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
