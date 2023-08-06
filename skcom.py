# -*- coding:utf-8 -*-
from PyQt6 import QtCore

#sys
import sys
import time

#comtypes
from comtypes.client import GetModule
sys.coinit_flags = 0
from pythoncom import PumpWaitingMessages
from pythoncom import CoInitialize 
