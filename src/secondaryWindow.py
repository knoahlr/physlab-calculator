from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QFormLayout, QMainWindow, QGroupBox, QMessageBox,\
QLabel, QTextEdit, QLineEdit, QPushButton, QVBoxLayout

from tableViewWindow import tableWindow
from errorWindow import ErrorWindow

import unicodedata, re
from sympy import sympify
from data import SIGMA
import pathlib

ICON = r'..\articles\atom.png'

class secondaryWindow(QWidget):
    
    def __init__(self, dataInput):
        
        super().__init__()

        ''' MISC '''
        
        self.icon = QtGui.QIcon(ICON)
        self.resize(500, 300)
        if self.icon: self.setWindowIcon(self.icon)
        
        self.setWindowTitle("Sample Calculation")
        self.setObjectName("SampleCalc")

        self.fromTable = False

        '''Data Fields'''

        self.dataInput = dataInput
        self.dataInput.equationData = {str(key):[] for key in self.dataInput.allSymbols}
        self.dataInput.errorData = {'{0}{1}'.format(SIGMA, key):[] for key in self.dataInput.allSymbols}

        self.latexOut = self.dataInput.latexOutput
        self.importWindow = None


        ''' Main Layout '''
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.setLayout(self.verticalLayout)

        ''' GroupBoxes  '''
        self.topGroupBox = self.designGroupBox('Equation - Sample Calculation')
        self.topGroupBoxformLT = QFormLayout(self.topGroupBox)
        self.dataInput.topGroupBox = self.topGroupBox
        

        self.bottomGroupBox = self.designGroupBox('Error - Sample Calculation')
        self.bottomGroupBoxformLT = QFormLayout(self.bottomGroupBox)
        self.bottomGroupBox.setObjectName('errorVariables')
        self.dataInput.bottomGroupBox = self.bottomGroupBox

        self.importDataGroupBox = self.designGroupBox('Import Data')
        self.importDataLayout = QFormLayout(self.importDataGroupBox)
        
        ''' Import Data Labels '''
        
        self.importFileLabel = QLabel('Import File', self.importDataGroupBox)
        self.importFileBox = QLineEdit(self.importDataGroupBox)
        self.importFileBox.setText(r'C:\Users\Noah Workstation\Desktop\P_PR\repo\physlab-calculator\test\testData.csv')

        self.outputFileLabel  = QLabel('Output File')
        self.outputFileBox = QLineEdit(self.importDataGroupBox)


        ''' sample equation submit and Import Data button '''
        self.sampleSubmitButton = QPushButton("Submit")
        self.sampleSubmitButton.clicked.connect(self.handleSubmit)


        self.importButton = QPushButton('Import')
        self.importButton.clicked.connect(self.importSubmit)

        self.importDataLayout.setWidget(0, QFormLayout.LabelRole, self.importFileLabel)
        self.importDataLayout.setWidget(0, QFormLayout.FieldRole, self.importFileBox)

        self.importDataLayout.setWidget(1, QFormLayout.LabelRole, self.outputFileLabel)
        self.importDataLayout.setWidget(1, QFormLayout.FieldRole, self.outputFileBox)
        self.importDataLayout.addWidget(self.importButton)

        self.verticalLayout.addWidget(self.topGroupBox)
        self.verticalLayout.addWidget(self.bottomGroupBox)
        self.verticalLayout.addWidget(self.importDataGroupBox)
        self.verticalLayout.addWidget(self.sampleSubmitButton)

        self.addInputs(self.topGroupBoxformLT, self.topGroupBox)
        self.addInputs(self.bottomGroupBoxformLT, self.bottomGroupBox)


    def designGroupBox(self, boxTitle):

        box = QGroupBox(boxTitle)

        return box

    def addInputs(self, layout, GroupBox):

        self.row = 0

        for variable in self.dataInput.allSymbols:
            
            self.input = QLineEdit(GroupBox)
            
            if re.search('errorVariables', GroupBox.objectName()): 

                self.inputLabel = QLabel('{0}{1}'.format(unicodedata.lookup("GREEK SMALL LETTER SIGMA"), str(variable)), GroupBox)
                #self.input.setText('0.023, 0.01, 0.02, 0.005, 0.7, 0.023, 0.01, 0.02, 0.005, 0.7, 0.023, 0.01, 0.02, 0.005, 0.7, 0.023, 0.01, 0.02, 0.005, 0.7')
                self.input.setText('0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0')
                #self.input.setText('0.3')
            else: 
                self.inputLabel = QLabel(str(variable), GroupBox)
                self.input.setText('2.7, 6.6, 7.8, 9.2, 10.4, 2.7, 6.6, 7.8, 9.2, 10.4, 2.7, 6.6, 7.8, 9.2, 10.4, 2.77, 6.6, 7.8, 9.2, 10.4')
                
 

            self.input.setObjectName(str(variable))
            self.input.setPlaceholderText(str(variable))
            
            layout.setWidget(self.row, QFormLayout.LabelRole, self.inputLabel)
            layout.setWidget(self.row, QFormLayout.FieldRole,self.input)
            
            self.row += 1

        
        return layout

    def handleSubmit(self):

        """ 
        method to retrieve sample calculation data and pass to main window.
        """
            
        if not self.fromTable:

            for var in self.dataInput.allSymbols:

                sampEquationInput= self.topGroupBox.findChild(QLineEdit, str(var))
                self.dataInput.equationData[str(var)] = sampEquationInput.text().split(',')

                sampErrInput = self.bottomGroupBox.findChild(QLineEdit, str(var))
                self.dataInput.errorData['{0}{1}'.format(SIGMA, var)] = sampErrInput.text().split(',')

            self.dataInput.dataNormalization()
            self.dataInput.postToGroupBox()
        
        self.fromTable = False

        self.validateInput()

        self.dataInput.sampleCalculations()

    def importSubmit(self):

        filePath = self.importFileBox.text()

        if self.validatFile(filePath):

            self.importWindow = tableWindow(filePath, self.dataInput)
            self.fromTable = True
            self.importWindow.show()

            

    def validateInput(self):

        ''' Integer validation '''
        invalidInputs = []

        for var, datas in self.dataInput.equationData.items():
            # print(self.symData[var].isnumeric())
            for data in datas:
                if not self.isNumber(data):
                    self.topGroupBox.findChild(QLineEdit, str(var)).clear()
                    invalidInputs.append(var)

        for var, datas in self.dataInput.errorData.items():
            for data in datas:
                if not self.isNumber(data):
                    self.bottomGroupBox.findChild(QLineEdit, str(var)).clear()
                    invalidInputs.append(var)

        if not invalidInputs: return 
        else:
            message = "{0} must be numeric values".format(str(invalidInputs).strip('[]'))
            self.error_window = ErrorWindow(message, self.icon)
            self.error_window.show()

    def validatFile(self, filePath):

        ''' Check whether file exists or not '''

        myfilePath = pathlib.PurePath(filePath)

        if pathlib.Path(myfilePath).exists():

            if pathlib.Path(myfilePath).is_file():

                return True
            else:

                self.error_window = ErrorWindow("{0} is not a file".format(str(myfilePath)), self.icon)
                self.error_window.show()

                return False
        else:
            self.error_window = ErrorWindow("{0} doesn`t exist".format(str(myfilePath)), self.icon)
            self.error_window.show()

            return False






            
    def isNumber(self, s):
        ''' Implemented in validating sample calculation inputs'''
        try:
            float(s)
            return True
        except ValueError:
            return False
