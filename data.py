from sympy import sympify
from errorWindow import ErrorWindow

from sympy import sympify, latex, diff, symbols, sqrt
from re import sub
from pandas import DataFrame
import sys, decimal

SIGMA = 'sigma_'
UNICODE_IDENTIFIER_PLUS_MINUS = "PLUS-MINUS SIGN"
EXPL = r'\intertext{The Corresponding error expression is,}'

'''
Data input class
 - Equation
 - Variables
 - AllSymbols
 - Constants
 '''
class userInput():

    def __init__(self, equation, allSymbols, variables):

        ''' Inputs '''
        self.equation = equation
        self.allSymbols = allSymbols
        self.variables = variables

        ''' Expressions '''

        self.equationExpression = sympify(self.equation)
        self.errorExpression  = self.partialDerivative()

        ''' Inter Expressions '''

        self.equationInterExpression = ""
        self.errorInterExpression = ""

        ''' Data '''
        self.equationData = []
        self.errorData = []

        ''' Misc '''
        self.latexOutput = None


    def floatFormatting(self, floatValue):
        ''' Returns a string in unicode format '''
        # print(str(floatValue))
        # return '%.2E' % decimal.Decimal(str(floatValue))

        #Complex Numbers formatting. Rid oif *I and replace with i.

        return sub('[*I]+','j', str(floatValue))


    def intermediateExpression(self):

        if self.equationExpression:

            self.equationInterExpression = self.equationExpression

            for variable in self.allSymbols:

                self.equationInterExpression = sub('(?<=[^a-zA-Z]){0}(?=[^a-zA-Z])'.format(str(variable)), str(self.equationData[str(variable)][0]), str(self.equationExpression))  


        if self.errorExpression:

            self.errorInterExpression = self.errorExpression

            for variable in self.allSymbols:

                sigmaRegEx = '{0}{1}'.format(SIGMA, str(variable))

                self.errorInterExpression = sub(sigmaRegEx, str(self.errorData[sigmaRegEx][0]), str(self.errorInterExpression))

                self.errorInterExpression = sub('(?<=[^a-zA-Z]){0}(?=[^a-zA-Z])'.format(str(variable)), str(self.equationData[str(variable)][0]), str(self.errorInterExpression))


        return sympify(self.equationInterExpression, evaluate=False), sympify(self.errorInterExpression, evaluate=False)

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

        df = DataFrame({'E':expressionAns, "{0}E".format(SIGMA):errorExprAns})
    
        return df.to_latex()     


    def sampleCalculations(self):
        """ 
        Show sample calculation, with symbols replaced by numbers
        Variables should be a tuple of sympy symbols
        """
        
        #Subs expression makes a temp dictionary to use only the first value for the sample calculation 
        #print(latex(expression.evalf(subs={key:data[0] for key, data in eqData.items()}), mul_symbol='times'))
        expressionAns = latex(self.equationExpression.evalf(subs={key:data[0] for key, data in self.equationData.items()}))
        errorExprAns = latex(self.errorExpression.evalf(subs=dict({key:data[0] for key, data in self.equationData.items()}, **{key:data[0] for key, data in self.errorData.items()})))

        try:
            intermediateExpressions = self.intermediateExpression()
            errInterExpression = '\sigma_E &= {0}'.format(latex(intermediateExpressions[1]))
            eqInterExpression = 'E&= {0}'.format(latex(intermediateExpressions[0]))
        
        except Exception as e:

            print(e)

            errInterExpression = ""
            eqInterExpression  = ""

        try:
            
            tableStringBlock = self.tableDesign()
        
        except Exception as e:
            
            print(e) 
            tableStringBlock = ""

        string_block = 'E&= {0} \\\\ {1} \\\\ E&= {2} \\\\ {3} \sigma_E &= {4} \\\\  {5} \\\\ \sigma_E &= {6} \n {7} ' \
        .format(latex(self.equationExpression), eqInterExpression, expressionAns, EXPL, latex(self.errorExpression), errInterExpression, errorExprAns, tableStringBlock)


        self.latexOutput.setText(string_block)

    def isNumber(self, s):
        ''' Implemented in validating sample calculation inputs'''
        try:
            float(s)
            return True
        except ValueError:
            return False


