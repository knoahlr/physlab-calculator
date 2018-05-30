import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication
# import main


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        menubar = self.menuBar()
        menubar.addMenu('File')
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PyQt5 Trial")

    def addEquationBox(self):
        self.EquationBox = equationBox((80, 20))

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
    def __init__(self, position):
        super().__init__()
        self.setPlaceholderText("Equation")
        self.move(position[0], position[1])
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
    myWindow.addEquationBox()
    myWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()