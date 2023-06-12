class SemanticError:
    def __init__(self):
        self.errors = []

    def printErrors(self):
        for i in range(len(self.errors)):
            print(self.errors[i])

    def getErrors(self):
        return self.errors

    def addError(self, error):
        self.errors.append(error)

    def incorrectCommentLine(self):
        self.errors.append(f"Error: The initial comment is not on the first line of the program")

    def masterNotFound(self):
        self.errors.append(f"Semantic error: Master not found")

    def masterMultipleDefinition(self):
        self.errors.append(f"Semantic error: Master multiple definition")

    def invalidArithmeticOperationValue(self):
        self.errors.append(f"Semantic error: Invalid value in arithmetic operation, value is not a int")

    def invalidSymbolType(self, line, ID):
        self.errors.append(f"Semantic error at line {line}: Incompatible type in symbol '{ID}'")

    def procedureNotFound(self, ID):
        self.errors.append(f"Semantic error: Procedure '{ID}' not found")

    def variableAlreadyDefined(self, line, ID):
        self.errors.append(f"Semantic error at line {line}: Variable '{ID}' already defined")

    def variableNotDefined0(self, line, ID):
        self.errors.append(f"Semantic error at line {line}: Variable '{ID}' not defined")

    def variableNotDefined(self, ID):
        self.errors.append(f"Semantic error: Variable '{ID}' not defined")

    def variableNotNumerical(self, line, ID):
        self.errors.append(f"Semantic error at line {line}: Variable '{ID}' must be numerical")

    def valueNotNumerical(self, line, value):
        self.errors.append(f"Semantic error at line {line}: Value {value} is not numerical")

    def variableNotBoolean(self, line, ID):
        self.errors.append(f"Semantic error at line {line}: Variable '{ID}' must be boolean")

    def procedureAlreadyDefined(self, ID):
        self.errors.append(f"Semantic error: Procedure '{ID}' already defined")

    def incompatibleType(self, line, ID):
        self.errors.append(f"Semantic error at line {line}: Incompatible type or value in variable '{ID}'")

    def badPosition(self, line, position):
        self.errors.append(f"Semantic error at line {line}: The position must be defined between 1 and 6. You set {position}")

    def badState(self, line, state):
        self.errors.append(f"Semantic error at line {line}: State can just be 0 or 1. You set {state}")

    def notBreak(self):
        self.errors.append(f"Semantic error: Repeat does not contain break")
