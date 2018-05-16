# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/stockinformation.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1070, 430)
        self.stockTBrowser = QtWidgets.QTextBrowser(Form)
        self.stockTBrowser.setGeometry(QtCore.QRect(2, 2, 360, 426))
        self.stockTBrowser.setObjectName("stockTBrowser")
        self.stockCanvas = QtWidgets.QWidget(Form)
        self.stockCanvas.setGeometry(QtCore.QRect(364, 2, 703, 427))
        self.stockCanvas.setObjectName("stockCanvas")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

