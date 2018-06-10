import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

from sympy import symbols, sympify
from backend import sampleCalculations, partialDerivative

import time

# import main


class mainWindow(QMainWindow):

    """ 
    Main window used to take in equation data and constants
    """

    def __init__(self):
        super().__init__()

        '''Fields'''
        self.equation_variables = {'equation':None,'variables':None}
        self.equation = None
        self.variables = None
        self.symData = {}
        self.secondThread = None


        self.setMinimumSize(800, 300)
        self.setWindowTitle("Error Propagation")
   
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName('centralWidget')

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")

        #Labels 
        self.equationLabel = QtWidgets.QLabel("Equation", self.centralwidget)
        self.equationLabel.setObjectName("equationLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.equationLabel)

        self.variablesLabel = QtWidgets.QLabel("variables", self.centralwidget)
        self.variablesLabel.setObjectName("variablesLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.variablesLabel)

        self.label = QtWidgets.QLabel("Latex Output", self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label)

        #Equation and variables text editors
        self.equationLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.equationLineEdit.setObjectName("equationLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.equationLineEdit)

        self.variablesLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.variablesLineEdit.setObjectName("variablesLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.variablesLineEdit)

        #Latex Output
        self.latexOutput = QtWidgets.QTextEdit(self.centralwidget)
        self.latexOutput.setObjectName("textEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.latexOutput)

        #submit button
        self.submitButton = QtWidgets.QPushButton("Submit", self.centralwidget)
        self.submitButton.setObjectName("pushButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.submitButton)

        self.submitButton.clicked.connect(self.handleSubmit)

        self.verticalLayout.addLayout(self.formLayout)

        self.setCentralWidget(self.centralwidget)

        
    def center(self):#Center Main window in active screen. Uses cursor position as reference.
        
        topGroupBoxGm = self.topGroupBoxGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        topGroupBoxGm.moveCenter(centerPoint)
        self.move(topGroupBoxGm.topLeft())

    def handleSubmit(self):

        self.equation_variables['equation'] = self.equationLineEdit.text()
        self.equation_variables['variables'] = self.variablesLineEdit.text()
        self.equationLineEdit.clear()
        self.variablesLineEdit.clear()

        self.variables = self.equation_variables['variables'].strip('\s').split(',')

        self.equation = self.equation_variables['equation'].strip('\s')

        ''' Integrate with LaTex backend here, also launch secondary window for sample calculations '''
        #Forming symbols

        self.symData = {key:None for key in symbols(self.variables)}

        self._running = False

        self.secondWindow = secondaryWindow(self.symData, self.handleSampleSubmit)
        self.secondWindow.show()
  
    def handleSampleSubmit(self):

        self.latexOutput.setText(sampleCalculations(partialDerivative(self.symData, sympify(self.equation)), self.symData))




class secondaryWindow(QWidget):
    
    def __init__(self, symData, handleSampleSubmit):
        
        super().__init__()

        '''Data Fields'''
        self.eqData = dict()
        self.errData = dict()
        self.symData = symData
        self.handleSampleSubmit = handleSampleSubmit

        self.setWindowTitle("Sample Calculation")
        self.setObjectName("SampleCalc")
        self.resize(self.sizeHint())
        
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.setLayout(self.verticalLayout)

        #GroupBoxes - Frames with labels
        self.topGroupBox = self.designGroupBox('Equation - Sample Calculation')      
        self.bottomGroupBox = self.designGroupBox('Error - Sample Calculation')
        self.sampleSubmitButton = QtWidgets.QPushButton("Submit")
        self.sampleSubmitButton.clicked.connect(self.handleSubmit)

        #setting Group Box layout
        self.topGroupBoxformLT = QFormLayout(self.topGroupBox)
        self.bottomGroupBoxformLT = QFormLayout(self.bottomGroupBox)

        self.verticalLayout.addWidget(self.topGroupBox)
        self.verticalLayout.addWidget(self.bottomGroupBox)
        self.verticalLayout.addWidget(self.sampleSubmitButton)

        self.addInputs(self.symData, self.topGroupBoxformLT, self.topGroupBox)
        self.addInputs(self.symData, self.bottomGroupBoxformLT, self.bottomGroupBox)


    def designGroupBox(self, boxTitle):

        box = QGroupBox(boxTitle)

        return box

    def addInputs(self, variables, layout, GroupBox):

        self.row = 0

        for variable in variables:

            self.inputLabel = QLabel(str(variable), GroupBox)
            self.input = QLineEdit(GroupBox)

            self.input.setObjectName(str(variable))
            self.input.setPlaceholderText(str(variable))
            
            layout.setWidget(self.row, QFormLayout.LabelRole, self.inputLabel)
            layout.setWidget(self.row, QFormLayout.FieldRole,self.input)
            
            self.row += 1

        
        return layout

    def handleSubmit(self):
        """ method to retrieve sample calculation data and pass to main window."""
        
        for var in self.symData:

            equationBox = self.topGroupBox.findChild(QLineEdit, str(var))
            self.symData[var] = equationBox.text()

        self.validateInput()

    def validateInput(self):

        ''' Integer validation '''
        invalidInputs = []

        for var in self.symData:
            # print(self.symData[var].isnumeric())
        
            if not self.symData[var].isnumeric():
                self.topGroupBox.findChild(QLineEdit, str(var)).clear()
                invalidInputs.append(var)

        if not invalidInputs:
            self.handleSampleSubmit()
            self.close()
        else:
            message = "{0} has to be integer".format(var)
            self.error_window = ErrorWindow(message)
            self.error_window.show()


'''Error Window Class Definition here'''
class ErrorWindow(QWidget):

    def __init__(self, errorInfo):

        super().__init__()
        self.setWindowTitle('Error Message')
        self.resize(self.minimumSizeHint())

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignCenter)

        self.label = QLabel(errorInfo)
        self.okButton = QPushButton('Ok')
        
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.okButton)

        self.okButton.clicked.connect(self.closeWindow)

    def closeWindow(self):

        self.close()

    

'''Line and Text edit custom implementation here'''
# class EquationVarEdit(QtWidgets.QLineEdit):


#class LatexOutEdit(QtWidgets.QTextEdit):


#class secondaryThreads(QtCore.QThread):
    
    # def __init__(self, secondaryWindow):

    #     super().__init__()
    #     self.window = secondaryWindow 

    # def obtainSampledata(self):
    #     #app = QApplication(sys.argv)
    #     self.window.show()
    #     #sys.exit(app.exec_())

    # def run(self):
    #     print('here')
    #     self.obtainSampledata()

    
    
def run():
    app = QApplication(sys.argv)
    app.setStyle(QCommonStyle())
    window = mainWindow()
    # myWindow = secondaryWindow()
    # myWindow.show()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()