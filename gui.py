import sys
from PyQt5 import QtGui, QtCore
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

    def equationBox(self):
        print('To be implemented')
    def sampleCalcBox(self):
        print('To be implemented')
    def latexOutputBox(self):
        print('To be implemented')



def run():
    app = QtGui.QGuiApplication(sys.argv)
    myWindow = Window() 
    sys.exit(app.exec_())

run()