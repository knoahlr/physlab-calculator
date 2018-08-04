
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QFormLayout, QMainWindow, QGroupBox, QMessageBox,\
QLabel, QTextEdit, QLineEdit, QPushButton, QVBoxLayout
from backend import sampleCalculations, partialDerivative, isNumber, SIGMA
import unicodedata, re

from sympy import sympify
from errorWindow import ErrorWindow

ICON = r'articles\atom.png'

class secondaryWindow(QWidget):
    
    def __init__(self, dataInput):
        
        super().__init__()

        '''Data Fields'''

        self.dataInput = dataInput

        self.dataInput.equationData = {str(key):None for key in self.dataInput.allSymbols}
        self.dataInput.errorData = {'{0}{1}'.format(SIGMA, key):None for key in self.dataInput.allSymbols}

        self.icon = QtGui.QIcon(ICON)
        self.resize(500, 300)

        self.latexOut = self.dataInput.latexOutput

        self.setWindowTitle("Sample Calculation")
        self.setObjectName("SampleCalc")
        #self.resize(self.sizeHint())
        #self.resize(200, 180)
        if self.icon: self.setWindowIcon(self.icon)
        
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.setLayout(self.verticalLayout)

        #GroupBoxes - Frames with labels
        self.topGroupBox = self.designGroupBox('Equation - Sample Calculation')      
        self.bottomGroupBox = self.designGroupBox('Error - Sample Calculation')
        self.bottomGroupBox.setObjectName('errorVariables')
        self.sampleSubmitButton = QPushButton("Submit")
        self.sampleSubmitButton.clicked.connect(self.handleSubmit)

        #setting Group Box layout
        self.topGroupBoxformLT = QFormLayout(self.topGroupBox)
        self.bottomGroupBoxformLT = QFormLayout(self.bottomGroupBox)

        self.verticalLayout.addWidget(self.topGroupBox)
        self.verticalLayout.addWidget(self.bottomGroupBox)
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
                self.input.setText('0.023, 0.01, 0.02, 0.005, 0.7')
            
            else: 
                self.inputLabel = QLabel(str(variable), GroupBox)
                self.input.setText('27, 6.6, 7.8, 9.2, 10.4')


            self.input.setObjectName(str(variable))
            self.input.setPlaceholderText(str(variable))
            
            layout.setWidget(self.row, QFormLayout.LabelRole, self.inputLabel)
            layout.setWidget(self.row, QFormLayout.FieldRole,self.input)
            
            self.row += 1

        
        return layout

    def handleSubmit(self):
        """ method to retrieve sample calculation data and pass to main window."""
            
        for var in self.dataInput.allSymbols:

            sampEquationInput= self.topGroupBox.findChild(QLineEdit, str(var))
            self.dataInput.equationData[str(var)] = sampEquationInput.text().split(',')

            sampErrInput = self.bottomGroupBox.findChild(QLineEdit, str(var))
            self.dataInput.errorData['{0}{1}'.format(SIGMA, var)] = sampErrInput.text().split(',')

        self.validateInput()

        self.dataInput.sampleCalculations()

    def validateInput(self):

        ''' Integer validation '''
        invalidInputs = []

        for var, datas in self.dataInput.equationData.items():
            # print(self.symData[var].isnumeric())
            for data in datas:
                if not isNumber(data):
                    self.topGroupBox.findChild(QLineEdit, str(var)).clear()
                    invalidInputs.append(var)

        for var, datas in self.dataInput.errorData.items():
            for data in datas:
                if not isNumber(data):
                    self.bottomGroupBox.findChild(QLineEdit, str(var)).clear()
                    invalidInputs.append(var)

        if not invalidInputs: return 
        else:
            message = "{0} must be numeric values".format(str(invalidInputs).strip('[]'))
            self.error_window = ErrorWindow(message, self.icon)
            self.error_window.show()
