import ex
import bcldata

rs = ex.IResult
ha = ex.hasarg
tk = ex.PToken

class Interpreter:
    def __init__(self, precmds, postcmds, throwfun):
        self.throwfun = throwfun
        #self.varTable = {}
        self.varTable = bcldata.VarTable(self.throwfun)
        self.labelTable = {}
        self.comeTable = {}
        self.flapStack = []
        self.imports = []
        for i in range(-32, 0):
            self.varTable[i] = bcldata.Shelf(99, self.throwfun)
        for i in range(-64, -32):
            self.varTable[i] = bcldata.Box()
        #print(self.varTable.items)
        self.reinit(precmds, postcmds)
    
    def reinit(self, precmds, postcmds):
        self.precmds = precmds
        self.postcmds = postcmds
        self.index = -1
        self.token = None
    
    def advancepre(self):
        self.index += 1
        self.token = self.precmds[self.index] if self.index < len(self.precmds) else None
    
    def advance(self):
        self.index += 1
        self.token = self.postcmds[self.index] if self.index < len(self.postcmds) else None
    
    def executepre(self):
        self.advancepre()
        while self.token != None:
            if self.token.t == "LABEL":
                self.labelTable[self.token.v[0]] = self.token.v[1]
            elif self.token.t == "COMEFROM":
                tol = None
                for l in self.precmds:
                    if l.t == "LABEL":
                        if self.token.v[0] == l.v[0]: tol = l.v[1]
                if not tol:
                    self.throwfun(8)
                self.comeTable[tol] = self.token.v[1]
            self.advancepre()
        
        #print(self.labelTable, self.comeTable)
    
    def execute(self):
        self.advance()
        while self.token != None:
            if self.index in self.comeTable:
                self.index = self.comeTable[self.index]
            else:
                self.varTable[1001].bset(self.index)
                res = self.eval(self.token)
                if res.error:
                    if res.error == 0:
                        break
                    self.throwfun(res.error)
                self.index = self.varTable[1001].bget()
            self.advance()
    
    def getval(self, tk, tk2=None):
        #print(type(tk).__name__, tk)
        if tk.ct("NUMBER") or tk.ct("SHELFID") or tk.ct("STRING"): return tk.v
        if tk.ct("BOX") or tk.ct("SHELF"):
            v = self.varTable.get(tk.v, None)
            if v == None: self.throwfun(12)
            if tk.ct("SHELF"):
                if tk2 != None:
                    if tk2.ct("SHELFID") or tk2.ct("NUMBER"):
                        return v.get(tk2.v)
                    elif tk2.ct("BOX"):
                        return v.get(self.varTable[tk2.v].bget())
                return v._print()
            return v.bget()
        return None

    def eval(self, token):
        if ex.debug: print(token, self.index)
        if ha(token, 0):
            if token[0].ct("EOF"): return rs(0)
            if not token[0].isID(): return rs(7)
            if not token[0].cv("DO"): return rs(7)
            if not ha(token, 1): return rs(7)
            if token[1].isID() and token[1].v.startswith("NOT"): return rs()
            if token[1].cv("MATERIALIZE"):
                if not ha(token, 2): return rs(7)
                if token[2].t not in ("SHELF", "BOX"): return rs(7)
                if token[2].ct("SHELF"):
                    if not ha(token, 3): return rs(7)
                    if not token[3].ct("SHELFID"): return rs(7)
                    if self.varTable.get(token[2].v, None): return rs(11)
                    self.varTable[token[2].v] = bcldata.Shelf(token[3].v, self.throwfun)
                if token[2].ct("BOX"):
                    if self.varTable.get(token[2].v, None): return rs(11)
                    self.varTable[token[2].v] = bcldata.Box()
            elif token[1].cv("ACQUIRE"):
                if not ha(token, 2): return rs(7)
                if not token[2].isstr(): return rs(7)
                import importlib
                self.imports.append(importlib.import_module(token[2].v))
            elif token[1].cv("FLY"):
                if not ha(token, 3): return rs(7)
                if not token[2].comp(tk("IDENTIFIER", "TO")): return rs(7)
                token3 = self.getval(token[3], token[4] if ha(token, 4) else None)
                if token3 == None: return rs(7)
                if self.labelTable.get(token3, None) == None: return rs(8)
                self.index = self.labelTable[token3] - 1
                self.varTable[1001].bset(self.index)
            elif token[1].cv("FLAP"):
                if not ha(token, 3): return rs(7)
                if not token[2].comp(tk("IDENTIFIER", "TO")): return rs(7)
                token3 = self.getval(token[3], token[4] if ha(token, 4) else None)
                if token3 == None: return rs(7)
                if self.labelTable.get(token3, None) == None: 
                    found = False
                    for i in self.imports:
                        found, varTable = i.callsub(self.varTable, token3)
                        self.varTable = varTable
                        if found: return rs()
                    if not found:
                        return rs(8)
                self.flapStack.append(self.index)
                if len(self.flapStack) > 64: return rs(13)
                self.index = self.labelTable[token3] - 1
                self.varTable[1001].bset(self.index)
            elif token[1].cv("BACKFLIP"):
                if len(self.flapStack) < 1: return rs(13)
                self.index = self.flapStack.pop()
                self.varTable[1001].bset(self.index)
            elif token[1].cv("COME") or token[1].cv("END") or token[1].cv("BEGIN"):
                pass
            elif token[1].cv("WRITE"):
                if not ha(token, 3): return rs(7)
                token2 = self.getval(token[2], None)
                if token2 == None: return rs(7)
                token3 = self.getval(token[3], token[4] if ha(token, 4) else None)
                if token3 == None: return rs(7)
                if token2 == "<sout>":
                    print(token3, end='')
                else:
                    open(token2, "w").write(token3)
            elif token[1].cv("READ"):
                if not ha(token, 3): return rs(7)
                token2 = self.getval(token[2], None)
                if token2 == None: return rs(7)
                token3 = self.getval(token[3], token[4] if ha(token, 4) else None)
                if token3 == None: return rs(7)
                if token2 == "<sin>":
                    val = input()
                else:
                    val = open(token2, "r").read(token3)
                if token[3].ct("BOX"):
                    #try:
                    self.varTable[token[3].v].bset(int(val))
                    #except:
                    #    return rs(5)
                elif token[3].ct("SHELF"):
                    #try:
                    self.varTable[token[3].v] = bcldata.Shelf(len(val), self.throwfun)
                    self.varTable[token[3].v].items = [ord(i) for i in val]
                    #except:
                    #    return rs(7)
            elif token[1].cv("COPY"):
                if not ha(token, 4): return rs(7)
                if self.varTable.get(token[2].v, None) == None: return rs(12)
                if self.varTable.get(token[4].v, None) == None: return rs(12)
                if not token[3].ct("ASSIGN"): return rs(7)
                if not token[2].ct("SHELF") or token[2].ct("BOX"): return rs(7)
                if token[2].t != token[4].t: return rs(7)
                if token[2].ct("BOX"):
                    self.varTable[token[2].v].bset(token[4].v)
                elif token[2].ct("SHELF"):
                    for i in range(len(self.varTable[token[4].v].items)):
                        self.varTable[token[2].v][i] = 0
                        self.varTable[token[2].v][i] += self.varTable[token[4].v][i]
                    
            elif token[1].ct("SHELF"):
                if not ha(token, 4): return rs(7)
                if self.varTable.get(token[1].v, None) == None: return rs(12)
                if not token[3].comp(tk("ASSIGN")): 
                    if not token[2].comp(tk("ASSIGN")): return rs(7)
                    if not token[3].ct("SHELF"): return rs(7)
                    if self.varTable.get(token[3].v, None) == None: return rs(12)
                    self.varTable[token[1].v] = self.varTable[token[3].v]
                token4 = self.getval(token[4], token[5] if ha(token, 5) else None)
                if token4 == None: return rs(12)
                token2 = self.getval(token[2], None)
                if token2 == None: return rs(12)
                self.varTable[token[1].v][token2 - 1] = token4
            elif token[1].ct("BOX"):
                if not ha(token, 3): return rs(7)
                if token[1].v not in self.varTable.items: return rs(12)
                if not token[2].comp(tk("ASSIGN")): return rs(7)
                token3 = self.getval(token[3], token[4] if ha(token, 4) else None)
                if token3 == None: return rs(12)
                self.varTable[token[1].v].bset(token3)
            else:
                return rs(7)
        return rs()
