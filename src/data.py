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

        self.equationInterExpression = self.equationExpression # ""
        self.errorInterExpression = self.errorExpression  #""

        ''' Data '''
        self.equationData = []
        self.errorData = []

        ''' Misc '''
        self.latexOutput = None
        self.maxDataLength = 0


    def floatFormatting(self, floatValue):
        ''' 
        Returns a string in unicode format
        '''
        # print(str(floatValue))
        # return '%.2E' % decimal.Decimal(str(floatValue))

        #Complex Numbers formatting. Rid oif *I and replace with i.

        return sub('[*I]+','j', str(floatValue))


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
        print(self.equationData.items())
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

            self.intermediateExpression()

        except Exception as e:

            #print(e) uncomment for debugging intermediateExpression()
            self.equationInterExpression = ""
            self.errorInterExpression = ""

        try:
            
            tableStringBlock = self.tableDesign()
        
        except Exception as e:

            tableStringBlock = ""

        string_block = 'E&= {0} \\\\ {1} \\\\ E&= {2} \\\\ {3} \sigma_E &= {4} \\\\  {5} \\\\ \sigma_E &= {6} \n {7} ' \
        .format(latex(self.equationExpression), self.equationInterExpression, expressionAns, EXPL, latex(self.errorExpression), self.errorInterExpression, errorExprAns, tableStringBlock)


        self.latexOutput.setText(string_block)

    def isNumber(self, s):
        ''' 
        Implemented in validating sample calculation inputs
        '''
        try:
            float(s)
            return True
        except ValueError:
            return False

    def dataNormality(self):

<<<<<<< HEAD
        ''' 
        In the secondary Window, if one variable has more data inputs than the other, 
        then zeros will be added to all variables and their equivalent errors so all error lists are the same size
        '''

=======
>>>>>>> 0653bd29a0ce5ac6488315e2da549be2e0041f17
        for data in self.equationData.values():
            if len(data) > self.maxDataLength: self.maxDataLength = len(data)
        
        for key, data in self.equationData.items():

            while(len(self.equationData[key]) < self.maxDataLength):

                self.equationData[key].append(0)
        
        for key, data in self.errorData.items():

            while(len(self.errorData[key]) < self.maxDataLength):

                self.errorData[key].append(0)
            '''Maybe add lines to remove excess data input in errorData '''



    

