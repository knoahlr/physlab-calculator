from sympy import sympify, latex, diff

#Variables
def partialDerivative(variables, expression):
    """ 
    Variables should be a tuple of sympy symbols
    Returns final expression    
    """

    for variable in variables:

        expression += diff(expression, variable)
        
    return expression

def tableDesign():

    """ Present sample calculation data on table """


def sampleCalculations(expression, variables):
    """ 
    Show sample calculation, with symbols replaced by numbers
    Variables should be a tuple of sympy symbols
    """

    return '{0}//{1}'. format(latex(expression), latex(expression.evalf(variables))) 


