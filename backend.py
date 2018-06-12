from sympy import sympify, latex, diff, symbols, sqrt

SIGMA = 'sigma_'

EXPL = r'\intertext{The Corresponding error expression is,}'




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


def sampleCalculations(expression, errorExpression, samplData):
    """ 
    Show sample calculation, with symbols replaced by numbers
    Variables should be a tuple of sympy symbols
    """
    eqData = samplData[0]
    errorData = samplData[1]

    expression = sympify(expression)
    expressionAns = latex(expression.evalf(subs=eqData))

    errorExprAns = latex(errorExpression.evalf(subs=dict(eqData, **errorData)))

    string_block = r'E&= {0} \\ E&= {1} \\ {2} \sigma_E &= {3} \\ \sigma_E &= {4}'.format(latex(expression), expressionAns, EXPL, latex(errorExpression), errorExprAns)

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
    variables =  {x:4, a:3, b:7}
    print(sampleCalculations(partialDerivative(variables, expression), variables))