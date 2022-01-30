import inspect

def whoami():
    return inspect.stack()[1][3]

def whosdaddy():
    return inspect.stack()[2][3]

def dbgP(*args):
    print(whosdaddy())
    logStr = ''
    for i in args:
        logStr += str(i) + ":" + str(type(i))
    print(logStr)
