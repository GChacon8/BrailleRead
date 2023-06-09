from Semantic.arithmetic_operation import *
from Semantic.symbol_table import *


class value(Instruction):
    def __init__(self, value):
        self.value = value
        self.temp = self.value

    def eval(self, func, token_ID, type, program, symbolTable, scope):
        self.value = self.getResult(program, symbolTable)
        validateType(token_ID, self.value, type, program)

        if func == "New":
            if (verifyType(self.value, int) and type == "Num") or (verifyType(self.value, bool) and type == "Bool") or (verifyType(self.value, str) and type == "String"):
                assignment(token_ID, self.value, program, symbolTable, scope)

        elif func == "Values":
            if (verifyType(self.value, int) and type == "Num") or (verifyType(self.value, bool) and type == "Bool") or (verifyType(self.value, str) and type == "String"):
                update(token_ID, self.value, program, symbolTable)

    def getResult(self, program, symbolTable):
        self.temp = copy.deepcopy(self.value)
        if verifyType(self.value, str) and self.value.startswith('@'):
            symbol = searchSymbolByID(self.value, program, symbolTable)
            if symbol is not None:
                self.value = symbol.value
            else:
                return

        if verifyType(self.value, ArithmeticOperation) or verifyType(self.value, MathValueNegative):
            self.value = self.value.eval(program, symbolTable)

        if verifyType(self.value, IsTrueFunction) or verifyType(self.value, AlterVariable) or verifyType(self.value, ViewSignalFunction):
            self.value = self.value.getResult(program, symbolTable)

        result = self.value
        self.value = self.temp
        return result


class Break(Instruction):
    def __init__(self, func):
        self.func = func

    def eval(self, program, symbolTable):
        pass


class VariableDeclaration(Instruction):
    def __init__(self, func, token_ID, type_value):
        self.func = func
        self.token_ID = token_ID
        self.ID = token_ID.value
        self.type = type_value[0]
        self.value = type_value[1]
        self.scope = "local"

    def eval(self, program, symbolTable):
        if self.scope == "global":
            self.value.eval(self.func, self.token_ID, self.type, program, program.symbolTable, "global")
        else:
            self.value.eval(self.func, self.token_ID, self.type, program, symbolTable, "local")


class VariableUpdate(Instruction):
    def __init__(self, func, token_ID, value):
        self.func = func
        self.token_ID = token_ID
        self.ID = token_ID.value
        self.value = value
        self.scope = "local"

    def eval(self, program, symbolTable):
        symbol = searchSymbolByID0(self.token_ID, program, symbolTable)
        if symbol:
            type = getType(symbol.value)
            if self.scope == "global":
                self.value.eval(self.func, self.token_ID, type, program, program.symbolTable, "global")
            else:
                self.value.eval(self.func, self.token_ID, type, program, symbolTable, "local")


class AlterVariable(Instruction):
    def __init__(self, func, token_ID, operator, value):
        self.func = func
        self.token_ID = token_ID
        self.ID = token_ID.value
        self.operator = operator
        self.value = value
        self.scope = "local"
        self.result = None

    def validate(self, program, symbolTable):
        symbol = searchSymbolByID0(self.token_ID, program, symbolTable)
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
                line = self.token_ID.lineno
                program.semanticError.variableNotNumerical(line, self.ID)
        return False

    def eval(self, program, symbolTable):
        if self.validate(program, symbolTable):
            update(self.token_ID, self.result, program, symbolTable)

    def getResult(self, program, symbolTable):
        if self.validate(program, symbolTable):
            return self.result


class VariableWithAlter(Instruction):
    def __init__(self, func, token_ID, alter_variable):
        self.func = func
        self.token_ID = token_ID
        self.ID = token_ID.value
        self.alter_variable = alter_variable
        self.scope = "local"

    def eval(self, program, symbolTable):
        symbol = searchSymbolByID0(self.token_ID, program, symbolTable)
        if symbol:
            result = self.alter_variable.getResult(program, symbolTable)
            if result is not None:
                update(self.token_ID, result, program, symbolTable)


class AlterBVariable(Instruction):
    def __init__(self, func, token_ID):
        self.func = func
        self.token_ID = token_ID
        self.ID = token_ID.value
        self.scope = "local"

    def eval(self, program, symbolTable):
        symbol = searchSymbolByID0(self.token_ID, program, symbolTable)
        if symbol:
            if getType(symbol.value) == "Bool":
                update(self.token_ID, not symbol.value, program, symbolTable)
            else:
                line = self.token_ID.lineno
                program.semanticError.variableNotBoolean(line, self.ID)


class SignalFunction(Instruction):
    def __init__(self, token_func, position, state):
        self.token_func = token_func
        self.func = token_func.value
        self.position = position
        self.state = state
        self.scope = "local"

    def eval(self, program, symbolTable):
        position = self.position.value.getResult(program, symbolTable)
        state = self.state.value.getResult(program, symbolTable)
        line = self.token_func.lineno

        if position is None or state is None:
            return

        if getType(position) != "Num":
            program.semanticError.valueNotNumerical(line, position)
            return

        if getType(state) != "Num":
            program.semanticError.valueNotNumerical(line, state)
            return

        if (position is True or position is False) or (state is True or state is False):
            return

        if position in [1, 2, 3, 4, 5, 6]:
            if state in [0, 1]:
                update2(-1, str(position), state, program, symbolTable)
                self.signal(str(position), str(state), program)
            else:
                program.semanticError.badState(line, state)
        else:
            program.semanticError.badPosition(line, position)


    def signal(self, position, state, program):
        output = "Signal;" + "s" + position + state
        program.programOutput.append(output)


class EndSignalFunction(Instruction):
    def __init__(self, func):
        self.func = func
        self.scope = "local"

    def eval(self, program, symbolTable):
        for i in range(6):
            update2(-1, str(i + 1), 0, program, symbolTable)
        self.end_signal(program)


    def end_signal(self, program):
        output = "EndSignal;" + "zzz"
        program.programOutput.append(output)


class ViewSignalFunction(Instruction):
    def __init__(self, token_func, position):
        self.token_func = token_func
        self.func = token_func.value
        self.position = position
        self.scope = "local"
        self.result = None

    def eval(self, program, symbolTable):
        position = self.position.value.getResult(program, symbolTable)
        line = self.token_func.lineno

        if position is None:
            return

        if getType(position) != "Num" or (position is True or position is False):
            program.semanticError.valueNotNumerical(line, position)
            return

        if position in [1, 2, 3, 4, 5, 6]:
            symbol = searchSymbolByID(str(position), program, symbolTable)
            self.result = symbol.value
        else:
            program.semanticError.badPosition(line, position)

    def getResult(self, program, symbolTable):
        self.eval(program, symbolTable)
        return self.result


class IsTrueFunction(Instruction):
    def __init__(self, func, token_ID):
        self.func = func
        self.token_ID = token_ID
        self.ID = token_ID.value
        self.scope = "local"
        self.result = None

    def eval(self, program, symbolTable):
        symbol = searchSymbolByID0(self.token_ID, program, symbolTable)
        if symbol:
            if getType(symbol.value) == "Bool":
                self.result = symbol.value
            else:
                line = self.token_ID.lineno
                program.semanticError.variableNotBoolean(line, self.ID)

    def getResult(self, program, symbolTable):
        self.eval(program, symbolTable)
        return self.result


class CaseStatement(Instruction):
    def __init__(self, func, token_ID, case_options, else_option):
        self.func = func
        self.token_ID = token_ID
        self.ID = token_ID.value
        self.expressions = None
        self.local_variables = []
        self.case_options = case_options
        self.else_option = else_option
        self.scope = "local"

    def eval(self, program, symbolTable):
        symbol = searchSymbolByID0(self.token_ID, program, symbolTable)
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

                    if program.semanticError.errors != []:
                        result = False
                        break

            for variable in self.local_variables:
                symbolTable.removeSymbolByID(variable)

            if result is False:
                result = False
            else:
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

                    if program.semanticError.errors != []:
                        result = False
                        break

            for variable in self.local_variables:
                symbolTable.removeSymbolByID(variable)

            if result is False:
                result = False
            else:
                result = not(self.condition.getResult(program, symbolTable))


class IfStatement(Instruction):
    def __init__(self, func, condition, expressions):
        self.func = func
        self.condition = condition
        self.expressions = expressions
        self.local_variables = []
        self.scope = "local"

    def eval(self, program, symbolTable):
        result = self.condition.getResult(program, symbolTable)
        if result:
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

            return result


class RepeatStatement(Instruction):
    def __init__(self, func, expressions):
        self.func = func
        self.expressions = expressions
        self.local_variables = []
        self.scope = "local"

    def eval(self, program, symbolTable):
        has_break = None
        for expression in self.expressions:
            if verifyType(expression, IfStatement):
                for exp in expression.expressions:
                    if verifyType(exp, Break):
                        has_break = True
                        break

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
                    if verifyType(expression, IfStatement):
                        result = expression.eval(program, symbolTable)
                        if result is None:
                            result = True
                        else:
                            result = False
                            break

                    if verifyType(expression, VariableDeclaration):
                        expression.scope = "local"
                    expression.eval(program, symbolTable)

                    if expression.func == "New":
                        if symbolTable.getSymbolByID(expression.ID):
                            self.local_variables.append(expression.ID)

                    if program.semanticError.errors != []:
                        result = False
                        break

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
