# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/capital.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        MainWindow.setStyleSheet("\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.connectBtn = QtWidgets.QPushButton(self.centralwidget)
        self.connectBtn.setGeometry(QtCore.QRect(172, 24, 48, 48))
        self.connectBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/新前置字串/led_redoff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/新前置字串/led_greenon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.connectBtn.setIcon(icon)
        self.connectBtn.setIconSize(QtCore.QSize(48, 48))
        self.connectBtn.setCheckable(True)
        self.connectBtn.setObjectName("connectBtn")
        self.msgBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.msgBrowser.setGeometry(QtCore.QRect(0, 460, 1021, 261))
        self.msgBrowser.setObjectName("msgBrowser")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(4, 0, 160, 50))
        self.groupBox.setObjectName("groupBox")
        self.userIDLine = QtWidgets.QLineEdit(self.groupBox)
        self.userIDLine.setGeometry(QtCore.QRect(4, 12, 150, 32))
        self.userIDLine.setInputMask("")
        self.userIDLine.setText("")
        self.userIDLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.userIDLine.setObjectName("userIDLine")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(4, 46, 160, 50))
        self.groupBox_2.setObjectName("groupBox_2")
        self.passwordLine = QtWidgets.QLineEdit(self.groupBox_2)
        self.passwordLine.setGeometry(QtCore.QRect(4, 12, 150, 32))
        self.passwordLine.setText("")
        self.passwordLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLine.setObjectName("passwordLine")
        self.connectBtn.raise_()
        self.connectBtn.raise_()
        self.msgBrowser.raise_()
        self.groupBox.raise_()
        self.groupBox_2.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "User"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Password"))

import capital_rc
