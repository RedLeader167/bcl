import bcldata

def callsub(varTable, subid):
    if subid == 1000:
        print(varTable[-1]._print())
        return True, varTable
    if subid == 1001:
        a = varTable[-33]
        b = varTable[-34]
        varTable[-35] = bcldata.Box().bset(a.bget() + b.bget())
        return True, varTable
    if subid == 1002:
        a = varTable[-33]
        b = varTable[-34]
        varTable[-35] = bcldata.Box().bset(a.bget() - b.bget())
        return True, varTable
    if subid == 1003:
        a = varTable[-33]
        b = varTable[-34]
        varTable[-35] = bcldata.Box().bset(a.bget() * b.bget())
        return True, varTable
    if subid == 1004:
        a = varTable[-33]
        b = varTable[-34]
        varTable[-35] = bcldata.Box().bset(int(a.bget() / b.bget()))
        return True, varTable
    if subid == 1100:
        varTable[-35] = 1 if varTable[-1].height > varTable[-33] else 0
        return True, varTable
    if subid == 1200:
        import time
        time.sleep(varTable[-1][0])
        return True, varTable
    return False, varTable   
    