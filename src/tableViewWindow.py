from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QFormLayout, QMainWindow, QGroupBox, QMessageBox,\
QLabel, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QScrollArea, QTableView

from PyQt5.QtWidgets import QCommonStyle, QApplication #Delete
from data import SIGMA

import pandas as pd
import numpy as np

import sys, re

ICON = r'..\articles\atom.png'

class tableWindow(QWidget):

    def __init__(self, filePath, dataInput):

        super().__init__()

        ''' MISC '''
        self.setWindowTitle("Data Import")
        self.icon = QtGui.QIcon(ICON)
        if self.icon: self.setWindowIcon(self.icon)

        ''' Data '''
        self.dataPath = filePath
        self.dataTable = None
        self.headers = None
        self.tableModel = None
        self.dataInput = dataInput

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
        self.submitButton = QPushButton("Done")
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
        self.dataTable.loc[-1] = np.array(["Select Data" for i in range(len(self.headers)) ])
        self.dataTable.index += 1
        self.dataTable = self.dataTable.sort_index()

    def getData(self):

        ''' Sub headers into dataframe columns '''

        self.dataTable.columns = self.headers
        self.dataTable = self.dataTable.drop(self.dataTable.index[0])

        for var in self.dataInput.allSymbols:

            if str(var) in self.dataTable.columns:
                self.dataInput.equationData[str(var)] = list((self.dataInput.floatFormatting(value) for value in self.dataTable.loc[:,str(var)]))

                for header in self.dataTable.columns:
                    if re.match("error{0}".format(str(var)), header, re.IGNORECASE):
                        self.dataInput.errorData['{0}{1}'.format(SIGMA, var)] = list((self.dataInput.floatFormatting(value) for value in self.dataTable.loc[:,header]))
        
        self.dataInput.dataNormalization()
        self.dataInput.postToGroupBox()
        
    # def isNumber(self, s):
    #     ''' 
    #     Implemented in validating sample calculation inputs
    #     '''
    #     try:
    #         float(s)
    #         return (True, None)
    #     except Exception as e:
    #         return (False, e)


    # def floatFormatting(self, floatValue):
    #     ''' 
    #     Returns a string in unicode format
    #     '''
    #     numCheck = self.isNumber(floatValue)

    #     '''
    #     Formatting Complex numbers to four significant figures and scientific notation
    #     '''
    #     if not numCheck[0]:
    #         if type(numCheck[1]).__name__ == 'TypeError':
    #             floatValue = re.sub('[*I]+','j', str(floatValue))
    #             floatValue = complex(re.sub('\s+',"",floatValue))
    #             return '{0:.4g}'.format(floatValue)
                
    #     floatValue = '{0:.4g}'.format(float(floatValue))
    #     return floatValue

    def handleSubmit(self):
        self.getData()
        self.close()
        


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

                return True
            else:
                self.myTableData.iat[index.row(), index.column()] = value
                self.dataChanged.emit(index, index)
                return True

        return False

    def setHeaderData(self, section, orientation, value, role):

        ''' Change column names '''
        if role == QtCore.Qt.DisplayRole:
            self.headers[section] = str(value)

    def flags(self, index):

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def verifyHeaderValue(self, value):

        ''' Check whether header name is valid '''

if __name__ == "__main__":

    print('Noah')

    app = QApplication(sys.argv)

    tableview  = tableWindow(r"C:\Users\Noah Workstation\Desktop\P_PR\repo\physlab-calculator\test\testData.csv", None)
    tableview.show()

    sys.exit(app.exec_())