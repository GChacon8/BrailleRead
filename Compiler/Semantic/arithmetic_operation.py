from Semantic.utilities import *


class ArithmeticOperation(Instruction):
    def __init__(self, operation):
        self.operation = operation

    def eval(self, program, symbolTable):
        operation_value = self.operation.eval(program, symbolTable)

        if operation_value is not None:
            if self.operation.operator == '<>':
                operation_value = operation_value.replace('<>', '!=')
                return bool(eval(operation_value))
            elif self.operation.operator in ['>=', '<=', '==', '>', '<']:
                return bool(eval(operation_value))
            else:
                return int(eval(operation_value))


class MathOperation(Instruction):
    def __init__(self, left_operation, operator, right_operation):
        self.left_operation = left_operation
        self.operator = operator
        self.right_operation = right_operation

    def eval(self, program, symbolTable):
        left_operation_value, right_operation_value = None, None

        if verifyType(self.left_operation,
                      MathValueNegative) and self.operator is None and self.right_operation is None:
            return self.left_operation.eval(program, symbolTable)

        if self.left_operation == "(" and self.right_operation == ")":
            value = self.operator.eval(program, symbolTable)
            if value is not None:
                return "(" + str(value) + ")"

        if verifyType(self.left_operation, MathOperation) or verifyType(self.left_operation, MathValue):
            left_operation_value = self.left_operation.eval(program, symbolTable)

        if verifyType(self.right_operation, MathOperation) or verifyType(self.right_operation, MathValue):
            right_operation_value = self.right_operation.eval(program, symbolTable)

        if left_operation_value is not None and right_operation_value is not None:
            return left_operation_value + self.operator + right_operation_value


class MathValue:
    def __init__(self, mathValue):
        self.mathValue = mathValue

    def eval(self, program, symbolTable):
        if verifyType(self.mathValue, int):
            return str(self.mathValue)

        elif verifyType(self.mathValue, str):
            symbol = searchSymbolByID(self.mathValue, program, symbolTable)
            if symbol is not None:
                if verifyType(symbol.value, int):
                    return str(symbol.value)
                else:
                    program.semanticError.invalidArithmeticOperationValue()

        elif verifyType(self.mathValue, MathOperation) or verifyType(self.mathValue, MathValueNegative):
            return self.mathValue.eval(program, symbolTable)


class MathValueNegative:
    def __init__(self, mathValue):
        self.mathValue = mathValue

    def eval(self, program, symbolTable):
        if verifyType(self.mathValue, int):
            return "-" + str(self.mathValue)

        elif verifyType(self.mathValue, str):
            symbol = searchSymbolByID(self.mathValue, program, symbolTable)
            if symbol is not None:
                if verifyType(symbol.value, int):
                    return "-" + str(symbol.value)
                else:
                    program.semanticError.invalidArithmeticOperationValue()

        elif verifyType(self.mathValue, MathOperation) or verifyType(self.mathValue, MathValueNegative):
            value = self.mathValue.eval(program, symbolTable)
            if value is not None:
                return "-" + str(value)
