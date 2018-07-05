from sympy import sympify, latex, diff, symbols, sqrt
from re import sub
from pandas import DataFrame
import sys, decimal


SIGMA = 'sigma_'

EXPL = r'\intertext{The Corresponding error expression is,}'

def floatFormatting(floatValue):
    ''' Returns a string in unicode format '''
    print(str(floatValue))
    return '%.2E' % decimal.Decimal(str(floatValue))


def intermediateExpression(expression, allSymbols, eqData, errorData):

    for variable in allSymbols:

        sigmaRegEx = '{0}{1}'.format(SIGMA, variable)

        expression = sub(sigmaRegEx, str(errorData[sigmaRegEx][0]), str(expression))

        expression = sub('(?<=[^a-zA-Z]){0}(?=[^a-zA-Z])'.format(str(variable)), str(eqData[str(variable)][0]), str(expression))  

    return sympify(expression, evaluate=False)

#Variables
def partialDerivative(variables, expression):
    """ 
    Variables should be a tuple of sympy symbols
    Returns final expression    
    """
    diffExpression = 0

    for variable in variables:

        diffExpression += (diff(expression, variable)  * sympify('{0}{1}'.format(SIGMA, str(variable))))**2

    return sqrt(diffExpression)

def tableDesign(expression , errorExpression, samplData):

    """ Present sample calculation data on table """

    eqData = samplData[0]
    errorData = samplData[1]
    expressionAns = []
    errorExprAns = []

    ex = [expression.evalf(subs={key:data[i] for key, data in eqData.items()}) for i in range(5)]

    expressionAns = [expression.evalf(subs={key:data[i] for key, data in eqData.items()}) for i in range(5)]
    errorExprAns = [errorExpression.evalf(subs=dict({key:data[i] for key, data in eqData.items()}, \
    **{key:data[i] for key, data in errorData.items()}))for i in range(5)]

    df = DataFrame({'E':expressionAns, SIGMA:errorExprAns})
 
    return df.to_latex()     


def sampleCalculations(expression, errorExpression, samplData, allSymbols):
    """ 
    Show sample calculation, with symbols replaced by numbers
    Variables should be a tuple of sympy symbols
    """
    eqData = samplData[0]
    errorData = samplData[1]
    expression = sympify(expression)
    tableStringBlock = None

    #Subs expression makes a temp dictionary to use only the first value for the sample calculation 
    #print(latex(expression.evalf(subs={key:data[0] for key, data in eqData.items()}), mul_symbol='times'))
    expressionAns = latex(expression.evalf(subs={key:data[0] for key, data in eqData.items()}))
    errorExprAns = latex(errorExpression.evalf(subs=dict({key:data[0] for key, data in eqData.items()}, **{key:data[0] for key, data in errorData.items()})))

    try:

        errInterExpression = '\sigma_E &= {0}'.format(latex(intermediateExpression(errorExpression, allSymbols, eqData, errorData)))
        eqInterExpression = 'E&= {0}'.format(latex(intermediateExpression(expression, allSymbols, eqData, errorData)))
    
    except Exception as e:

        errInterExpression = ""
        eqInterExpression  = ""

    try:
        
        tableStringBlock = tableDesign(expression, errorExpression, samplData)
    
    except Exception as e:
         
        print(e) 
        tableStringBlock = ""

    string_block = 'E&= {0} \\\\ {1} \\\\ E&= {2} \\\\ {3} \sigma_E &= {4} \\\\  {5} \\\\ \sigma_E &= {6} \n {7} ' \
    .format(latex(expression), eqInterExpression, expressionAns, EXPL, latex(errorExpression), errInterExpression, errorExprAns, tableStringBlock)


    return string_block

def isNumber(s):
    ''' Implemented in validating sample calculation inputs'''
    try:
        float(s)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    
    expression = sympify('x^2 +(a^3)*b')
    x, a, b = symbols('x a b')

    variables =  {'x':4, 'y':3, 'z':7}

    eqData, errorData = {'x': '23', 'y': '23', 'z': '23'}, {'sigma_x': '0.023', 'sigma_y': '0.023', 'sigma_z': '0.023'}


    #print(sampleCalculations(partialDerivative(variables, expression), variables))
    expression = 'exp(3*z)*asin(z)**3 + sin(y)**2 + cos(x)'
    errorExpression = 'sqrt(sigma_x**2*sin(x)**2 + 4*sigma_y**2*sin(y)**2*cos(y)**2 + sigma_z**2*(3*exp(3*z)*asin(z)**3 + 3*exp(3*z)*asin(z)**2/sqrt(-z**2 + 1))**2)'
    
    print(intermediateExpression(errorExpression, variables, eqData, errorData))