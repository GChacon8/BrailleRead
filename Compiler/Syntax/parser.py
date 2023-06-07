from Lexical.lexer import *
from Semantic.semantic import *
import ply.yacc as yacc
import sys
sys.path.append("..")

data = ""

# List of errors
syntax_errors = []

# List of comments
systax_comments = []

# Rules of precedence
precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
    ('right', 'UMINUS')
)


def p_program(p):
    '''program : procedure_set'''
    p[0] = Program(systax_comments, p[1])


def p_procedure_set(p):
    '''procedure_set : comments procedure procedure_set'''
    global systax_comments
    systax_comments = systax_comments + p.slice[1].value
    p[0] = [p[2]] + p[3]


def p_comments(p):
    '''comments : empty
                | COMMENT comments'''
    if len(p) == 3:
        p[0] = [p.slice[1].lineno] + p[2]
    else:
        p[0] = []


def p_comments_2(p):
    '''comments : COMMENT'''
    p[0] = [p.slice[1].lineno]


def p_procedure_set_2(p):
    '''procedure_set : comments procedure'''
    global systax_comments
    systax_comments = systax_comments + p.slice[1].value
    p[0] = [p[2]]


def p_procedure(p):
    '''procedure : PROC ID LPAREN statements RPAREN SEMICOLON'''
    if p[2] == "@Master":
        p[0] = MasterProcedure(p[2], p[4])
    else:
        p[0] = Procedure(p[2], p[4])


def p_statemets(p):
    '''statements : statement
                  | statement statements'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]


def p_statement(p):
    '''statement : variable_declaration SEMICOLON
                 | variable_update SEMICOLON
                 | alter_variable SEMICOLON
                 | variable_with_alter SEMICOLON
                 | alter_b_variable SEMICOLON
                 | signal_function SEMICOLON
                 | end_signal_function SEMICOLON
                 | view_signal_function SEMICOLON
                 | is_true_function SEMICOLON
                 | case_statement SEMICOLON
                 | while_statement SEMICOLON
                 | until_statement SEMICOLON
                 | repeat_statement SEMICOLON
                 | procedure_call SEMICOLON
                 | print_statement SEMICOLON
                 | write_statement SEMICOLON
                 | break SEMICOLON
                 | comments
                 | empty'''
    if p.slice[1].type != "comments":
        p[0] = p[1]


def p_variable_declaration(p):
    '''variable_declaration : NEW ID COMMA type_value'''
    p[0] = VariableDeclaration(p[1], p[2], p[4])


def p_type_value(p):
    '''type_value : LPAREN type COMMA value RPAREN'''
    p[0] = [p[2], p[4]]


def p_type(p):
    '''type : NUM
            | BOOL
            | STRING'''
    p[0] = p[1]


def p_value(p):
    '''value : NUMBER
             | BOOLEAN
             | STRING
             | ID
             | arith_op'''
    p[0] = value(p[1])


def p_arithmetic(p):
    '''arith_op : math_operation'''
    p[0] = ArithmeticOperation(p[1])


def p_math_operator_1(p):
    '''math_operation : math_operation operator math_operation'''
    p[0] = MathOperation(p[1], p[2], p[3])


def p_math_operator_2(p):
    '''math_operation : math_operation operator math_value'''
    p[0] = MathOperation(p[1], p[2], p[3])


def p_math_operator_3(p):
    '''math_operation : math_value operator math_operation'''
    p[0] = MathOperation(p[1], p[2], p[3])


def p_math_operator_4(p):
    '''math_operation : math_value operator math_value'''
    p[0] = MathOperation(p[1], p[2], p[3])


def p_math_operation_5(p):
    '''math_operation_paren : LPAREN math_operation RPAREN'''
    p[0] = MathOperation(p[1], p[2], p[3])


def p_math_value(p):
    '''math_value : ID
                  | NUMBER
                  | math_value_negative
                  | math_operation_paren'''
    p[0] = MathValue(p[1])


def p_math_value_negative(p):
    '''math_value_negative : SUB ID %prec UMINUS
                           | SUB NUMBER %prec UMINUS '''
    p[0] = MathValueNegative(p[2])


def p_operator(p):
    '''operator : ADD
                | SUB
                | MUL
                | DIV
                | REL_OP'''
    if p[1] == "ADD":
        p[0] = "+"
    elif p[1] == "SUB":
        p[0] = "-"
    elif p[1] == "MUL":
        p[0] = "*"
    elif p[1] == "DIV":
        p[0] = "/"
    else:
        p[0] = p[1]


def p_variable_update(p):
    '''variable_update : VALUES LPAREN ID COMMA value RPAREN'''
    p[0] = VariableUpdate(p[1], p[3], p[5])


def p_alter_variable(p):
    '''alter_variable : ALTER LPAREN ID COMMA operator COMMA value RPAREN'''
    p[0] = AlterVariable(p[1], p[3], p[5], p[7])


def p_variable_with_alter(p):
    '''variable_with_alter : VALUES LPAREN ID COMMA alter_variable RPAREN'''
    p[0] = VariableWithAlter(p[1], p[3], p[5])


def p_alter_b_variable(p):
    '''alter_b_variable : ALTER_B LPAREN ID RPAREN'''
    p[0] = AlterBVariable(p[0], p[3])


def p_signal_function(p):
    '''signal_function : SIGNAL LPAREN position_state COMMA position_state RPAREN'''
    p[0] = SignalFunction(p[1], p[3], p[5])


def p_position_state(p):
    '''position_state : value'''
    p[0] = value(p[1])


def p_end_signal_function(p):
    '''end_signal_function : END_SIGNAL LPAREN RPAREN'''
    p[0] = EndSignalFunction(p[1])


def p_view_signal_function(p):
    '''view_signal_function : VIEW_SIGNAL LPAREN position_state RPAREN'''
    p[0] = ViewSignalFunction(p[1], p[3])


def p_is_true_function(p):
    '''is_true_function : IS_TRUE LPAREN ID RPAREN'''
    p[0] = IsTrueFunction(p[1], p[3])


def p_case_statement(p):
    '''case_statement : CASE ID case_options
                      | CASE ID case_options else_option'''
    if len(p) == 4:
        p[0] = CaseStatement(p[1], p[2], p[3], [])
    else:
        p[0] = CaseStatement(p[1], p[2], p[3], p[4])


def p_case_options(p):
    '''case_options : when_statement
                    | when_statement case_options'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]


def p_when_statement(p):
    '''when_statement : WHEN value THEN LPAREN statements RPAREN'''
    p[0] = [p[2], p[5]]


def p_else_option(p):
    '''else_option : ELSE LPAREN statements RPAREN'''
    p[0] = p[3]


def p_while_statement(p):
    '''while_statement : WHILE condition LPAREN statements RPAREN'''
    p[0] = WhileStatement(p[1], p[2], p[4])


def p_condition(p):
    '''condition : value
                 | is_true_function'''
    p[0] = p[1]


def p_until_statement(p):
    '''until_statement : UNTIL LPAREN statements RPAREN condition'''
    p[0] = UntilStatement(p[1], p[3], p[5])


def p_repeat_statement(p):
    '''repeat_statement : REPEAT LPAREN statements RPAREN'''
    p[0] = RepeatStatement(p[1], p[3])


def p_procedure_call(p):
    '''procedure_call : CALL LPAREN ID RPAREN'''
    p[0] = ProcedureCall(p[1], p[3])


def p_print_statement(p):
    '''print_statement : PRINT_VALUES LPAREN print_value_list RPAREN'''
    p[0] = PrintValues(p[1], p[3])


def p_print_value_list(p):
    '''print_value_list : print_value
                        | print_value COMMA print_value_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_print_value(p):
    '''print_value : value
                   | is_true_function
                   | view_signal_function'''
    p[0] = p[1]


def p_write_statement(p):
    '''write_statement : WRITE LPAREN print_value_list RPAREN'''
    p[0] = Write(p[1], p[3])


def p_break(p):
    '''break : BREAK'''
    p[0] = Break(p[1])


def p_empty(p):
    '''empty : '''
    pass


def p_error(p):
    if p:
        syntax_errors.append(f"Syntax error at line {p.lineno}, column {find_column(data, p)}: Unexpected token {p.value}")
    else:
        syntax_errors.append("Syntax error: Unexpected end of input")


def systax_analysis(source_code):
    global data
    data = source_code
    lexical_analysis()
    parser = yacc.yacc(start="program")
    result = parser.parse(source_code)
    return result
