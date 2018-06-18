# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/warrantviewer.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WarrantViewer(object):
    def setupUi(self, WarrantViewer):
        WarrantViewer.setObjectName("WarrantViewer")
        WarrantViewer.resize(1366, 800)
        self.centralwidget = QtWidgets.QWidget(WarrantViewer)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(2, 4, 283, 753))
        self.groupBox.setObjectName("groupBox")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(6, 14, 231, 32))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(244, 14, 32, 32))
        self.pushButton.setObjectName("pushButton")
        self.stockList = QtWidgets.QListWidget(self.groupBox)
        self.stockList.setGeometry(QtCore.QRect(6, 50, 271, 701))
        self.stockList.setObjectName("stockList")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(288, 6, 1071, 747))
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName("tabWidget")
        WarrantViewer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(WarrantViewer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1366, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        WarrantViewer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(WarrantViewer)
        self.statusbar.setObjectName("statusbar")
        WarrantViewer.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(WarrantViewer)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(WarrantViewer)
        self.tabWidget.setCurrentIndex(-1)
        self.actionQuit.toggled['bool'].connect(WarrantViewer.close)
        QtCore.QMetaObject.connectSlotsByName(WarrantViewer)

    def retranslateUi(self, WarrantViewer):
        _translate = QtCore.QCoreApplication.translate
        WarrantViewer.setWindowTitle(_translate("WarrantViewer", "MainWindow"))
        self.groupBox.setTitle(_translate("WarrantViewer", "Stock List"))
        self.pushButton.setText(_translate("WarrantViewer", "Go"))
        self.menuFile.setTitle(_translate("WarrantViewer", "File"))
        self.actionQuit.setText(_translate("WarrantViewer", "Quit"))

