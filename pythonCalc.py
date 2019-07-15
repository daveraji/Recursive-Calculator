import logging
from flask import Flask, render_template, jsonify, request, redirect, url_for
app = Flask(__name__)

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('values')

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('values')

def deconstructor(arr):
    '''
    This function takes the full array of operations for the calculator and sends out an array
    of numbers and signs to break down the operation
    '''
    bool=False #method for keeping track of multiple digit numbers
    expression=[]
    for a in arr:
        if ord(a) in list(range(48,58))+[46, 56]: #if a number
            if bool:
                expression[len(expression)-1] += a #add the number to the last number in the list
                bool=True
            else:
                expression.append(a)
                bool = True
        elif ord(a) in [40,41,42,43,45,47,94]:
            expression.append(a)
            bool = False
        else:
            raise Exception('Wrong syntax on input - Use only numbers, operations and brackets')
    logger.warning('expression: %s', expression)
    return expression

def function(sign, num1, num2):
    '''
    This function takes in the sign and two numbers and returns the solution (solving the smallest problem)
    '''
    if sign=="^":
        return num1**num2
    elif sign=="/":
        return num1/num2
    elif sign=="*":
        return num1*num2
    elif sign=="+":
        return num1+num2
    elif sign=="-":
        return num1-num2

def calculate_num(expression):
    '''
    This is the function that recursively solves the smallest calculation and returns it to the main arrays until
    spits out the final value of the calculation
    '''
    tiers = [['^',''],['/','*'],['+','-']]

    if len(expression) == 1:  # basecase
        logger.warning('numresult: %s', expression[0])
        return expression[0]

    #handle recursive math
    for tier in tiers:
        for sign in expression:
            if sign in tier:
                index = expression.index(sign) #issue how do you know right instance of index? does that matter?
                expression[index]= function(expression[index],float(expression[index-1]), float(expression[index+1]))
                del expression[index-1]
                del expression[index]
                #logger.warning('breakdown: %s', expression)
                return calculate_num(expression)


def calculate_brack(expression):
    #base case
    if len(expression) == 1:  # basecase
        logger.warning('basebrack: %s', expression)
        return expression[0]

    #recursive case
    if '(' in expression:
        brack_open = dict(map(reversed, enumerate(expression)))['('] #find last open bracket
        brack_close =next(i for i in range(len(expression)) if expression[i]==')' and i > brack_open)  #find first closed after that
        #brack_close = expression.index(')')
        #run brack calc on all the numbers minus the open bracket
        logger.warning('when theres brack opens: %s, %s, %s', expression, str(brack_open), str(brack_close))
        expression[brack_open:brack_close+1] = [calculate_num(expression[brack_open+1: brack_close])] #replace bracket with number
        logger.warning('changed expression after evaluating brack: %s, %s, %s', expression, str(brack_open), str(brack_close))
        #return expression where the bracket is replaced by the number
        return calculate_brack(expression)
    else:
        return calculate_num(expression)


@app.route('/', methods=['GET','POST'])
def index(result=0):
    if request.method == 'POST':
        entry = str(request.form['result'])
        try:
            expression = deconstructor(entry)
            result = calculate_brack(expression)
        except Exception as e:
            result = e
            #logger.warning('result: %s', result)
            #return redirect(url_for('processor'))
    return render_template('CalcUI.html', title='Calculator Home', final=result)

'''
    Next tings to do:
    Bracket funcitonality (DONE)
    When you finish a function - go to index with answer already in the form
    add database of answers.
        - when you click on an answer it will be added to the demo value.
'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
