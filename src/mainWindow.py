from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QFormLayout, QMainWindow, QGroupBox, \
QMessageBox, QLabel, QTextEdit, QLineEdit, QPushButton, QApplication

from sympy import symbols, sympify, pretty

from secondaryWindow import secondaryWindow
from errorWindow import ErrorWindow
from data import userInput

import re

ICON = r'..\articles\atom.png'


class mainWindow(QMainWindow):

    """ 
    Main window used to take in equation data and constants
    """

    def __init__(self, args):
        super().__init__()
        self.args = args

        '''Fields'''
        self.equation_variables = {'equation':None, 'variables':None}
        self.equation = None
        self.variables = None
        self.actualEqBlock = u"Equation:\n\tcos(x) +sin(y)\u00B2  +e\u00B3\u02b8 + ln(z) + log(y)"      #Equation formatting example
        self.typedEquation = "Represented As:\n\tcos(x) + sin(y)^2 + exp(3*y) + log(z) + log(y, 10)"    #Equation formatting example
        self.dataInput = None

        ''' Window Properties '''
        self.icon = QtGui.QIcon(r'..\articles\atom.png')
        self.setMinimumSize(self.sizeHint())
        self.resize(800,500)
        self.setWindowTitle("Error Propagation")
        self.setWindowIcon(self.icon)

        ''' Setting window layout and central widget '''
        self.centralwidget = QtWidgets.QWidget()
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.formLayout = QtWidgets.QFormLayout()
        
        '''Box Frames'''
        self.formatGroupBox = self.designGroupBox('Equation format')
        self.EqVarGroupBox = self.designGroupBox('Equation and Variables Input')
        self.latexGroupBox = self.designGroupBox('Latex Output')
        

        '''Add layout to frames'''
        self.eqFormatLayout = QFormLayout(self.formatGroupBox)
        self.EqVarLayout = QFormLayout(self.EqVarGroupBox)
        self.latexLayout = QFormLayout(self.latexGroupBox)

        self.eqFormatLayout.setAlignment(QtCore.Qt.AlignHCenter)
        self.EqVarLayout.setAlignment(QtCore.Qt.AlignHCenter)
        self.latexLayout.setAlignment(QtCore.Qt.AlignHCenter)


        ''' Labels '''
        self.equationFormatLabel = QtWidgets.QLabel(self.actualEqBlock, self.centralwidget)
        self.typedEquationLabel = QtWidgets.QLabel(self.typedEquation, self.centralwidget)
        self.equationLabel = QtWidgets.QLabel("Equation", self.centralwidget)
        self.variablesLabel = QtWidgets.QLabel("variables", self.centralwidget)
        self.latexLabel = QtWidgets.QLabel("Latex Output", self.centralwidget)

        '''Equation and variables text editors'''
        self.equationLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.equationLineEdit.setText('cos(x) + sin(y)^2 + asin(z)^3 *exp(3*z)*sin(a)')
        self.variablesLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.variablesLineEdit.setText('x, y, z')


        '''Text Edit'''
        self.latexOutput = QtWidgets.QTextEdit(self.centralwidget)
        self.latexOutput.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        '''submit button'''
        self.submitButton = QtWidgets.QPushButton("Submit", self.centralwidget)
        self.submitButton.clicked.connect(self.handleSubmit)

        #self.addFields(0, self.eqFormatLayout, self.equationFormat, self.equationFormatLabel)
        self.addFields(0,self.EqVarLayout, self.equationLineEdit, self.equationLabel)
        self.addFields(1, self.EqVarLayout, self.variablesLineEdit, self.variablesLabel)
        self.addFields(0,self.latexLayout, self.latexOutput, self.latexLabel)


        self.EqVarLayout.setWidget(2, QFormLayout.FieldRole, self.submitButton)

        '''Adding layouts and widgets to window'''
        self.verticalLayout.addWidget(self.formatGroupBox)
        self.verticalLayout.addWidget(self.EqVarGroupBox)
        self.verticalLayout.addWidget(self.latexGroupBox)

        self.eqFormatLayout.setWidget(0, QFormLayout.LabelRole, self.equationFormatLabel)
        self.eqFormatLayout.setWidget(1, QFormLayout.LabelRole, self.typedEquationLabel)
        self.setCentralWidget(self.centralwidget)

    
    
    def addFields(self, row, layout, editBox, label):

        layout.setWidget(row, QFormLayout.LabelRole,label)
        layout.setWidget(row, QFormLayout.FieldRole, editBox)

    def designGroupBox(self, boxTitle):

        box = QGroupBox(boxTitle)

        return box

        
    def center(self):
        
        ''' Center Main window in active screen. Uses cursor position as reference. '''
        
        topGroupBoxGm = self.topGroupBoxGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        topGroupBoxGm.moveCenter(centerPoint)
        self.move(topGroupBoxGm.topLeft())

    def handleSubmit(self):

        self.equation = self.equationLineEdit.text().strip('\s')
        self.variables = re.findall(r"[a-zA-Z']+", self.variablesLineEdit.text())
        
        if self.validateInput():

            ''' Integrate with LaTex backend here, also launch secondary window for sample calculations '''

            self.dataInput = userInput(self.equation, self.allSymbols, self.variables, self.args)
            self.dataInput.latexOutput = self.latexOutput

            self.secondWindow = secondaryWindow(self.dataInput)
            self.secondWindow.show()

    def validateInput(self):

        '''Equation and Variables validation'''

        try:

            sympify(self.equation)
            self.allSymbols = list(sympify(self.equationLineEdit.text()).free_symbols)

            ''' Error window generated if atleast one variables hasn`t been provided '''
            if not self.variables:
                self.errorWindow = ErrorWindow('There has to be atleast one differentiable variable bro', self.icon)
                self.variablesLineEdit.clear()
                self.errorWindow.show()

                return False
            else: 
                ''' if a variable cannot be detected in equation (self.allSymbols), it`ll  be erased from self.variables'''
                for variable in self.variables:
                    symbols = [str(item) for item in self.allSymbols]
                    if variable not in symbols:
                        self.variables.remove(variable)
                
                self.variablesLineEdit.setText(", ".join(str(x) for x in self.variables))
                
        except Exception as e:

            ''' Catches Sympify error if equation cannot be parsed '''

            windowMsg = e
            self.equationLineEdit.clear()
            if type(windowMsg).__name__ == 'SympifyError': self.errorWindow = ErrorWindow(windowMsg.expr, self.icon)
            else: self.errorWindow = ErrorWindow(str(windowMsg), self.icon)
            self.errorWindow.show()

            return False

        return True

   