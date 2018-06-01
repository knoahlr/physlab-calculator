# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\PhysLabGui_v3.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SampleCalc(object):
    def setupUi(self, SampleCalc):
        SampleCalc.setObjectName("SampleCalc")
        SampleCalc.resize(585, 368)
        self.verticalLayout = QtWidgets.QVBoxLayout(SampleCalc)
        self.verticalLayout.setObjectName("verticalLayout")

        self.frame = QtWidgets.QFrame(SampleCalc)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.formLayout = QtWidgets.QFormLayout(self.frame)
        self.formLayout.setObjectName("formLayout")
        
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_4)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_5)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_6)
        self.verticalLayout.addWidget(self.frame)
        
        self.frame_2 = QtWidgets.QFrame(SampleCalc)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.frame_2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.verticalLayout.addWidget(self.frame_2)

        self.retranslateUi(SampleCalc)
        QtCore.QMetaObject.connectSlotsByName(SampleCalc)

    def retranslateUi(self, SampleCalc):
        _translate = QtCore.QCoreApplication.translate
        SampleCalc.setWindowTitle(_translate("SampleCalc", "Form"))
        self.label_2.setText(_translate("SampleCalc", "TextLabel"))
        self.label_4.setText(_translate("SampleCalc", "TextLabel"))
        self.label_5.setText(_translate("SampleCalc", "TextLabel"))
        self.label_3.setText(_translate("SampleCalc", "TextLabel"))
        self.label.setText(_translate("SampleCalc", "TextLabel"))

