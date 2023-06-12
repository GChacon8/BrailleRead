import sys
sys.path.append("..")


class Instruction:
    def eval(self, program, symbolTable):
        pass


def verifyType(value1, instance):
    return type(value1) == instance


def validateType(token_ID, value, type, program):
    line = token_ID.lineno
    ID = token_ID.value
    if verifyType(value, int) and type != "Num":
        program.semanticError.incompatibleType(line, ID)

    if verifyType(value, bool) and type != "Bool":
        program.semanticError.incompatibleType(line, ID)

    if verifyType(value, str) and type != "String":
        program.semanticError.incompatibleType(line, ID)


def checkValue(value, typeValue, program, symbolTable, error):
    if verifyType(value, typeValue):
        return value

    elif verifyType(value, str):
        symbol = searchSymbolByID(value, program, symbolTable)
        if symbol is not None:
            if verifyType(symbol.value, typeValue):
                return symbol.value
            else:
                error()
    else:
        error()


def searchSymbolByID0(token_ID, program, symbolTable):
    line = token_ID.lineno
    ID = token_ID.value
    if symbolTable.exist(ID):
        return symbolTable.getSymbolByID(ID)
    elif program.symbolTable.exist(ID):
        return program.symbolTable.getSymbolByID(ID)
    else:
        program.semanticError.variableNotDefined0(line, ID)
        return None


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


def assignment(token_ID, value, program, symbolTable, scope):
    line = token_ID.lineno
    ID = token_ID.value
    if value is not None:
        if not symbolTable.exist(ID):
            symbolTable.addSymbol(ID, value, type(value), scope)
        else:
            program.semanticError.variableAlreadyDefined(line, ID)


def update(token_ID, value, program, symbolTable):
    line = token_ID.lineno
    ID = token_ID.value
    if value is not None:
        if not symbolTable.exist(ID):
            program.semanticError.variableNotDefined(line, ID)
        else:
            old_value = symbolTable.getSymbolByID(ID)
            if verifyType(old_value.value, type(value)):
                symbolTable.changeSymbolValue(ID, value)
            else:
                program.semanticError.invalidSymbolType(line, ID)


def update2(line, ID, value, program, symbolTable):
    if value is not None:
        if not symbolTable.exist(ID):
            program.semanticError.variableNotDefined(line, ID)
        else:
            old_value = symbolTable.getSymbolByID(ID)
            if verifyType(old_value.value, type(value)):
                symbolTable.changeSymbolValue(ID, value)
            else:
                program.semanticError.invalidSymbolType(line, ID)


def addEngine(ID, value, symbolTable, scope):
    symbolTable.addSymbol(ID, value, type(value), scope)
