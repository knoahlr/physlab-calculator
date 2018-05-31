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
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(SampleCalc)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout.addWidget(self.frame_2)

        self.retranslateUi(SampleCalc)
        QtCore.QMetaObject.connectSlotsByName(SampleCalc)

    def retranslateUi(self, SampleCalc):
        _translate = QtCore.QCoreApplication.translate
        SampleCalc.setWindowTitle(_translate("SampleCalc", "Form"))

