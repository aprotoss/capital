# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/historyviewer.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1360, 762)
        MainWindow.setMaximumSize(QtCore.QSize(1360, 765))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.msgBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.msgBrowser.setGeometry(QtCore.QRect(2, 626, 257, 93))
        self.msgBrowser.setObjectName("msgBrowser")
        self.stockTab = QtWidgets.QTabWidget(self.centralwidget)
        self.stockTab.setGeometry(QtCore.QRect(266, 6, 1087, 711))
        self.stockTab.setTabsClosable(True)
        self.stockTab.setObjectName("stockTab")
        self.stockTree = QtWidgets.QTreeWidget(self.centralwidget)
        self.stockTree.setGeometry(QtCore.QRect(2, 8, 256, 615))
        self.stockTree.setObjectName("stockTree")
        self.stockTree.headerItem().setText(0, "1")
        self.stockTree.header().setVisible(True)
        self.stockTree.header().setCascadingSectionResizes(False)
        self.stockTree.header().setDefaultSectionSize(120)
        self.stockTree.header().setHighlightSections(False)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1360, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionIntraCMD = QtWidgets.QAction(MainWindow)
        self.actionIntraCMD.setCheckable(True)
        self.actionIntraCMD.setChecked(False)
        self.actionIntraCMD.setEnabled(True)
        self.actionIntraCMD.setObjectName("actionIntraCMD")
        self.action_Exit = QtWidgets.QAction(MainWindow)
        self.action_Exit.setObjectName("action_Exit")
        self.actionWarrant = QtWidgets.QAction(MainWindow)
        self.actionWarrant.setObjectName("actionWarrant")
        self.actionStockKLine = QtWidgets.QAction(MainWindow)
        self.actionStockKLine.setCheckable(True)
        self.actionStockKLine.setObjectName("actionStockKLine")
        self.menuFile.addAction(self.action_Exit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.stockTab.setCurrentIndex(-1)
        self.action_Exit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionIntraCMD.setText(_translate("MainWindow", "IntraCMD"))
        self.action_Exit.setText(_translate("MainWindow", "Exit"))
        self.actionWarrant.setText(_translate("MainWindow", "Warrant"))
        self.actionStockKLine.setText(_translate("MainWindow", "Stock - Day-KLine"))

import capital_rc
