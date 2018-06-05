import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

# import main


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        '''Fields'''
        self.equation_constants = {'equation':None,'constants':None}
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

        self.constantsLabel = QtWidgets.QLabel("Constants", self.centralwidget)
        self.constantsLabel.setObjectName("constantsLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.constantsLabel)

        self.label = QtWidgets.QLabel("Latex Output", self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label)

        #Equation and constants text editors
        self.equationLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.equationLineEdit.setObjectName("equationLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.equationLineEdit)

        self.constantsLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.constantsLineEdit.setObjectName("constantsLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.constantsLineEdit)

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
        self.equation_constants['equation'] = self.equationLineEdit.text()[0]
        self.equation_constants['constants'] = self.constantsLineEdit.text()[0]
        self.equationLineEdit.clear()
        self.constantsLineEdit.clear()

        constants = self.equation_constants['constants'].strip('\s').split(',')
        equation = self.equation_constants['equation'].strip('\s')

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