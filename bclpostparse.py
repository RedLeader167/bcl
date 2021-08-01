import ex
import string

tk = ex.PToken
st = ex.PState
rs = ex.PResult


class PostParser:
    def __init__(self, tokens):
        self.reinit(tokens)
        self.advance()
        
    def reinit(self, tokens):
        self.tokens = tokens
        self.token = None
        self.index = -1
    
    def advance(self):
        self.index += 1
        self.token = self.tokens[self.index] if self.index < len(self.tokens) else None
    
    def parse(self):
        tokens = [[]]
        pretokens = []
        state = st(0,0)
        l = 0
        
        while self.token != None:
            if self.token.t in ("IDENTIFIER", "NUMBER", "STRING", "SHELF", "BOX", "SHELFID", "ASSIGN"):
                if self.token.t == "IDENTIFIER" and self.token.v == "COME":
                    tokens[len(tokens) - 1].append(self.token)
                    self.advance()
                    if self.token.t != "IDENTIFIER" and self.token.v != "FROM":
                        state.id = 7
                        state.line = l
                        break
                    tokens[len(tokens) - 1].append(self.token)
                    self.advance()
                    if self.token.t != "NUMBER":
                        state.id = 7
                        state.line = l
                        break
                    pretokens.append(tk("COMEFROM", [int(self.token.v), l]))
                else:
                    tokens[len(tokens) - 1].append(self.token)
                    self.advance()
            elif self.token.t == "EOL":
                tokens.append([])
                l += 1
                self.advance()
            elif self.token.t == "LABEL":
                pretokens.append(self.token)
                #l -= 1
                self.advance()
            elif self.token.t == "EOF":
                break
            else:
                state.id = 7
                state.line = l
                break
        
        tokens.append([tk("EOF")])
        return rs(state, [pretokens, tokens])
