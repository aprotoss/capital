# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/warrantitem.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1070, 740)
        Form.setMaximumSize(QtCore.QSize(1070, 740))
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(6, 10, 177, 53))
        self.groupBox.setObjectName("groupBox")
        self.dateCBox = QtWidgets.QComboBox(self.groupBox)
        self.dateCBox.setGeometry(QtCore.QRect(8, 14, 161, 32))
        self.dateCBox.setObjectName("dateCBox")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(186, 8, 177, 53))
        self.groupBox_2.setObjectName("groupBox_2")
        self.vendorCBox = QtWidgets.QComboBox(self.groupBox_2)
        self.vendorCBox.setGeometry(QtCore.QRect(8, 14, 161, 32))
        self.vendorCBox.setObjectName("vendorCBox")
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setGeometry(QtCore.QRect(366, 8, 177, 53))
        self.groupBox_3.setObjectName("groupBox_3")
        self.typeCBox = QtWidgets.QComboBox(self.groupBox_3)
        self.typeCBox.setGeometry(QtCore.QRect(8, 14, 161, 32))
        self.typeCBox.setObjectName("typeCBox")
        self.tableView = QtWidgets.QTableView(Form)
        self.tableView.setGeometry(QtCore.QRect(8, 60, 1055, 323))
        self.tableView.setMaximumSize(QtCore.QSize(1070, 745))
        self.tableView.setObjectName("tableView")
        self.graphicsView = GraphicsLayoutWidget(Form)
        self.graphicsView.setGeometry(QtCore.QRect(8, 384, 1055, 353))
        self.graphicsView.setObjectName("graphicsView")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Date"))
        self.groupBox_2.setTitle(_translate("Form", "Vendor"))
        self.groupBox_3.setTitle(_translate("Form", "Type"))

from pyqtgraph import GraphicsLayoutWidget
