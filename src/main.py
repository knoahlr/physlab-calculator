import sys, time, ctypes, re, argparse
from mainWindow import mainWindow
from secondaryWindow import secondaryWindow

from PyQt5.QtWidgets import QCommonStyle, QApplication
ICON = r'articles\atom.png'



if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--oneAlign", help="Represent equations in one align block", action="store_true" ,default=False)
    args = parser.parse_args()
    
    logFile = open('../test/mainlog.log', 'w')
    sys.stdout = logFile

    myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
    ''' https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105 '''
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    #app.setStyle(QCommonStyle())


    window = mainWindow(args)
    window.show()
    sys.exit(app.exec_())