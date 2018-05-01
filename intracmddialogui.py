# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/intracmddialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_intraCMD(object):
    def setupUi(self, intraCMD):
        intraCMD.setObjectName("intraCMD")
        intraCMD.resize(480, 240)
        self.groupBox = QtWidgets.QGroupBox(intraCMD)
        self.groupBox.setGeometry(QtCore.QRect(2, 0, 475, 97))
        self.groupBox.setObjectName("groupBox")
        self.cmdLine = QtWidgets.QTextEdit(self.groupBox)
        self.cmdLine.setGeometry(QtCore.QRect(2, 12, 379, 80))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.cmdLine.setFont(font)
        self.cmdLine.setObjectName("cmdLine")
        self.enterBtn = QtWidgets.QPushButton(self.groupBox)
        self.enterBtn.setGeometry(QtCore.QRect(386, 10, 80, 80))
        self.enterBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/新前置字串/enter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.enterBtn.setIcon(icon)
        self.enterBtn.setIconSize(QtCore.QSize(80, 80))
        self.enterBtn.setObjectName("enterBtn")
        self.groupBox_2 = QtWidgets.QGroupBox(intraCMD)
        self.groupBox_2.setGeometry(QtCore.QRect(4, 96, 470, 140))
        self.groupBox_2.setObjectName("groupBox_2")
        self.histroyBrowser = QtWidgets.QTextBrowser(self.groupBox_2)
        self.histroyBrowser.setGeometry(QtCore.QRect(1, 12, 467, 125))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.histroyBrowser.setFont(font)
        self.histroyBrowser.setObjectName("histroyBrowser")

        self.retranslateUi(intraCMD)
        QtCore.QMetaObject.connectSlotsByName(intraCMD)

    def retranslateUi(self, intraCMD):
        _translate = QtCore.QCoreApplication.translate
        intraCMD.setWindowTitle(_translate("intraCMD", "Dialog"))
        self.groupBox.setTitle(_translate("intraCMD", "Command"))
        self.groupBox_2.setTitle(_translate("intraCMD", "History"))

import capital_rc
