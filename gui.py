import sys
from PyQt5 import QtGui, QtCore, QtWidget
from PyQt5.QtWidgets import QApplication, QWidget
import main


class Window(QtGui.QWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setTitle("PyQt5 Trail")
        self.setIcon(QtGui.QIcon('BlackPanther.png'))
        self.equationBox()
        self.sampleCalcBox()
        self.latexOutputBox()

    # def equationBox(self):
    #     print('To be implemented')

    # def latexOutputBox(self):
    #     print('To be implemented')

class equationBox(QtWidget.QLineEdit):
    def __init__(self, position):
        super().__init__()
        #Continue class definition


class latexOutputBox(QtWidget.QTextBox):
    def __init__(self, position):
        super().__init__()
        #Continue class definition


class sampleCalculation(QWidget.QLineEdit):

    def __init__(self, position, boxTitle):
        super().__init__()
        self.move(position[0], position[1])
        self.setTitle(boxTitle)


def run():
    app = QtGui.QGuiApplication(sys.argv)
    myWindow = Window() 
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()