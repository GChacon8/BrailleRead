import copy
from Semantic.utilities import *


class SymbolVariable:
    def __init__(self, ID, value, symbol_type, scope):
        self.ID = ID
        self.value = value
        self.type = symbol_type
        self.scope = scope

    def getID(self):
        return self.ID

    def getValue(self):
        return self.value

    def getType(self):
        return self.type

    def getScope(self):
        return self.scope


class SymbolProcedure:
    def __init__(self, ID):
        self.procedures = []
        self.ID = ID

    def addProcedure(self, procedure):
        self.procedures.append(procedure)

    def getID(self):
        return self.ID

    def getProcedures(self):
        return self.procedures


class SymbolTable:
    def __init__(self):
        self.variableTable = {}
        self.procedureTable = {}

    def addSymbol(self, ID, value, symbol_type, scope):
        temp = copy.deepcopy(value)
        new_symbol = SymbolVariable(ID, temp, symbol_type, scope)
        self.variableTable[ID] = new_symbol

    def removeSymbolByID(self, ID):
        if ID in self.variableTable:
            del self.variableTable[ID]

    def getSymbolByID(self, ID):
        try:
            return self.variableTable[ID]
        except KeyError:
            return None

    def getProcedureByID(self, ID):
        try:
            return self.procedureTable[ID]
        except KeyError:
            return None

    def addProcedureSymbol(self, ID, procedure):
        if ID in self.procedureTable:
            self.procedureTable[ID].addProcedure(procedure)
        else:
            new_procedure = SymbolProcedure(ID)
            new_procedure.addProcedure(procedure)
            self.procedureTable[ID] = new_procedure

    def changeSymbolValue(self, ID, value):
        temp = self.variableTable[ID]
        temp.value = copy.deepcopy(value)

    def getVariableTable(self):
        return self.variableTable

    def getProcedureTable(self):
        return self.procedureTable

    def attachSymboltable(self, symboltable):
        symbols = symboltable.getVariableTable()

        for symbol in symbols:
            self.variableTable[symbol] = symboltable.getSymbolByID(symbol)

    def clean(self):
        self.variableTable = {}
        self.procedureTable = {}

    def exist(self, ID):
        return ID in self.variableTable

    def existProcedure(self, ID):
        return ID in self.procedureTable

    def print(self):
        print("ID \t\t\t\t\t Value \t\t\t\t  Type \t\t\t\t   Scope")
        for key in self.variableTable:
            var = self.variableTable[key]
            var_id = var.ID.ljust(20)
            var_value = str(var.value).ljust(20)
            var_type = getType(var.value).ljust(20)
            var_scope = var.scope.ljust(20)

            print(f"{var_id} {var_value} {var_type} {var_scope.capitalize()}")