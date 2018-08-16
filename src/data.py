from sympy import sympify
from errorWindow import ErrorWindow

from sympy import sympify, latex, diff, symbols, sqrt, lambdify
from re import sub
from pandas import DataFrame
from PyQt5.QtWidgets import QLineEdit
import sys, decimal

import enum
from numpy import array
import numpy
import time

from inspect import getargspec
SIGMA = 'sigma_'
UNICODE_IDENTIFIER_PLUS_MINUS = "PLUS-MINUS SIGN"

class latexStrings(enum.Enum):
    
    EXPL = "The Corresponding error expression is,"
    tableEXPL = "Value of --- and corresponding error for values presented in table , "
    interEXPL = r'\intertext{The Corresponding error expression is,}'
    interTableEXPL = r'\intertext{ Value of --- and corresponding error for values presented in table,}'
    equationBegin = "\r\\begin{align}\r"
    equationEnd = "\r\end{align}\r"
    tableBegin = "\\begin{table}[]\n\centering"
    tableEnd = "\caption{caption}\n\label{tab:my_label}\n\end{table}\n"

class functionStrings(enum.Enum):
    SINE = "sin"
    COSINE = "cos"
    TAN = "tan"
    ARCSINE = "asin"
    ARCCOSINE = "acos"
    ARCTAN = "atan"
    EXPONENTIAL = "exp"
    LOGARITHMIC = "log"
    
'''
Data input class
 - Equation
 - Variables
 - AllSymbols
 - Constants
 '''
class userInput():

    def __init__(self, equation, allSymbols, variables, args):

        '''
        Data class to handle user input and generate expressions for sample calculation
        '''
        self.args = args
        ''' Inputs '''
        self.equation = equation
        self.allSymbols = allSymbols
        self.variables = variables
        
        ''' Secondary Window GroupBoxes '''
        self.topGroupBox = None
        self.bottomGroupBox = None

        ''' Expressions '''

        self.equationExpression = Expressions(sympify(self.equation), self.allSymbols)

        self.errorExpression  = Expressions(self.partialDerivative(), self.allSymbols)

        ''' Inter Expressions '''

        self.equationInterExpression = Expressions(sympify(self.equation), self.allSymbols)
        self.errorInterExpression = Expressions(self.partialDerivative(), self.allSymbols)

        ''' Data '''
        self.equationData = {}
        self.errorData = {}

        ''' Misc '''
        self.latexOutput = None
        self.maxDataLength = None
        self.cases = ()

        ''' Table Data '''

        self.fullTable = ""
        self.tableDataBlock = ""
        self.tableBegin = "\\begin{table}[h]\n\centering"
        self.tableEnd = "\caption{caption}\n\label{tab:my_label}\n\end{table}\n"
  
    def isNumber(self, s):
        ''' 
        Implemented in validating sample calculation inputs
        '''
        try:
            float(s)
            return (True, None)
        except Exception as e:
            return (False, e)
    # def isComplex(self, s):


    def floatFormatting(self, floatValue):
        ''' 
        Returns a string in unicode format
        '''
        numCheck = self.isNumber(floatValue)
        '''
        Formatting Complex numbers to four significant figures and scientific notation
        '''
        if not numCheck[0]:
            if type(numCheck[1]).__name__ == 'TypeError'or  type(numCheck[1]).__name__ == 'ValueError':
                floatValue = sub('[*Ii]+','j', str(floatValue)) 
                floatValue = complex(sub('\s+',"",floatValue))
                return '{0:.4g}'.format(floatValue)
                
        floatValue = '{0:.4g}'.format(float(floatValue))
        return float(floatValue)

    def intermediateExpression(self):
        '''
        Subs values into equations for intermediate expressions.
        i.e. cos(72) + sin(5)^2 + exp(3*24) + log(23)
        '''
        self.errorInterExpression.addEvaluateFalse()
        self.equationInterExpression.addEvaluateFalse()

        if self.equationExpression:

            for variable in self.allSymbols:

                self.equationInterExpression.expression = sub('(?<=[^a-zA-Z]){0}(?=[^a-zA-Z])'.format(str(variable)), str(self.equationData[str(variable)][0]), str(self.equationInterExpression.expression))  
        
            self.equationInterExpression.expression = sympify(self.equationInterExpression.expression, evaluate=False)
            self.equationInterExpression.expression = 'E&= {0}'.format(latex(self.equationInterExpression.expression))

        if self.errorExpression:

            for variable in self.allSymbols:

                sigmaRegEx = '{0}{1}'.format(SIGMA, str(variable))

                self.errorInterExpression.expression = sub(sigmaRegEx, str(self.errorData[sigmaRegEx][0]), str(self.errorInterExpression.expression))
                
                self.errorInterExpression.expression = sub('(?<=[^a-zA-Z]){0}(?=[^a-zA-Z])'.format(str(variable)), str(self.equationData[str(variable)][0]), str(self.errorInterExpression.expression))

            self.errorInterExpression.expression = sympify(self.errorInterExpression.expression, evaluate=False)

            self.errorInterExpression.expression = '\sigma_E &= {0}'.format(latex(self.errorInterExpression.expression))

    
    def partialDerivative(self):
        """ 
        Variables should be a tuple of sympy symbols
        Returns final expression    
        """
        diffExpression = 0

        for variable in self.variables:

            diffExpression += (diff(self.equationExpression.expression, variable)  * sympify('{0}{1}'.format(SIGMA, str(variable))))**2

        return sqrt(diffExpression)

    def tableDesign(self):

        """ Present sample calculation data on table """

        ''' Evaluating equations using sympy 

        sympyStart = time.time()
        expressionAns = [self.floatFormatting(self.equationExpression.expression.evalf(subs={key:data[i] for key, data in self.equationData.items()})) for i in range(self.maxDataLength)]
        errorExprAns = [self.floatFormatting(self.errorExpression.expression.evalf(subs=dict({key:data[i] for key, data in self.equationData.items()}, \
        **{key:data[i] for key, data in self.errorData.items()}))) for i in range(self.maxDataLength)]
        sympyEnd = time.time()

        '''

        mpmathStart = time.time()

        eqData = [self.equationData[str(symbol)] for symbol in self.allSymbols]
        eqData = array([list(map(self.floatFormatting, item)) for item in eqData])

        errorData = [self.errorData['{0}{1}'.format(SIGMA, str(symbol))] for symbol in self.allSymbols]
        errorData = array([list(map(self.floatFormatting, item)) for item in errorData])

        
        self.equationExpression.lambdifyExpression()
        self.errorExpression.lambdifyExpression(errorExpression=True)

        # print(getargspec(self.equationExpression.lambdaExpression))
        # print(getargspec(self.errorExpression.lambdaExpression))

        eqExpressionAns = [self.floatFormatting(self.equationExpression.lambdaExpression(*[data[i] for data in eqData])) for i in range(self.maxDataLength)]
        errorExpressionAns = [self.floatFormatting(self.errorExpression.lambdaExpression(*list([data[i] for data in eqData] + [errData[i] for errData in errorData]))) for i in range(self.maxDataLength)]

        mpmathEnd = time.time()

        #print("Time" , sympyEnd - sympyStart, mpmathEnd - mpmathStart, (sympyEnd - sympyStart)/(mpmathEnd - mpmathStart))

       
        df = DataFrame({'E':eqExpressionAns, "Error on E":errorExpressionAns})
        #print(df)

        # print('\n\nSecond DF\n\n')
        # df = DataFrame({'E':expressionAns, "Error on E":errorExprAns})
        # print(df)
    
        return df.to_latex(column_format='cccc')     

    def sampleCalculations(self):
        """ 
        Show sample calculation, with symbols replaced by numbers
        Variables should be a tuple of sympy symbols
        """
        #Subs expression makes a temp dictionary to use only the first value for the sample calculation 
        expressionAns = self.floatFormatting(self.equationExpression.expression.evalf(subs={key:data[0] for key, data in self.equationData.items()}))
        errorExprAns = self.floatFormatting(self.errorExpression.expression.evalf(subs=dict({key:data[0] for key, data in self.equationData.items()}, **{key:data[0] for key, data in self.errorData.items()})))

        try: self.intermediateExpression()
        except Exception as e:
            print(e) #uncomment for debugging intermediateExpression()
            self.equationInterExpression.expression = ""
            self.errorInterExpression.expression = ""
        
        try: 
            if self.maxDataLength > 1: self.tableDataBlock = self.tableDesign()

            self.fullTable = "{0}\n{1}\n{2}".format(self.tableBegin, self.tableDataBlock, self.tableEnd)
        except Exception as e: print(e) #uncomment for debugging intermediateExpression()

        self.answerPresentation = 'E&= {0} \u00B1 {1}'.format(expressionAns, errorExprAns) #Presents final answer, unicode in the middle is for plus minus sign

        if self.args.oneAlign:
            string_block = '\r\\begin{{align}} \n E&= {0} \\\\ {1} \\\\ E&= {2} \\\\ {3} \sigma_E &= {4} \\\\  {5} \\\\ \sigma_E &= {6} \\\\ {7} \\\\ {8} \n\end{{align}} \n{9}' \
            .format(latex(self.equationExpression.expression), self.equationInterExpression.expression, expressionAns, latexStrings.interEXPL.value, latex(self.errorExpression.expression), self.errorInterExpression.expression, \
            errorExprAns, self.answerPresentation, latexStrings.interTableEXPL.value, self.fullTable)	
        else:    
            string_block = '{eqBegin}\n E&= {0} {eqEnd}\\\\ {eqBegin} {1} {eqEnd} \\\\ {eqBegin}\n E&= {2} {eqEnd} {EXPL} \\\\ {eqBegin}\n \sigma_E &= {3} {eqEnd} \\\\ {eqBegin} {4} {eqEnd} \\\\ {eqBegin} \sigma_E &= {5} {eqEnd} \\\\ {eqBegin} {6} {eqEnd} {tableEXPL} \\\\ \n{7}' \
            .format(latex(self.equationExpression.expression), self.equationInterExpression.expression, latex(expressionAns), latex(self.errorExpression.expression),\
            self.errorInterExpression.expression, latex(errorExprAns), self.answerPresentation, self.fullTable, EXPL=latexStrings.EXPL.value, tableEXPL=latexStrings.tableEXPL.value, eqBegin=latexStrings.equationBegin.value , eqEnd=latexStrings.equationEnd.value)
            
        self.reInitializeData()
        self.latexOutput.setText(string_block)

    def dataNormalization(self):

        ''' 
        In the secondary Window, if one variable has more data inputs than the other, 
        then zeros will be added to all variables and their equivalent errors so all error lists are the same size
        '''

        self.maxDataLength = 0

        for data in self.equationData.values():
            if len(data) > self.maxDataLength: self.maxDataLength = len(data)
        
        for key, data in self.equationData.items():

            while(len(self.equationData[key]) < self.maxDataLength):

                self.equationData[key].append(str(0))
        
        for key, data in self.errorData.items():

            while(len(self.errorData[key]) < self.maxDataLength):

                self.errorData[key].append(str(0))
            '''Maybe add lines to remove excess data input in errorData '''

            while(len(self.errorData[key]) > self.maxDataLength):

                del self.errorData[key][len(self.errorData[key]) - 1]

    def postToGroupBox(self):

        for var in self.allSymbols:

            sampEquationInput= self.topGroupBox.findChild(QLineEdit, str(var))
            presentationStrings = [self.equationData[str(var)][i] for i in range(self.maxDataLength)]
            sampEquationInput.setText(", ".join(map(str, presentationStrings)))


            sampErrInput = self.bottomGroupBox.findChild(QLineEdit, str(var))
            presentationStrings = [self.errorData['{0}{1}'.format(SIGMA, var)][i] for i in range(self.maxDataLength)]
            sampErrInput.setText(", ".join(map(str, presentationStrings)))

        

    def reInitializeData(self):

        ''' 
        It`s in the name
        '''

        ''' Expressions '''
        self.equationExpression = Expressions(sympify(self.equation), self.allSymbols)
        self.errorExpression  = Expressions(self.partialDerivative(), self.allSymbols)
        self.answerPresentation = ""

        ''' Inter Expressions '''
        self.equationInterExpression = Expressions(sympify(self.equation), self.allSymbols)
        self.errorInterExpression = Expressions(self.partialDerivative(), self.allSymbols)

        ''' Data '''
        for key in self.equationData.keys(): self.equationData[key] = []
        for key in self.errorData.keys(): self.errorData[key] = []

        ''' Misc '''
        self.maxDataLength = None
        self.tableDataBlock = ""

    

class Expressions():
    
    ''' 
    Expressions class to deal with formatting expressions for various uses

    '''
    def __init__(self, expression, allSymbols):

        self.allSymbols = allSymbols
        self.expression = expression
        self.lambdaExpression = None

        


    def addEvaluateFalse(self):

        '''
        Adds evaluate=False flag to functions in expression
        '''
        for symbol in self.allSymbols:

            for func in functionStrings:

                regexString = "(?<=[^a-zA-Z]){0}\([A-Za-z0-9]\)".format(func.value)
                regexSub  = "{0}({1}, evaluate=False)".format(func.value, str(symbol))

                self.expression = sub(regexString, regexSub, str(self.expression))

    def lambdifyExpression(self, errorExpression=False):

        symbols = tuple(map(str, self.allSymbols))
        print(errorExpression)

        if not errorExpression: self.lambdaExpression = lambdify( symbols, self.expression, 'mpmath')
        else:
            symbols = tuple(map(str, self.allSymbols)) + tuple(("{0}{1}".format(SIGMA, symbol) for symbol in self.allSymbols))
            print("symbols", symbols)
            self.lambdaExpression = lambdify( symbols, self.expression, 'mpmath')

  
if __name__ == "__main__":

    logFile = open('../test/log.log', 'w')
    sys.stdout = logFile
    expr = sympify("sqrt(sigma_x**2*sin(x)**2 + 4*sigma_y**2*sin(y)**2*cos(y)**2 + sigma_z**2*(3*exp(3*z)*sin(a)*asin(z)**3 + 3*exp(3*z)*sin(a)*asin(z)**2/sqrt(-z**2 + 1))**2)")
    expr2 = sympify("exp(3*z)*sin(a)*asin(z)**3 + sin(y)**2 + cos(x)")
    symbols1 = ["x", "y", "a", "z"]
    symbols2 = ["x", "y", "a", "z", "sigma_x", "sigma_a", "sigma_y", "sigma_z"]
    datas = ((1.0,2.0,3.0,4.0), (1.0,2.0,3.0,4.0), (1.0,2.0,3.0,4.0), (1.0,2.0,3.0,4.0) )
    datas2 = ((1.0,2.0,3.0,4.0, 5.0, 6.0, 7.0, 8.0), (1.0,2.0,3.0,4.0, 5.0, 6.0, 7.0, 8.0), (1.0,2.0,3.0,4.0, 5.0, 6.0, 7.0, 8.0), (1.0,2.0,3.0,4.0, 5.0, 6.0, 7.0, 8.0))
    
    x, y, a, z, sigma_x, sigma_a, sigma_y, sigma_z = symbols("x, y, a, z, sigma_x, sigma_a, sigma_y, sigma_z")
    sDatas = {x:(1.0,2.0,3.0,4.0),y:(1.0,2.0,3.0,4.0),a:(1.0,2.0,3.0,4.0), z:(1.0,2.0,3.0,4.0)}
    sErrorDatas = {x:(1.0,2.0,3.0,4.0),y:(1.0,2.0,3.0,4.0),a:(1.0,2.0,3.0,4.0), z:(1.0,2.0,3.0,4.0), sigma_x:(5.0, 6.0, 7.0, 8.0), sigma_y:(5.0, 6.0, 7.0, 8.0), sigma_a:(5.0, 6.0, 7.0, 8.0), sigma_z:(5.0, 6.0, 7.0, 8.0)}
    finalExpr = Expressions(expr2, symbols1)
    finalerrorExpr = Expressions(expr, symbols2)


    mpStart = time.time()
    finalExpr.lambdifyExpression()
    finalerrorExpr.lambdifyExpression()

    print(getargspec(finalExpr.lambdaExpression))
    print(getargspec(finalerrorExpr.lambdaExpression))
    answer = [finalExpr.lambdaExpression(*data) for data in datas]
    answer2 = [finalerrorExpr.lambdaExpression(*data) for data in datas2]
    mpEnd = time.time()

    sympyStart = time.time()
    answer3 = [finalExpr.expression.evalf(subs={key:value[i] for key, value in sDatas.items()}) for i in range(4)]
    answer4 = [finalerrorExpr.expression.evalf(subs={key:value[i] for key, value in sErrorDatas.items()}) for i in range(4)]
    sympyEnd = time.time()

    print(mpEnd - mpStart, sympyEnd - sympyStart)
    print(answer, answer3)
    print(answer2, answer4)

    #finalExpr.lambdaExpression(*array([[1,1], [2,2], [3,3], [4,4]]) )
    #finalExpr.addEvaluateFalse()

