from sympy import sympify, latex, diff, symbols

#Variables
def partialDerivative(variables, expression):
    """ 
    Variables should be a tuple of sympy symbols
    Returns final expression    
    """
    diffExpression = 0

    for variable in variables:

        diffExpression +=  diff(expression, variable)

    return diffExpression

def tableDesign():

    """ Present sample calculation data on table """


def sampleCalculations(expression, variables):
    """ 
    Show sample calculation, with symbols replaced by numbers
    Variables should be a tuple of sympy symbols
    """

    return '={0} // ={1}'. format( latex(expression), latex(expression.evalf(subs=variables)) ) 


if __name__ == '__main__':
    expression = sympify('x^2 +(a^3)*b')
    x, a, b = symbols('x a b')
    variables =  {x:4, a:3, b:7}
    print(sampleCalculations(partialDerivative(variables, expression), variables))