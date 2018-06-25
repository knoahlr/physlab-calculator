from sympy import sympify, latex, diff, symbols, sqrt
from re import sub
import sys

SIGMA = 'sigma_'

EXPL = r'\intertext{The Corresponding error expression is,}'

def intermediateExpression(expression, allSymbols, eqData, errorData):

    for variable in allSymbols:

        sigmaRegEx = '{0}{1}'.format(SIGMA, variable)

        expression = sub(sigmaRegEx, str(errorData[sigmaRegEx]), str(expression))

        expression = sub('(?<=[^a-zA-Z]){0}(?=[^a-zA-Z])'.format(str(variable)), str(eqData[str(variable)]), str(expression))  

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

def tableDesign():

    """ Present sample calculation data on table """


def sampleCalculations(expression, errorExpression, samplData, allSymbols):
    """ 
    Show sample calculation, with symbols replaced by numbers
    Variables should be a tuple of sympy symbols
    """
    eqData = samplData[0]
    errorData = samplData[1]
    expression = sympify(expression)
    expressionAns = latex(expression.evalf(subs=eqData))

    errorExprAns = latex(errorExpression.evalf(subs=dict(eqData, **errorData)))

    try:

        errInterExpression = '\sigma_E &= {0}'.format(latex(intermediateExpression(errorExpression, allSymbols, eqData, errorData)))
        eqInterExpression = 'E&= {0}'.format(latex(intermediateExpression(expression, allSymbols, eqData, errorData)))
    
    except Exception as e:

        errInterExpression = ""
        eqInterExpression  = ""


    string_block = r'E&= {0} \\ {1} \\ E&= {2} \\ {3} \sigma_E &= {4} \\  {5} \\ \sigma_E &= {6}' \
    .format(latex(expression), eqInterExpression, expressionAns, EXPL, latex(errorExpression), errInterExpression, errorExprAns)

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