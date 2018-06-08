import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

# import main


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        '''Fields'''
        self.equation_variables = {'equation':None,'variables':None}
        self.secondWindow = secondaryWindow()


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
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.textEdit)

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
        self.equation_variables['equation'] = self.equationLineEdit.text()[0]
        self.equation_variables['variables'] = self.variablesLineEdit.text()[0]
        self.equationLineEdit.clear()
        self.variablesLineEdit.clear()

        variables = self.equation_variables['variables'].strip('\s').split(',')
        equation = self.equation_variables['equation'].strip('\s')

        ''' Integrate with LaTex backend here, also launch secondary window for sample calculations '''
        
class secondaryWindow(QWidget):
    
    def __init__(self):
        super().__init__()

        '''Data Fields'''
        self.eqData = dict()
        self.errData = dict()

        self.setWindowTitle("Sample Calculation")
        self.setObjectName("SampleCalc")
        self.resize(self.sizeHint())
        

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.setLayout(self.verticalLayout)

        self.topGroupBox = self.designGroupBox('Equation - Sample Calculation')      
        self.bottomGroupBox = self.designGroupBox('Error - Sample Calculation')

        #setting Group Box layout
        self.topGroupBox1formLT = QFormLayout(self.topGroupBox)
        self.topGroupBox2formLT = QFormLayout(self.bottomGroupBox)


   
        self.verticalLayout.addWidget(self.topGroupBox)
        self.verticalLayout.addWidget(self.bottomGroupBox)
        self.addInputs(['cow','dog','monkey','Mosquito', 'Rhino'], self.topGroupBox1formLT, self.topGroupBox)
        self.addInputs(['Noah','Hannah','Chris', 'Mauro'], self.topGroupBox2formLT, self.bottomGroupBox)

    def designGroupBox(self, boxTitle):

        box = QGroupBox(boxTitle)
        #styling
        return box

    def addInputs(self, variables, layout, topGroupBox):

        self.row = 0

        for variable in variables:

            self.inputLabel = QLabel(variable, topGroupBox)
            self.input = QLineEdit(topGroupBox)
            self.input.setPlaceholderText(variable)
            layout.setWidget(self.row, QFormLayout.LabelRole, self.inputLabel)
            layout.setWidget(self.row, QFormLayout.FieldRole,self.input)
            self.row += 1
        
        return layout
'''Error Window Class Definition here'''
#class ErrorWindow(QWidget):
    

'''Line and Text edit custom implementation here'''
# class EquationVarEdit(QtWidgets.QLineEdit):


#class LatexOutEdit(QtWidgets.QTextEdit):




    
    
def run():
    app = QApplication(sys.argv)
    app.setStyle(QCommonStyle())
    window = mainWindow()
    myWindow = secondaryWindow()
    myWindow.show()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()