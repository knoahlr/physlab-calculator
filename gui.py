import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
# import main


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #Menus
        menubar = self.menuBar()
        menubar.addMenu('File')

        self.setMinimumSize(800, 300)
        self.setGeometry(1000, 1000, 500, 300)
        self.setWindowTitle("PyQt5 Trial")

        #BaseLayout and Central widget
        # centreW = QWidget()
        # self.baseLayout = QBoxLayout(0)
        
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName('centralWidget')

        #Labels
        self.eqlabel = QtWidgets.QLabel(self.centralwidget)
        self.eqlabel.setGeometry(QtCore.QRect(40, 40, 89, 25))
        self.eqlabel.setObjectName("Equation")

        self.eqEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.eqEdit.setGeometry(QtCore.QRect(120, 40, 181, 31))
        self.eqEdit.setObjectName("equation editor")

        self.latexOut = QtWidgets.QTextEdit(self.centralwidget)
        self.latexOut.setGeometry(QtCore.QRect(110, 120, 661, 140))
        self.latexOut.setObjectName("Latex Output")

        self.latexOutLabel = QtWidgets.QLabel(self.centralwidget)
        self.latexOutLabel.setGeometry(QtCore.QRect(30, 160, 89, 25))
        self.latexOutLabel.setObjectName("latex Output Label")

        self.submit = QtWidgets.QPushButton(self.centralwidget)
        self.submit.setGeometry(QtCore.QRect(320, 50, 61, 21))
        self.submit.setObjectName("submit")

        self.setCentralWidget(self.centralwidget)

        #self.centralWidget().setLayout(self.baseLayout)

        #Secondary Customizations
        # topLayout = QHBoxLayout() #.minimumSize(QBoxLayout.sizeHint())
        # bottomLayout = QHBoxLayout()#.minmumSize(QBoxLayout.sizeHint())
        # self.baseLayout.addWidget(topLayout)
        # self.baseLayout.addWidget(bottomLayout)

        

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
        
class equationBox(QtWidgets.QLineEdit):
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Equation")
        self.setFrame(True)
        self.setFixedSize(self.sizeHint())
        #self.move(position[0], position[1])
        #self.show()
        #Continue class definition


class latexOutputBox(QtWidgets.QTextEdit):
    def __init__(self, position):
        super().__init__()
        self.setPlaceholderText("LaTex OutPut")
        self.move(position[0], position[1])
        #self.move()
        #Continue class definition


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