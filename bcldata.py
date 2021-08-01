import ex
import random

class Shelf:
    def __init__(self, height, throwfun, s=False):
        self.throwfun = throwfun
        self.height = height
        self.items = []
        if height > 99 and not s:
            self.throwfun(9)
        for i in range(height):
            self.items.append(0)
            
    def __getitem__(self, key):
        if key > -1 and key < self.height:
            return self.items[key]
        self.throwfun(10)
    
    def get(self, key, ifn=None):
        if key > -1 and key < self.height:
            return self.items[key]
        return ifn
    
    def __setitem__(self, key, value):
        if not isinstance(value, int): self.throwfun(5)
        if key > -1 and key < self.height:
            self.items[key] = value
            return self.items[key]
        self.throwfun(10)
    
    def _print(self):
        return "".join([chr(i) for i in self.items])

class VarTable:
    def __init__(self, throwfun):
        self.spec = [1000, 1100, 1101, 1002]
        self.items = {1001: Box()}
        for i in self.spec:
            self.items[i] = Box()
        self.throwfun = throwfun
    
    def sget(self, key):
        if key == 1000: return Box()
        if key == 1100: return Box().bset(self.items[1100].bget() + 1)
        if key == 1101: return Box().bset(self.items[1101].bget() - 1)
        if key == 1002: return Box().bset(random.choice([0,1]))
    
    def __getitem__(self, key):
        #if key in self.spec: return self.sget(key)
        if key in self.items:
            return self.items[key]
        self.throwfun(10)
    
    def get(self, key, ifn=None):
        if key in self.spec: return self.sget(key)
        return self.items.get(key, ifn)
    
    def __setitem__(self, key, value):
        self.items[key] = value
        return self.items[key]

class Box:
    def __init__(self):
        self.bvalue = 0
    
    def bget(self):
        return self.bvalue
    
    def bset(self, value):
        if not isinstance(value, int): self.throwfun(5)
        self.bvalue = value
        return self