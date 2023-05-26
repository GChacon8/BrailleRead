import sys
sys.path.append("..")


class Instruction:
    def eval(self, program, symbolTable):
        pass


def verifyType(value1, instance):
    return type(value1) == instance


def validateType(ID, value, type, program):
    if verifyType(value, int) and type != "Num":
        program.semanticError.incompatibleType(ID)

    if verifyType(value, bool) and type != "Bool":
        program.semanticError.incompatibleType(ID)

    if verifyType(value, str) and type != "String":
        program.semanticError.incompatibleType(ID)


def checkValue(value, typeValue, program, symbolTable, error):
    if verifyType(value, typeValue):
        return value

    elif verifyType(value, str):
        symbol = searchSymbolByID(value, program, symbolTable)
        if symbol != None:
            if verifyType(symbol.value, typeValue):
                return symbol.value
            else:
                error()
    else:
        error()


def searchSymbolByID(ID, program, symbolTable):
    if symbolTable.exist(ID):
        return symbolTable.getSymbolByID(ID)
    elif program.symbolTable.exist(ID):
        return program.symbolTable.getSymbolByID(ID)
    else:
        program.semanticError.variableNotDefined(ID)
        return None


def getType(value):
    if isinstance(value, int) and not isinstance(value, bool):
        return "Num"
    elif isinstance(value, bool):
        return "Bool"
    else:
        return "String"


def assignment(ID, value, program, symbolTable, scope):
    if value != None:
        if not symbolTable.exist(ID):
            symbolTable.addSymbol(ID, value, type(value), scope)
        else:
            program.semanticError.variableAlreadyDefined(ID)


def update(ID, value, program, symbolTable):
    if value != None:
        if not symbolTable.exist(ID):
            program.semanticError.variableNotDefined(ID)
        else:
            old_value = symbolTable.getSymbolByID(ID)
            if verifyType(old_value.value, type(value)):
                symbolTable.changeSymbolValue(ID, value)
            else:
                program.semanticError.invalidSymbolType(ID)


def addEngine(ID, value, symbolTable, scope):
    symbolTable.addSymbol(ID, value, type(value), scope)