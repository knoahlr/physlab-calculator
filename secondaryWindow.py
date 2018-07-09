
from PyQt5.QtWidgets import QWidget, QFormLayout, QMainWindow, QGroupBox, QMessageBox,\
QLabel, QTextEdit, QLineEdit, QPushButton, QVBoxLayout
from backend import sampleCalculations, partialDerivative, isNumber, SIGMA
import unicodedata, re

from sympy import sympify
from errorWindow import ErrorWindow

class secondaryWindow(QWidget):
    
    def __init__(self, equation, variables, allSymbols, icon, latexOutput):
        
        super().__init__()

        '''Data Fields'''

        self.variables = variables
        self.allSymbols = allSymbols
        self.equation = equation

        self.symData = {str(key):None for key in self.allSymbols}
        self.errData = {'{0}{1}'.format(SIGMA, key):None for key in self.allSymbols}

        self.icon = icon

        self.latexOut = latexOutput

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

        self.addInputs(self.variables, self.allSymbols, self.topGroupBoxformLT, self.topGroupBox)
        self.addInputs(self.variables, self.allSymbols, self.bottomGroupBoxformLT, self.bottomGroupBox)


    def designGroupBox(self, boxTitle):

        box = QGroupBox(boxTitle)

        return box

    def addInputs(self, variables, allSymbols, layout, GroupBox):

        self.row = 0

        for variable in self.allSymbols:
            
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
            
        for var in self.allSymbols:

            sampEquationInput= self.topGroupBox.findChild(QLineEdit, str(var))
            self.symData[str(var)] = sampEquationInput.text().split(',')

            sampErrInput = self.bottomGroupBox.findChild(QLineEdit, str(var))
            self.errData['{0}{1}'.format(SIGMA, var)] = sampErrInput.text().split(',')

        self.validateInput()

        errorExpression = partialDerivative(self.variables, sympify(self.equation))

        latexOutput = sampleCalculations(self.equation, errorExpression, [self.symData, self.errData], self.allSymbols)

        self.latexOut.setText(latexOutput)

    def validateInput(self):

        ''' Integer validation '''
        invalidInputs = []

        for var, datas in self.symData.items():
            # print(self.symData[var].isnumeric())
            for data in datas:
                if not isNumber(data):
                    self.topGroupBox.findChild(QLineEdit, str(var)).clear()
                    invalidInputs.append(var)

        for var, datas in self.errData.items():
            for data in datas:
                if not isNumber(data):
                    self.bottomGroupBox.findChild(QLineEdit, str(var)).clear()
                    invalidInputs.append(var)

        if not invalidInputs: return 
        else:
            message = "{0} must be numeric values".format(str(invalidInputs).strip('[]'))
            self.error_window = ErrorWindow(message, self.icon)
            self.error_window.show()
