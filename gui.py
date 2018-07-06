import sys
import time, ctypes, re, unicodedata

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QFormLayout, QMainWindow, QGroupBox, QMessageBox, QLabel, QTextEdit, QLineEdit, \
QPushButton, QCommonStyle, QApplication

from sympy import symbols, sympify, pretty
from backend import sampleCalculations, partialDerivative, isNumber, SIGMA


class mainWindow(QMainWindow):

    """ 
    Main window used to take in equation data and constants
    """

    def __init__(self):
        super().__init__()

        '''Fields'''
        self.equation_variables = {'equation':None, 'variables':None}
        self.equation = None
        self.variables = None
        self.actualEqBlock = u"Equation:\n\tcos(x) +sin(y)\u00B2  +e\u00B3\u02b8 + ln(z) + log(y)"      #Equation formatting example
        self.typedEquation = "Represented As:\n\tcos(x) + sin(y)^2 + exp(3*y) + log(z) + log(y, 10)"    #Equation formatting example

        ''' Window Properties '''
        self.icon = QtGui.QIcon(r'articles\atom.png')
        self.setMinimumSize(self.minimumSizeHint())
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
        # self.equationFormat = QtWidgets.QTextEdit(self.centralwidget)
        # self.equationFormat.setReadOnly(True)
        #self.equationFormat.setText(pretty(sympify('cos(x) + sin(y)^2'),use_unicode=True))
        self.latexOutput = QtWidgets.QTextEdit(self.centralwidget)


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

        
    def center(self):#Center Main window in active screen. Uses cursor position as reference.
        
        topGroupBoxGm = self.topGroupBoxGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        topGroupBoxGm.moveCenter(centerPoint)
        self.move(topGroupBoxGm.topLeft())

    def handleSubmit(self):

        self.equation_variables['equation'] = self.equationLineEdit.text()
        self.equation_variables['variables'] = self.variablesLineEdit.text()

        self.variables = re.findall(r"[a-zA-Z']+", self.equation_variables['variables']) #strip('\s').split(',')

        self.allSymbols = list(sympify(self.equation_variables['equation']).free_symbols)

        self.equation = self.equation_variables['equation'].strip('\s')

        if self.validateInput():

            ''' Integrate with LaTex backend here, also launch secondary window for sample calculations '''

            self._running = False

            self.secondWindow = secondaryWindow(self.equation, self.variables, self.allSymbols, self.icon, self.latexOutput)
            self.secondWindow.show()

    def validateInput(self):

        '''Equation and Variables validation'''

        try:

            sympify(self.equation)

            if not self.variables:
                self.errorWindow = ErrorWindow('There has to be atleast one differentiable variable bro', self.icon)
                self.variablesLineEdit.clear()
                self.errorWindow.show()

                return False

  
        except Exception as e:

            windowMsg = e
            self.equationLineEdit.clear()
            self.errorWindow = ErrorWindow(windowMsg.expr, self.icon)
            self.errorWindow.show()

            return False

        return True

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
        self.resize(self.sizeHint())
        if self.icon: self.setWindowIcon(self.icon)
        
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.setLayout(self.verticalLayout)

        #GroupBoxes - Frames with labels
        self.topGroupBox = self.designGroupBox('Equation - Sample Calculation')      
        self.bottomGroupBox = self.designGroupBox('Error - Sample Calculation')
        self.bottomGroupBox.setObjectName('errorVariables')
        self.sampleSubmitButton = QtWidgets.QPushButton("Submit")
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


'''Error Window Class Definition here'''
class ErrorWindow(QWidget):

    def __init__(self, errorInfo, icon):

        super().__init__()
        self.setWindowTitle('Error Message')
        self.icon = icon
        self.resize(self.minimumSizeHint())

        if self.icon: self.setWindowIcon(self.icon)

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

class InformationBox(QMessageBox):
    
    def __init__(self, message, buttons):
        ''' Consider passing in message type, error or question '''
        super().__init__()
        

    

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
    
    myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
    ''' https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105 '''
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    run()