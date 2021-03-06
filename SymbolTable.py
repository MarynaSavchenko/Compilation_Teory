#!/usr/bin/python

class Symbol:
    pass


class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.name = name
        self.type = type


class VectorType(Symbol):

    def __init__(self, size, type, dimension):
        self.size = size
        self.type = type
        self.dimension = dimension

    def __str__(self):
        return 'vector'


class SymbolTable(object):

    def __init__(self, parent, name):  # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.var_dict = {}

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.var_dict[name] = symbol

    def get(self, name):  # get variable symbol or fundef from <name> entry
        try:
            return self.var_dict[name]
        except KeyError:
            if self.parent is None:
                return None
            else:
                return self.getParentScope().get(name)

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        return SymbolTable(self, name) #parent = self

    def popScope(self):
        return self.parent
