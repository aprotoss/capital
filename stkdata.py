#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import talib
from talib import abstract

class StkData(object):
    def __init__(self):
        self._sid = None
        self._stkdata = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Volume"])
        self._raw_stkdata = None

    @property
    def stk_id(self):
        return self._sid

    @stk_id.setter
    def stk_id(self, sid):
        self._sid = sid

    @property
    def stk_data(self):
        return self._stkdata
    
    @stk_data.setter
    def stk_data(self, sdata):
        self._stkdata = sdata
        self._raw_stkdata = sdata

    def read_csv(self, csvfilename=None):
        #print(csvfilename)
        self._stkdata = pd.read_csv(csvfilename)

    def save_csv(self, filename=None):
        self._stkdata.to_csv(filename, index=False)

    #[Date,Open,High,Low,Close,Volume]
    def concat_row(self, data):
        row = pd.Series(data, index=["Date", "Open", "High", "Low", "Close", "Volume"])
        self._stkdata = pd.concat([self._stkdata, row.to_frame().T], ignore_index=True)
        return True

    def concat_raw(self, date, open_price, high_price, low_price, close_price, volume):
        return self.concat_row([date, open_price, high_price, low_price, close_price, volume])

    #Algorithm
    def RSI(self, up=10, down=5):
        if self._stkdata is None:
            return None
        rsiU = talib.RSI(self._stkdata["Close"], up)
        rsiD = talib.RSI(self._stkdata["Close"], down)
        return pd.DataFrame({"Up": rsiU, "Down": rsiD})

    def SMA(self, date = 10):
        if self._stkdata is None:
            return None
        sma = talib.SMA(self._stkdata["Close"], date)
        return pd.DataFrame({f"SMA_{date}": sma})

    def KD(self):
        if self._stkdata is None:
            return None
        df_k, df_d = talib.STOCH(self._stkdata["High"], self._stkdata["Low"], self._stkdata["Close"])
        return pd.DataFrame({"Date": self._stkdata["Date"], "K": df_k, "D": df_d})
    
    def BBands(self, period=10, stdNbr=2):
        if self._stkdata is None:
            return None
        upper, middle, lower = talib.BBANDS(self._stkdata["Close"], timeperiod=period, nbdevup=stdNbr, nbdevdn=stdNbr, matype=0)
        return pd.DataFrame({"upper": upper, "middle": middle, "lower": lower})

    def switch_K_type(self, ktype = "T"):
        if self._raw_stkdata is None:
            self._raw_stkdata = self._stkdata.copy() 
            
        if ktype == "T": 
            self._stkdata = self._raw_stkdata.copy()
            return None

        stkdata = self._raw_stkdata.copy()
    
        stkdata["Date"] = pd.to_datetime(stkdata["Date"])
        stkdata.set_index("Date", inplace=True)

        stkdata = stkdata.resample(ktype).agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum",
            }).dropna()

        stkdata.reset_index(inplace=True)
        stkdata.to_csv("60T-result", index=False)
        self._stkdata = stkdata

if "__main__" in __name__:
    print("StkData Test Start")

    sd = StkData()
    sd.stk_id = "2330"
    print(sd.stk_id)

    sd.read_csv("./stkdata/0000-1234.txt")


    print(sd.stk_data)

    sd.concat_raw('2023-07-24', 100.50, 102.20, 99.80, 101.20, 100000)
    sd.concat_raw('2023-07-25', 101.50, 103.20, 90.80, 108.20, 103000)

    print(sd.stk_data)

    '''
    rsi = sd.RSI()
    print("--RSI-------------------")
    print(rsi)

    print("--SMA 10-------------------")
    sma_10 = sd.SMA(10)
    print(sma_10)
    
    print("--SMA 30-------------------")
    sma_30 = sd.SMA(30)
    print(sma_30)

    print("--KD-------------------")
    kd = sd.KD()
    print(kd)
    '''
