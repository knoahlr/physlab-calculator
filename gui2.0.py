# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\PhysLabGui_v2.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(481, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.equationLabel = QtWidgets.QLabel(self.centralwidget)
        self.equationLabel.setObjectName("equationLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.equationLabel)
        self.equationLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.equationLineEdit.setObjectName("equationLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.equationLineEdit)
        self.constantsLabel = QtWidgets.QLabel(self.centralwidget)
        self.constantsLabel.setObjectName("constantsLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.constantsLabel)
        self.constantsLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.constantsLineEdit.setObjectName("constantsLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.constantsLineEdit)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.pushButton)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.textEdit)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label)
        self.verticalLayout.addLayout(self.formLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 481, 21))
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
        self.equationLabel.setText(_translate("MainWindow", "Equation"))
        self.constantsLabel.setText(_translate("MainWindow", "Constants"))
        self.pushButton.setText(_translate("MainWindow", "Submit"))
        self.label.setText(_translate("MainWindow", "Latex Output"))

