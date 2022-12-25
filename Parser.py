import sys


def getChar(variable, varType):
    if (variable in varMap):
        varList = list(varMap[variable])
        return varList
    else:
        if (varType == 'int'):
            try:
                varList = [int(variable), varType]
                return varList
            except ValueError:
                sys.exit("Syntax-Error")
        elif (varType == 'real'):
            try:
                varList = [float(variable), varType]
                return varList
            except ValueError:
                sys.exit("Syntax-Error")


def addChar():
    global i, nextChar
    i += 1
    if (len(tokenList) == 0):
        print('Empty-File')
    if (i <= len(tokenList) - 1):
        nextChar = tokenList[i]
    else:
        nextChar = ''


def lookup(lft, mathOperator, right):
    rNum = right[VAL]
    if (lft[TYPE] == right[TYPE]):
        if (mathOperator == '+'):
            lft[VAL] += rNum
            return lft
        elif (mathOperator == '-'):
            lft[VAL] -= rNum
            return lft
        elif (mathOperator == '*'):
            lft[VAL] *= rNum
            return lft
        elif (mathOperator == '/'):
            lft[VAL] /= rNum
            return lft
        else:
            sys.exit("Syntax-Error")
    else:
        sys.exit("Syntax-Error")


def lex():
    global varMap
    while (i <  len(tokenList) - 2):
        stmtList()
    if (nextChar == ''):
        return
    else:
        sys.exit("Syntax-Error")


def stmtList():
    if (nextChar == 'print'):
        match('print')
        programList = expr('int')
        if (nextChar == ';'):
            match(';')
            print(programList[VAL])
            return
        else:
            sys.exit("Syntax-Error")
    else:
        stmt()

    return


def stmt():
    global varMap
    varType, varVal = 'int', None
    varName = nextChar
    addChar()
    if (nextChar == '='):
        match(nextChar)
        varVal = expr(varType)
        match(';')
    else:
        sys.exit('System Errors')
    varMap[varName] = (varVal[VAL], varType)
    return


def expr(varType):
    leftT = term(varType)
    while (True):
        if (nextChar == '+'):
            match(nextChar)
            rightT = term(varType)
            leftT = lookup(leftT, '+', rightT)
        elif (nextChar == '-'):
            match(nextChar)
            rightT = term(varType)
            leftT = lookup(leftT, '-', rightT)
        elif (nextChar == ')' or nextChar == ';' or nextChar == 'end'):
            break
        else:
            sys.exit("Syntax-Error")
    return leftT


def term(varType):
    leftF = factor(varType)
    while (True):
        if (nextChar == '*'):
            match(nextChar)
            rightF = factor(varType)
            leftF = lookup(leftF, '*', rightF)
        elif (nextChar == '/'):
            match(nextChar)
            rightF = factor(varType)
            leftF = lookup(leftF, '/', rightF)
        else:
            break
    return leftF


def factor(varType):
    returnList = []
    if (nextChar == '('):
        match(nextChar)
        ExpValue = expr(varType)
        returnList = [ExpValue[VAL], varType]
        match(')')
    elif (nextChar == 'int' or nextChar == 'real'):
        varType = type()
        if (nextChar == '('):
            match(nextChar)
            value = getChar(nextChar, varType)
            match(nextChar)
            returnList = [value[VAL], varType]
            match(')')
    else:
        returnList = getChar(nextChar, varType)
        addChar()
    return returnList


def match(token):
    if (token == nextChar):
        addChar()
    else:
        sys.exit("Syntax-Error")


def main():
    global tokenList
    file = open(sys.argv[1], 'r')
    tokenList = file.read().split()
    addChar()
    lex()

if __name__ == "__main__":
    i = -1
    VAL = 0
    TYPE = 1
    tokenList = []
    varMap = {}
    nextChar = None
    main()