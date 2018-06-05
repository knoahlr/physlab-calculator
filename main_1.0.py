from gui import mainWindow, secondaryWindow
from PyQt5.QtWidgets import QApplication, QCommonStyle
import sys
''' Functions'''


if __name__ == '__main__':
    guiApp = QApplication(sys.argv)
    guiApp.setStyle(QCommonStyle())
    window = mainWindow()
    window.show()
    for i in range(50):
        print('Noah')
    sys.exit(guiApp.exec_())

   


