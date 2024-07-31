def check(value: bool, trueFunction, falseFunction):
    return trueFunction() if value else falseFunction()
