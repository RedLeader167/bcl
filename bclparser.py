import ex
import string

alph = string.ascii_uppercase + string.ascii_lowercase
tk = ex.PToken
st = ex.PState
rs = ex.PResult


class Parser:
    def __init__(self, code):
        self.reinit(code)
        self.advance()
        
    def reinit(self, code):
        self.code = code
        self.char = None
        self.index = -1
    
    def advance(self):
        self.index += 1
        self.char = self.code[self.index] if self.index < len(self.code) else None
    
    def parse(self):
        tokens = []
        state = st(0,0)
        l = 0
        
        while self.char != None:
            if self.char == "\n":
                tokens.append(tk("EOL"))
                l += 1
                self.advance()
            elif self.char == ":":
                tokens.append(tk("ASSIGN"))
                self.advance()
            elif self.char in alph:
                fstr = ""
                while self.char != None and self.char in alph + "0123456789":
                    fstr += self.char
                    self.advance()
                tokens.append(tk("IDENTIFIER", fstr))
                if fstr.startswith("NOT"):
                    while self.char != None and self.char != "\n":
                        self.advance()
                    
            elif self.char == '"':
                fstr = ""
                self.advance()
                while self.char != None and self.char != '"':
                    if self.char == "\\":
                        self.advance()
                        fstr += ex.rep.get(self.char, self.char)
                    else:
                        fstr += self.char
                    self.advance()
                self.advance()
                tokens.append(tk("STRING", fstr))
            elif self.char in "-0123456789$%^":
                typeo = "NUMBER"
                if self.char in "$%^":
                    typeo = "SHELF" if self.char == "$" else "1"
                    if typeo == "1":
                        typeo = "BOX" if self.char == "%" else "SHELFID"
                    self.advance()
                fstr = ""
                while self.char != None and self.char in "-0123456789":
                    fstr += self.char
                    self.advance()
                try:
                    fstr = int(fstr)
                except:
                    state.id = 5
                    state.line = l
                    break
                tokens.append(tk(typeo, fstr))
            elif self.char == "(":
                fstr = ""
                self.advance()
                while self.char != None and self.char != ")":
                    if self.char not in " \t": fstr += self.char
                    self.advance()
                self.advance()
                try:
                    fstr = int(fstr)
                except:
                    state.id = 6
                    state.line = l
                    break
                tokens.append(tk("LABEL", [fstr, l]))
            elif self.char in " \t":
                self.advance()
            else:
                state.id = 3
                state.line = l
                break
        
        tokens.append(tk("EOF"))
        return rs(state, tokens)
