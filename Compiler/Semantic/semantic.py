from Semantic.semantic_errors import *
from Semantic.clases import *
import sys
sys.path.append("..")


def semantic_analysis(program):
    program.execute()
    return program


# Defines the behavior of the main program, the Master is searched for and evaluated
class Program:
    def __init__(self, comment_list, expressions_set):
        self.comment_list = comment_list
        self.expressions_set = expressions_set
        self.master = None
        self.semanticError = SemanticError()
        self.programOutput = []
        self.symbolTable = SymbolTable()
        self.prints = []

    def getErrors(self):
        return self.semanticError.errors

    def getPrints(self):
        return self.prints

    def isEmpty(self):
        return self.expressions_set[0] is None

    def execute(self):
        for i in range(6):
            addEngine(str(i + 1), 0, self.symbolTable, "global")

        if 1 not in self.comment_list:
            self.semanticError.incorrectCommentLine()
            return

        master_count = 0
        if not self.isEmpty():
            for expression in self.expressions_set:
                if expression is not None:
                    if expression.ID == "@Master":
                        master_count += 1
                        self.master = expression
                        continue
                    expression.eval(self, self.symbolTable)

        if master_count == 0:
            self.semanticError.mainNotFound()
            return

        if master_count > 1:
            self.semanticError.mainMultipleDefinition()
            return

        else:
            self.master.eval(self, self.symbolTable)
            print("\n------------------------------- GLOBAL -------------------------------\n")
            self.symbolTable.print()


# Defines the behavior of the master, is in charge of validating the particularities of the master
# and executes the body of this
class MasterProcedure(Instruction):
    def __init__(self, ID, expressions):
        self.ID = ID
        self.expressions = expressions

    def eval(self, program, symbolTable):
        for expression in self.expressions:
            if expression:
                if verifyType(expression, VariableDeclaration):
                    expression.scope = "global"
                expression.eval(program, symbolTable)


# Defines the behavior of a procedure, evaluates the body of the procedure
class Procedure(Instruction):
    def __init__(self, ID, expressions):
        self.ID = ID
        self.expressions = expressions

    def getID(self):
        return self.ID

    def getExpressions(self):
        return self.expressions

    def eval(self, program, symbolTable):
        if program.symbolTable.existProcedure(self.ID):
            program.semanticError.procedureAlreadyDefined()
        else:
            program.symbolTable.addProcedureSymbol(self.ID, self)
