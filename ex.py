import sys

debug = True if len(sys.argv) > 2 and sys.argv[2] == "dbg" else False

errdesc = {
    0: "Interpreter succeed, but somewhy still died",
    1: "Void executed, galaxy collapsed, interpreter died",
    2: "Nothing executed, nothing happened",
    3: "Programmer used unkown runic symbols",
    4: "Programmer cannot describe what he wants correctly",
    5: "Number is actually not a number",
    6: "Strings are disguisting and not valid here",
    7: "Do not forget to add some syntax error message here",
    8: "label where",
    9: "Shelf size was too big for this world",
    10: "Programmer tried to reach shelf section from parallel dimension",
    12: "Programmer tried to reach item from parallel dimension",
    11: "Materialization of already materialized object caused nuclear explosion and program died",
    13: "Program flapped right into abyss"
}

rep = {
    "n": "\n",
    "\\": "\\",
    "t": "\t",
    "0": "\0"
}

def throw(id, fatal=True, details=None):
    if id == 0: return
    id = str(id)
    if len(str(id)) < 6: id = (6 - len(id)) * "0" + id
    s = "E" if fatal else "W"
    sys.stderr.write("BCL" + s + id + " " + errdesc.get(int(id), "Unknown error message") + "\n")
    if details: sys.stderr.write(11*" " + details)
    sys.stderr.write("Rewrite your code and try again.\n")
    if fatal: sys.exit(int(id))


class PToken:
    def __init__(self, t, v=None):
        self.t = t
        self.v = v
    
    def __repr__(self):
        if self.v: return f"({self.t}: {self.v})"
        return f"({self.t})"
    
    def isv(self):
        if self.v: return True
        return False
    
    def isID(self):
        return self.t == "IDENTIFIER"
    
    def isnum(self):
        return self.t == "NUMBER"
        
    def isstr(self):
        return self.t == "STRING"
        
    def islabel(self):
        return self.t == "LABEL"
    
    def comp(self, other):
        if isinstance(other, PToken):
            return self.t == other.t and self.v == other.v
    
    def ct(self, other):
        return self.t == other
    
    def cv(self, other):
        return self.v == other

class PState:
    def __init__(self, id, line):
        self.id = id
        self.line = line
    
    def ise(self):
        return self.id != 0

class PResult:
    def __init__(self, state, tokens):
        self.tokens = tokens
        self.state = state

class IResult:
    def __init__(self, error=None):
        self.error = error

def hasarg(list, arg):
    return len(list) > arg