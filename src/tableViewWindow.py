from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QFormLayout, QMainWindow, QGroupBox, QMessageBox,\
QLabel, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QScrollArea, QTableView

from PyQt5.QtWidgets import QCommonStyle, QApplication #Delete

import pandas as pd
import numpy as np

import sys

ICON = r'..\articles\atom.png'

class tableWindow(QWidget):

    def __init__(self, filePath):

        super().__init__()

        ''' MISC '''
        self.setWindowTitle("Data Import")
        self.icon = QtGui.QIcon(ICON)

        ''' Data '''
        self.dataPath = filePath
        self.dataTable = None
        self.headers = None
        self.tableModel = None

        ''' Layout '''
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.setLayout(self.verticalLayout)

        
        ''' Resizing Window '''
        self.resize(800, 500)

        ''' Scroll '''
        self.scroll = QScrollArea()
        self.scrollLayout = QVBoxLayout(self.scroll)
        self.scroll.setLayout(self.scrollLayout)
        self.scroll.setWidgetResizable(True)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        
        ''' Two Group boxes for table view and submit button '''

        self.tableGroupBox = QGroupBox('TestData CSV')
        self.tableLayout = QVBoxLayout(self.tableGroupBox)

        self.submitGroupBox = QGroupBox()
        self.submitLayout = QVBoxLayout(self.submitGroupBox)

        ''' Table View and button '''

        self.tableView = QTableView()
        self.submitButton = QPushButton("Submit")
        self.submitButton.clicked.connect(self.handleSubmit)

        ''' Intialize and add table view '''
        self.initializeData()
        self.tableView.setModel(self.tableModel)
        
        self.scrollLayout.addWidget(self.tableGroupBox)
        self.scrollLayout.addWidget(self.submitGroupBox)
        self.verticalLayout.addWidget(self.scroll)


    def initializeData(self):

        self.readData()

        ''' Table Model '''
        self.tableModel = myTableModel(self.dataTable, self.headers)

        ''' layout for Group boxes '''
        self.tableLayout.addWidget(self.tableView)
        self.submitLayout.addWidget(self.submitButton)


    def readData(self):

        self.dataTable = pd.read_csv(r"{0}".format(self.dataPath))
        
        self.headers = list(self.dataTable.columns.values)
        self.dataTable.loc[-1] = np.array(["" for i in range(len(self.headers)) ])
        self.dataTable.index += 1
        self.dataTable = self.dataTable.sort_index()
        

    def handleSubmit(self):
        pass


class myTableModel(QtCore.QAbstractTableModel):

    def __init__(self, tableData, headers):
        super().__init__()

        self.myTableData = tableData
        self.headers = headers
        self.defaultHeaders = list(headers) #using a constructor so data doesn`t point to same place in memory. Can easily change headers now.


    def rowCount(self, parent):
        return self.myTableData.shape[0]

    def columnCount(self, parent):
        return self.myTableData.shape[1]
 

    def data(self, index, role=QtCore.Qt.DisplayRole):
        
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                i = index.row()
                j = index.column()

                return '{0}'.format(self.myTableData.iat[i, j])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.headers[col]
        return None
    def setData(self, index, value, role):

        if index.isValid():
            if index.row() == 0:
                if value == "": 
                    self.headers[index.column()] = self.defaultHeaders[index.column()]
                    self.dataChanged.emit(index, index)
                    return True
                self.headers[index.column()] = value
                self.myTableData.iat[index.row(), index.column()] = value
                self.dataChanged.emit(index, index)
            ''' Implement Data Edit '''

            return True
        return False

    def setHeaderData(self, section, orientation, value, role):

        ''' Change column names '''
        if role == QtCore.Qt.DisplayRole:
            self.headers[section] = str(value)
            print(self.headers)

    def flags(self, index):

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def verifyHeaderValue(self, value):

        ''' Check whether header name is valid '''

  



    


if __name__ == "__main__":

    print('Noah')

    app = QApplication(sys.argv)
    app.setStyle(QCommonStyle())

    

    tableview  = tableWindow(r"C:\Users\Noah Workstation\Desktop\P_PR\repo\physlab-calculator\test\testData.csv")
    tableview.show()

    sys.exit(app.exec_())