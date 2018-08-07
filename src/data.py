from sympy import sympify
from errorWindow import ErrorWindow

from sympy import sympify, latex, diff, symbols, sqrt
from re import sub
from pandas import DataFrame
import sys, decimal

import enum

SIGMA = 'sigma_'
UNICODE_IDENTIFIER_PLUS_MINUS = "PLUS-MINUS SIGN"

class latexStrings(enum.Enum):
    
    EXPL = "The Corresponding error expression is,"
    tableEXPL = "Value of --- and corresponding error for values presented in table , "
    equationBegin = "\r\\begin{align}\r"
    equationEnd = "\r\end{align}\r"
    tableBegin = "\\begin{table}[]\n\centering"
    tableEnd = "\caption{caption}\n\label{tab:my_label}\n\end{table}\n"
    
'''
Data input class
 - Equation
 - Variables
 - AllSymbols
 - Constants
 '''
class userInput():

    def __init__(self, equation, allSymbols, variables):

        '''
        Data class to handle user input and generate expressions for sample calculation
        '''

        ''' Inputs '''
        self.equation = equation
        self.allSymbols = allSymbols
        self.variables = variables

        ''' Expressions '''

        self.equationExpression = sympify(self.equation)
        self.errorExpression  = self.partialDerivative()

        ''' Inter Expressions '''

        self.equationInterExpression = self.equationExpression 
        self.errorInterExpression = self.errorExpression  
        self.answerPresentation = ""

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
            if type(numCheck[1]).__name__ == 'TypeError':
                floatValue = sub('[*I]+','j', str(floatValue))
                floatValue = complex(sub('\s+',"",floatValue))
                return '{0:.4g}'.format(floatValue)
                
        floatValue = '{0:.4g}'.format(float(floatValue))
        return floatValue

    def intermediateExpression(self):
        '''
        Subs values into equations for intermediate expressions.
        i.e. cos(72) + sin(5)^2 + exp(3*24) + log(23)
        '''
        if self.equationExpression:

            for variable in self.allSymbols:

                self.equationInterExpression = sub('(?<=[^a-zA-Z]){0}(?=[^a-zA-Z])'.format(str(variable)), str(self.equationData[str(variable)][0]), str(self.equationInterExpression))  

            self.equationInterExpression = sympify(self.equationInterExpression, evaluate=False)
            self.equationInterExpression = 'E&= {0}'.format(latex(self.equationInterExpression))

        if self.errorExpression:

            for variable in self.allSymbols:

                sigmaRegEx = '{0}{1}'.format(SIGMA, str(variable))

                self.errorInterExpression = sub(sigmaRegEx, str(self.errorData[sigmaRegEx][0]), str(self.errorInterExpression))

                self.errorInterExpression = sub('(?<=[^a-zA-Z]){0}(?=[^a-zA-Z])'.format(str(variable)), str(self.equationData[str(variable)][0]), str(self.errorInterExpression))

            self.errorInterExpression = sympify(self.errorInterExpression, evaluate=False)
            self.errorInterExpression = '\sigma_E &= {0}'.format(latex(self.errorInterExpression))

    def partialDerivative(self):
        """ 
        Variables should be a tuple of sympy symbols
        Returns final expression    
        """
        diffExpression = 0

        for variable in self.variables:

            diffExpression += (diff(self.equationExpression, variable)  * sympify('{0}{1}'.format(SIGMA, str(variable))))**2

        return sqrt(diffExpression)

    def tableDesign(self):

        """ Present sample calculation data on table """

        expressionAns = [self.floatFormatting(self.equationExpression.evalf(subs={key:data[i] for key, data in self.equationData.items()})) for i in range(5)]
        errorExprAns = [self.floatFormatting(self.errorExpression.evalf(subs=dict({key:data[i] for key, data in self.equationData.items()}, \
        **{key:data[i] for key, data in self.errorData.items()}))) for i in range(5)]

        df = DataFrame({'E':expressionAns, "Error on E":errorExprAns})
    
        return df.to_latex(column_format='cccc')     

    def sampleCalculations(self):
        """ 
        Show sample calculation, with symbols replaced by numbers
        Variables should be a tuple of sympy symbols
        """
        
        #Subs expression makes a temp dictionary to use only the first value for the sample calculation 
        expressionAns = latex(self.equationExpression.evalf(subs={key:data[0] for key, data in self.equationData.items()}))
        errorExprAns = latex(self.errorExpression.evalf(subs=dict({key:data[0] for key, data in self.equationData.items()}, **{key:data[0] for key, data in self.errorData.items()})))

        try: self.intermediateExpression()
        except Exception as e:
            print(e) #uncomment for debugging intermediateExpression()
            self.equationInterExpression = ""
            self.errorInterExpression = ""
        try: 
            if self.maxDataLength > 1: self.tableDataBlock = self.tableDesign()

            self.fullTable = "{0}\n{1}\n{2}".format(self.tableBegin, self.tableDataBlock, self.tableEnd)
        except Exception as e: print(e) #uncomment for debugging intermediateExpression()

        self.answerPresentation = 'E&= {0} \u00B1 {1}'.format(expressionAns, errorExprAns) #Presents final answer, unicode in the middle is for plus minus sign
        
        string_block = '{eqBegin}\n E&= {0} {eqEnd}\\\\ {eqBegin} {1} {eqEnd} \\\\ {eqBegin}\n E&= {2} {eqEnd} {EXPL} \\\\ {eqBegin}\n \sigma_E &= {3} {eqEnd} \\\\ {eqBegin} {4} {eqEnd} \\\\ {eqBegin} \sigma_E &= {5} {eqEnd} \\\\ {eqBegin} {6} {eqEnd} {tableEXPL} \\\\ {7}' \
        .format(latex(self.equationExpression), self.equationInterExpression, expressionAns, latex(self.errorExpression),\
        self.errorInterExpression, errorExprAns, self.answerPresentation, self.fullTable, EXPL=latexStrings.EXPL.value, tableEXPL=latexStrings.tableEXPL.value, eqBegin=latexStrings.equationBegin.value , eqEnd=latexStrings.equationEnd.value)
        
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

                self.equationData[key].append(0)
        
        for key, data in self.errorData.items():

            while(len(self.errorData[key]) < self.maxDataLength):

                self.errorData[key].append(0)
            '''Maybe add lines to remove excess data input in errorData '''

            while(len(self.errorData[key]) > self.maxDataLength):

                del self.errorData[key][len(self.errorData[key]) - 1]

    def reInitializeData(self):

        ''' 
        It`s in the name
        '''

        ''' Expressions '''
        self.equationInterExpression = self.equationExpression
        self.errorInterExpression = self.errorExpression
        self.answerPresentation = ""

        ''' Data '''
        for key in self.equationData.keys(): self.equationData[key] = []
        for key in self.errorData.keys(): self.errorData[key] = []

        ''' Misc '''
        self.maxDataLength = None
        self.tableDataBlock = ""

    

