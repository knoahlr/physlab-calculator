import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
# import main


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

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
                #Push button
        self.submitButton = QtWidgets.QPushButton("Submit", self.centralwidget)
        self.submitButton.setObjectName("pushButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.submitButton)

        self.submitButton.clicked.connect(self.handleSubmit)

        self.verticalLayout.addLayout(self.formLayout)

        self.setCentralWidget(self.centralwidget)

        
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def handleSubmit(self):
        print(self.equationLineEdit.text())
        print(self.constantsLineEdit.text())
        self.equationLineEdit.clear()
        self.constantsLineEdit.clear()
        

    def addEquationBox(self):
        label = QLabel('Equation')
        displace = label.frameWidth()
        self.vLayout.addWidget(label)
        self.EquationBox = equationBox()
        self.vLayout.addWidget(self.EquationBox)

    def addOutput(self, position):
        latexOutputBox((150, 100))

class secondaryWindow(QtGui.QWindow):
    def __init__(self):
        super().__init__()
        self.setBaseSize()
        self.setTitle("Sample Calculation")

    def addSampleCalcBox(self, position):
        equationBox(position)
        

class sampleCalculation(QtWidgets.QLineEdit):

    def __init__(self, position, boxTitle):
        super().__init__()
        self.move(position[0], position[1])
        self.setTitle(boxTitle)
        self.setBaseSize(50, 50)


def run():
    app = QApplication(sys.argv)
    myWindow = Window()
    myWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()