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

    # Main errors
    def mainNotFound(self):
        self.errors.append(f"Semantic error: Main not found")

    def mainMultipleDefinition(self):
        self.errors.append(f"Semantic error: Main multiple definition")

    # if error
    def invalidComparatorBoolean(self):
        self.errors.append(f"Semantic error: Invalid comparator for booleans")

    # Arithmetic operation errors
    def invalidArithmeticOperationValue(self):
        self.errors.append(f"Semantic error: Invalid value in arithmetic operation, value is not a int")

    # Variables and procedures errors
    def symbolNotFound(self, ID):
        self.errors.append(f"Semantic error: Symbol '{ID}' not found")

    def invalidSymbolType(self, ID):
        self.errors.append(f"Semantic error: Incompatible type in symbol '{ID}'")

    def isNotAProcedure(self, ID):
        self.errors.append(f"Semantic error: '{ID}' is not a procedure")

    def procedureNotFound(self, ID):
        self.errors.append(f"Semantic error: Procedure '{ID}' not found")

    def variableAlreadyDefined(self, ID):
        self.errors.append(f"Semantic error: Variable '{ID}' already defined")

    def variableNotDefined(self, ID):
        self.errors.append(f"Semantic error: Variable '{ID}' not defined")

    def variableNotNumerical(self, ID):
        self.errors.append(f"Semantic error: Variable '{ID}' must be numerical")

    def valueNotNumerical(self, value):
        self.errors.append(f"Semantic error: Value {value} is not numerical")

    def variableNotBoolean(self, ID):
        self.errors.append(f"Semantic error: Variable '{ID}' must be boolean")

    def procedureAlreadyDefined(self, ID):
        self.errors.append(f"Semantic error: Procedure '{ID}' already defined")

    def incompatibleType(self, ID):
        self.errors.append(f"Semantic error: Incompatible type or value in variable '{ID}'")

    def badPosition(self, position):
        self.errors.append(f"Semantic error: The position must be defined between 1 and 6. You set {position}")

    def badState(self, state):
        self.errors.append(f"Semantic error: State can just be 0 or 1. You set {state}")