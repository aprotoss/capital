# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/intracmddialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 240)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
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
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(4, 96, 470, 140))
        self.groupBox_2.setObjectName("groupBox_2")
        self.histroyBrowser = QtWidgets.QTextBrowser(self.groupBox_2)
        self.histroyBrowser.setGeometry(QtCore.QRect(1, 12, 467, 125))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.histroyBrowser.setFont(font)
        self.histroyBrowser.setObjectName("histroyBrowser")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "Command"))
        self.groupBox_2.setTitle(_translate("Dialog", "History"))

import capital_rc
