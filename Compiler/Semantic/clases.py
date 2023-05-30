from Semantic.arithmetic_operation import *
from Semantic.symbol_table import *


class value(Instruction):
    def __init__(self, value):
        self.value = value
        self.temp = self.value

    def eval(self, func, ID, type, program, symbolTable, scope):
        self.value = self.getResult(program, symbolTable)
        validateType(ID, self.value, type, program)

        if func == "New":
            if (verifyType(self.value, int) and type == "Num") or (verifyType(self.value, bool) and type == "Bool") or (verifyType(self.value, str) and type == "String"):
                assignment(ID, self.value, program, symbolTable, scope)

        elif func == "Values":
            if (verifyType(self.value, int) and type == "Num") or (verifyType(self.value, bool) and type == "Bool") or (verifyType(self.value, str) and type == "String"):
                update(ID, self.value, program, symbolTable)

    def getResult(self, program, symbolTable):
        self.temp = copy.deepcopy(self.value)
        symbol = None
        if verifyType(self.value, str) and self.value.startswith('@'):
            symbol = searchSymbolByID(self.value, program, symbolTable)
            if symbol is not None:
                self.value = symbol.value
            else:
                return

        if verifyType(self.value, ArithmeticOperation):
            self.value = self.value.eval(program, symbolTable)

        if verifyType(self.value, MathValueNegative):
            self.value = self.value.eval(program, symbolTable)

        result = self.value
        self.value = self.temp
        return result


class Break(Instruction):
    def __init__(self, func):
        self.func = func

    def eval(self, program, symbolTable):
        pass

class VariableDeclaration(Instruction):
    def __init__(self, func, ID, type_value):
        self.func = func
        self.ID = ID
        self.type = type_value[0]
        self.value = type_value[1]
        self.scope = "local"

    def eval(self, program, symbolTable):
        if self.scope == "global":
            self.value.eval(self.func, self.ID, self.type, program, program.symbolTable, "global")
        else:
            self.value.eval(self.func, self.ID, self.type, program, symbolTable, "local")


class VariableUpdate(Instruction):
    def __init__(self, func, ID, value):
        self.func = func
        self.ID = ID
        self.value = value
        self.scope = "local"

    def eval(self, program, symbolTable):
        symbol = searchSymbolByID(self.ID, program, symbolTable)
        if symbol:
            type = getType(symbol.value)
            if self.scope == "global":
                self.value.eval(self.func, self.ID, type, program, program.symbolTable, "global")
            else:
                self.value.eval(self.func, self.ID, type, program, symbolTable, "local")


class AlterVariable(Instruction):
    def __init__(self, func, ID, operator, value):
        self.func = func
        self.ID = ID
        self.operator = operator
        self.value = value
        self.scope = "local"
        self.result = None

    def validate(self, program, symbolTable):
        symbol = searchSymbolByID(self.ID, program, symbolTable)
        if symbol:
            if getType(symbol.value) == "Num":
                self.result = symbol.value
                if self.operator == "+":
                    self.result += self.value.value
                elif self.operator == "-":
                    self.result -= self.value.value
                elif self.operator == "*":
                    self.result *= self.value.value
                else:
                    self.result /= self.value.value
                return True
            else:
                program.semanticError.variableNotNumerical(self.ID)
        return False

    def eval(self, program, symbolTable):
        if self.validate(program, symbolTable):
            update(self.ID, self.result, program, symbolTable)

    def getResult(self, program, symbolTable):
        if self.validate(program, symbolTable):
            return self.result


class VariableWithAlter(Instruction):
    def __init__(self, func, ID, alter_variable):
        self.func = func
        self.ID = ID
        self.alter_variable = alter_variable
        self.scope = "local"

    def eval(self, program, symbolTable):
        symbol = searchSymbolByID(self.ID, program, symbolTable)
        if symbol:
            result = self.alter_variable.getResult(program, symbolTable)
            if result is not None:
                update(self.ID, result, program, symbolTable)


class AlterBVariable(Instruction):
    def __init__(self, func, ID):
        self.func = func
        self.ID = ID
        self.scope = "local"

    def eval(self, program, symbolTable):
        symbol = searchSymbolByID(self.ID, program, symbolTable)
        if symbol:
            if getType(symbol.value) == "Bool":
                update(self.ID, not symbol.value, program, symbolTable)
            else:
                program.semanticError.variableNotBoolean(self.ID)


class SignalFunction(Instruction):
    def __init__(self, func, position, state):
        self.func = func
        self.position = position
        self.state = state
        self.scope = "local"

    def eval(self, program, symbolTable):
        position = self.position.value.getResult(program, symbolTable)
        state = self.state.value.getResult(program, symbolTable)

        if getType(position) != "Num":
            program.semanticError.valueNotNumerical(position)
            return

        if getType(state) != "Num":
            program.semanticError.valueNotNumerical(state)
            return

        if (position is True or position is False) or (state is True or state is False):
            return

        if position in [1, 2, 3, 4, 5, 6]:
            if state in [0, 1]:
                update(str(position), state, program, symbolTable)
                self.signal(str(position), str(state), program)
            else:
                program.semanticError.badState(state)
        else:
            program.semanticError.badPosition(position)


    def signal(self, position, state, program):
        output = "Signal;" + "s" + position + state
        program.programOutput.append(output)


class EndSignalFunction(Instruction):
    def __init__(self, func):
        self.func = func
        self.scope = "local"

    def eval(self, program, symbolTable):
        self.end_signal(program)


    def end_signal(self, program):
        output = "EndSignal;" + "z"
        program.programOutput.append(output)


class ViewSignalFunction(Instruction):
    def __init__(self, func, position):
        self.func = func
        self.position = position
        self.scope = "local"
        self.result = None

    def eval(self, program, symbolTable):
        position = self.position.value.getResult(program, symbolTable)

        if getType(position) != "Num" or (position is True or position is False):
            program.semanticError.valueNotNumerical(position)
            return

        if position in [1, 2, 3, 4, 5, 6]:
            symbol = searchSymbolByID(str(position), program, symbolTable)
            self.result = symbol.value
        else:
            program.semanticError.badPosition(position)

    def getResult(self, program, symbolTable):
        self.eval(program, symbolTable)
        return self.result


class IsTrueFunction(Instruction):
    def __init__(self, func, ID):
        self.func = func
        self.ID = ID
        self.scope = "local"
        self.result = None

    def eval(self, program, symbolTable):
        symbol = searchSymbolByID(self.ID, program, symbolTable)
        if symbol:
            if getType(symbol.value) == "Bool":
                self.result = symbol.value
            else:
                program.semanticError.variableNotBoolean(self.ID)

    def getResult(self, program, symbolTable):
        self.eval(program, symbolTable)
        return self.result


class CaseStatement(Instruction):
    def __init__(self, func, ID, case_options, else_option):
        self.func = func
        self.ID = ID
        self.expressions = None
        self.local_variables = []
        self.case_options = case_options
        self.else_option = else_option
        self.scope = "local"

    def eval(self, program, symbolTable):
        symbol = searchSymbolByID(self.ID, program, symbolTable)
        for i in range(len(self.case_options)):
            if self.case_options[i][0].value == symbol.value:
                self.expressions = self.case_options[i][1]
                break

        if self.expressions is None:
            self.expressions = self.else_option

        for expression in self.expressions:
            if expression:
                if verifyType(expression, VariableDeclaration):
                    expression.scope = "local"
                expression.eval(program, symbolTable)

                if expression.func == "New":
                    if symbolTable.getSymbolByID(expression.ID):
                        self.local_variables.append(expression.ID)

        for variable in self.local_variables:
            symbolTable.removeSymbolByID(variable)


class WhileStatement(Instruction):
    def __init__(self, func, condition, expressions):
        self.func = func
        self.condition = condition
        self.expressions = expressions
        self.local_variables = []
        self.scope = "local"

    def eval(self, program, symbolTable):
        result = self.condition.getResult(program, symbolTable)
        while result:
            for expression in self.expressions:
                if expression:
                    if verifyType(expression, VariableDeclaration):
                        expression.scope = "local"
                    expression.eval(program, symbolTable)

                    if expression.func == "New":
                        if symbolTable.getSymbolByID(expression.ID):
                            self.local_variables.append(expression.ID)

            for variable in self.local_variables:
                symbolTable.removeSymbolByID(variable)

            result = self.condition.getResult(program, symbolTable)


class UntilStatement(Instruction):
    def __init__(self, func, expressions, condition):
        self.func = func
        self.expressions = expressions
        self.condition = condition
        self.local_variables = []
        self.scope = "local"

    def eval(self, program, symbolTable):
        result = True
        while result:
            for expression in self.expressions:
                if expression:
                    if verifyType(expression, VariableDeclaration):
                        expression.scope = "local"
                    expression.eval(program, symbolTable)

                    if expression.func == "New":
                        if symbolTable.getSymbolByID(expression.ID):
                            self.local_variables.append(expression.ID)

            for variable in self.local_variables:
                symbolTable.removeSymbolByID(variable)

            result = not(self.condition.getResult(program, symbolTable))


class RepeatStatement(Instruction):
    def __init__(self, func, expressions):
        self.func = func
        self.expressions = expressions
        self.local_variables = []
        self.scope = "local"

    def eval(self, program, symbolTable):
        has_break = None
        for expression in self.expressions:
            if verifyType(expression, Break):
                has_break = True
                break

        if has_break is None:
            program.semanticError.notBreak()
            return

        result = True
        while result:
            for expression in self.expressions:
                if expression:
                    if verifyType(expression, VariableDeclaration):
                        expression.scope = "local"
                    expression.eval(program, symbolTable)

                    if expression.func == "New":
                        if symbolTable.getSymbolByID(expression.ID):
                            self.local_variables.append(expression.ID)

                    if verifyType(expression, Break):
                        result = False
                        break

            for variable in self.local_variables:
                symbolTable.removeSymbolByID(variable)


class ProcedureCall(Instruction):
    def __init__(self, func, ID):
        self.func = func
        self.ID = ID
        self.local_variables = []
        self.scope = "local"

    def eval(self, program, symbolTable):
        symbol_procedure = program.symbolTable.getProcedureByID(self.ID)

        if symbol_procedure:
            procedure = symbol_procedure.getProcedures()[0]
            if procedure:
                for expression in procedure.getExpressions():
                    if expression:
                        if verifyType(expression, VariableDeclaration):
                            expression.scope = "local"
                        expression.eval(program, symbolTable)

                        if expression.func == "New":
                            if symbolTable.getSymbolByID(expression.ID):
                                self.local_variables.append(expression.ID)

                for variable in self.local_variables:
                    symbolTable.removeSymbolByID(variable)
        else:
            program.semanticError.procedureNotFound(self.ID)


class PrintValues(Instruction):
    def __init__(self, func, print_value_list):
        self.func = func
        self.print_value_list = print_value_list
        self.scope = "local"
        self.result = ""

    def eval(self, program, symbolTable):
        for expression in self.print_value_list:
            if verifyType(expression, value):
                prev_result = expression.getResult(program, symbolTable)
                if prev_result is None:
                    return
                if isinstance(prev_result, str):
                    self.result += prev_result
                else:
                    self.result += str(prev_result)

            elif verifyType(expression, IsTrueFunction) or verifyType(expression, ViewSignalFunction):
                prev_result = expression.getResult(program, symbolTable)
                if prev_result is None:
                    return
                else:
                    self.result += str(prev_result)

        program.getPrints().append(self.result)
        self.result = ""


class Write(Instruction):
    def __init__(self, func, print_value_list):
        self.func = func
        self.print_value_list = print_value_list
        self.scope = "local"
        self.result = ""

    def eval(self, program, symbolTable):
        for expression in self.print_value_list:
            if verifyType(expression, value):
                prev_result = expression.getResult(program, symbolTable)
                if prev_result is None:
                    return
                if isinstance(prev_result, str):
                    self.result += prev_result
                else:
                    self.result += str(prev_result)

            elif verifyType(expression, IsTrueFunction) or verifyType(expression, ViewSignalFunction):
                prev_result = expression.getResult(program, symbolTable)
                if prev_result is None:
                    return
                else:
                    self.result += str(prev_result)

        program.programOutput.append("Write;w" + self.result)
        self.result = ""