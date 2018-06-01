import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
# import main


class Window(QMainWindow):
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

        #submit button
        self.submitButton = QtWidgets.QPushButton("Submit", self.centralwidget)
        self.submitButton.setObjectName("pushButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.submitButton)

        self.submitButton.clicked.connect(self.handleSubmit)

        self.verticalLayout.addLayout(self.formLayout)

        self.setCentralWidget(self.centralwidget)

        
    def center(self):#Center Main window in active screen. Uses cursor position as reference.
        
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


        
        
class secondaryWindow(QWidget):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sample Calculation")
        self.setObjectName("SampleCalc")
        self.resize(self.sizeHint())
        self.row = 0

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.setLayout(self.verticalLayout)

        self.frame = QtWidgets.QFrame()
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.setMidLineWidth(2)
        self.frame.setLineWidth(2)
        

        self.frame_2 = QtWidgets.QFrame()
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)

        self.frame_2.setMidLineWidth(2)
        self.frame_2.setLineWidth(2)
        self.frame_2.setObjectName("frame_2")

        self.frame1formLT = QFormLayout(self.frame)

        self.addInputs(['cow','dog','monkey'], self.frame1formLT, self.frame)
        self.addInputs(['Noah','Hannah','Chris'], self.frame1formLT, self.frame_2)
   
        self.verticalLayout.addWidget(self.frame)
        self.verticalLayout.addWidget(self.frame_2)

    def addInputs(self, variables, layout, frame):


        for variable in variables:

            self.inputLabel = QLabel(variable, frame)
            self.input = QLineEdit(frame)
            self.input.setPlaceholderText(variable)
            layout.setWidget(self.row, QFormLayout.LabelRole, self.inputLabel)
            layout.setWidget(self.row, QFormLayout.FieldRole,self.input)
            self.row += 1
        
        return layout


    
    
def run():
    app = QApplication(sys.argv)
    myWindow = secondaryWindow()
    myWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()