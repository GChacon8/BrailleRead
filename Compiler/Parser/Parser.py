import ply.yacc as yacc
import sys
sys.path.append("..")
from Lexer.Lexer import tokens
from Lexer.Lexer import find_column

# Rules of precedence
precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
)

def p_program(p):
    '''program : proc_declaration'''

def p_proc_declaration(p):
    '''proc_declaration : PROC ID block SEMICOLON'''

def p_block(p):
    '''block : LPAREN statements RPAREN'''

def p_statemets(p):
    '''statements : statement
                  | statements statement'''

def p_statement(p):
    '''statement : variable_declaration SEMICOLON
                 | variable_update SEMICOLON
                 | alter_variable SEMICOLON
                 | variable_with_alter SEMICOLON
                 | variable_with_alterb SEMICOLON
                 | signal_function SEMICOLON
                 | view_signal_function SEMICOLON
                 | is_true_function SEMICOLON
                 | procedure_call SEMICOLON
                 | print_statement SEMICOLON'''

def p_variable_declaration(p):
    '''variable_declaration : NEW ID COMMA type_value'''
    variable_name = p[2]
    type_value = p[4]
    type_token = p.parser.token

    if variable_name in env:
        raise BRSyntaxError(
            f"Syntax error at line {p.slice[2].lineno}, column {find_column(data, p.slice[2])}: Variable '{variable_name}' is already defined")

    if type_value[0] == 'Num' and (type_value[1] is True or type_value[1] is False or isinstance(type_value[1], str)):
        raise BRSyntaxError(
            f"Syntax error at line {type_token.lineno}, column {find_column(data, type_token)}: Expected integer literal for Num type")
    if type_value[0] == 'Bool' and not isinstance(type_value[1], bool):
        raise BRSyntaxError(
            f"Syntax error at line {type_token.lineno}, column {find_column(data, type_token)}: Expected boolean literal for Bool type")
    if type_value[0] == 'String' and not isinstance(type_value[1], str):
        raise BRSyntaxError(
            f"Syntax error at line {type_token.lineno}, column {find_column(data, type_token)}: Expected string literal for String type")
    p.parser.token = None

    env[variable_name] = [type_value[0], type_value[1]]

def p_type_value(p):
    '''type_value : LPAREN type COMMA expression RPAREN'''
    p[0] = (p[2], p[4])

def p_type(p):
    '''type : NUM
            | BOOL
            | STRING'''
    p[0] = p[1]

def p_expression(p):
    '''expression : value
                  | ID
                  | is_true_function
                  | view_signal_function
                  | expression ADD expression
                  | expression SUB expression
                  | expression MUL expression
                  | expression DIV expression'''
    if len(p) == 2 and p.slice[1].type != 'ID':
        p[0] = p[1]
    elif len(p) == 2 and p.slice[1].type == 'ID':
        if p[1] not in env:
            raise BRSyntaxError(
                f"Syntax error at line {p.slice[1].lineno}, column {find_column(data, p.slice[1])}: Variable '{p.slice[1].value}' is not defined")
        p[0] = env[p[1]][1]
        p.parser.token = p.slice[1]
    else:
        operator = p[2]
        if operator == 'ADD':
            p[0] = p[1] + p[3]
        elif operator == 'SUB':
            p[0] = p[1] - p[3]
        elif operator == 'MUL':
            p[0] = p[1] * p[3]
        elif operator == 'DIV':
            p[0] = p[1] / p[3]

def p_value(p):
    '''value : NUMBER
             | BOOLEAN
             | STRING
             | LPAREN expression RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
        p.parser.token = p.slice[1]
    else:
        p[0] = p[2]

def p_variable_update(p):
    '''variable_update : VALUES LPAREN ID COMMA expression RPAREN'''
    variable_name = p[3]
    new_value = p[5]
    type_token = p.parser.token

    if variable_name not in env:
        raise BRSyntaxError(
            f"Syntax error at line {p.slice[3].lineno}, column {find_column(data, p.slice[3])}: Variable '{variable_name}' is not defined")
    if env[variable_name][0] == 'Num' and (new_value is True or new_value is False or isinstance(new_value, str)):
        raise BRSyntaxError(
            f"Syntax error at line {type_token.lineno}, column {find_column(data, type_token)}: Value '{new_value}' must be numerical for variable '{variable_name}'")
    if env[variable_name][0] == 'Bool' and not isinstance(new_value, bool):
        raise BRSyntaxError(
            f"Syntax error at line {type_token.lineno}, column {find_column(data, type_token)}: Value '{new_value}' must be boolean for variable '{variable_name}'")
    if env[variable_name][0] == 'String' and not isinstance(new_value, str):
        raise BRSyntaxError(
            f"Syntax error at line {type_token.lineno}, column {find_column(data, type_token)}: Value '{new_value}' must be string for variable '{variable_name}'")
    type_token = None

    env[variable_name][1] = new_value

def p_alter_variable(p):
    '''alter_variable : ALTER LPAREN ID COMMA operator COMMA NUMBER RPAREN'''
    variable_name = p[3]
    operator = p.slice[5].value
    value = p[7]

    if variable_name not in env:
        raise BRSyntaxError(
            f"Syntax error at line {p.slice[3].lineno}, column {find_column(data, p.slice[3])}: Variable '{variable_name}' is not defined")
    if env[variable_name][0] != 'Num':
        raise BRSyntaxError(
            f"Syntax error at line {p.slice[3].lineno}, column {find_column(data, p.slice[3])}: Variable '{variable_name}' must be numerical")

    result = env[variable_name][1]
    if operator == 'ADD':
        result += value
    elif operator == 'SUB':
        result -= value
    elif operator == 'MUL':
        result *= value
    elif operator == 'DIV':
        result /= value

    p[0] = result

def p_operator(p):
    '''operator : ADD
                | SUB
                | MUL
                | DIV'''
    p[0] = p[1]

def p_variable_with_alter(p):
    '''variable_with_alter : VALUES LPAREN ID COMMA alter_variable RPAREN'''
    variable_name = p[3]
    result = p[5]

    if variable_name not in env:
        raise BRSyntaxError(
            f"Syntax error at line {p.slice[3].lineno}, column {find_column(data, p.slice[3])}: Variable '{variable_name}' is not defined")
    if env[variable_name][0] == 'Bool':
        raise BRSyntaxError(
            f"Syntax error at line {p.slice[3].lineno}, column {find_column(data, p.slice[3])}: Variable '{variable_name}' must be numerical")

    env[variable_name][1] = result

def p_variable_with_alterb(p):
    '''variable_with_alterb : ALTERB LPAREN ID RPAREN'''
    variable_name = p[3]

    if variable_name not in env:
        raise BRSyntaxError(
            f"Syntax error at line {p.slice[3].lineno}, column {find_column(data, p.slice[3])}: Variable '{variable_name}' is not defined")
    if env[variable_name][0] != 'Bool':
        raise BRSyntaxError(
            f"Syntax error at line {p.slice[3].lineno}, column {find_column(data, p.slice[3])}: Variable '{variable_name}' must be boolean")

    if env[variable_name][1]:
        env[variable_name][1] = False
    else:
        env[variable_name][1] = True

def p_signal_function(p):
    '''signal_function : SIGNAL LPAREN position_state COMMA position_state RPAREN'''
    position = p[3]
    state = p[5]

    if position < 1 or position > 6:
        print("The position must be defined between 1 and 6")
    elif state not in [0, 1]:
        print("State can just be 0 or 1")
    else:
        env[position] = state
        print((position, state))

def p_position_state(p):
    '''position_state : expression
                      | ID'''
    type_token = p.parser.token

    if p.slice[1].type == 'ID' and p[1] not in env:
        raise BRSyntaxError(
            f"Syntax error at line {p.slice[1].lineno}, column {find_column(data, p.slice[1])}: Variable '{p.slice[1].value}' is not defined")
    if p.slice[1].type == 'ID' and env[p[1]][0] != 'Num':
        raise BRSyntaxError(
            f"Syntax error at line {p.slice[1].lineno}, column {find_column(data, p.slice[1])}: Variable '{p.slice[1].value}' must be numerical")
    if p.slice[1].type == 'expression' and (p.slice[1].value is True or p.slice[1].value is False or isinstance(p.slice[1].value, str)):
        raise BRSyntaxError(
            f"Syntax error at line {type_token.lineno}, column {find_column(data, type_token)}: Value '{type_token.value}' must be numerical")
    type_token = None

    if p.slice[1].type == 'ID':
        p[0] = env[p[1]][1]
    else:
        p[0] = p.slice[1].value

def p_view_signal_function(p):
    '''view_signal_function : VIEWSIGNAL LPAREN position_state RPAREN'''
    position = p[3]

    if position < 1 or position > 6:
        print("The position must be defined between 1 and 6")
    else:
        p[0] = env[position]

def p_is_true_function(p):
    '''is_true_function : ISTRUE LPAREN ID RPAREN'''
    variable_name = p[3]

    if variable_name not in env:
        raise BRSyntaxError(
            f"Syntax error at line {p.slice[3].lineno}, column {find_column(data, p.slice[3])}: Variable '{variable_name}' is not defined")
    if env[variable_name][0] != 'Bool':
        raise BRSyntaxError(
            f"Syntax error at line {p.slice[3].lineno}, column {find_column(data, p.slice[3])}: Variable '{variable_name}' must be boolean")

    p[0] = env[variable_name][1]

def p_procedure_call(p):
    '''procedure_call : CALL LPAREN RPAREN'''

def p_print_statement(p):
    '''print_statement : PRINTVALUES LPAREN print_value_list RPAREN'''
    p[0] = p[3]
    print(p[0])

def p_print_value_list(p):
    '''print_value_list : print_value
                        | print_value_list COMMA print_value'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[3]

def p_print_value(p):
    '''print_value : STRING
                   | ID
                   | view_signal_function'''
    if p.slice[1].type == 'STRING':
        p[0] = p[1]
    elif p.slice[1].type == 'ID':
        variable_name = p[1]
        if variable_name not in env:
            raise BRSyntaxError(
                f"Syntax error at line {p.slice[1].lineno}, column {find_column(data, p.slice[1])}: Variable '{variable_name}' is not defined")
        if isinstance(env[variable_name][1], bool):
            raise BRSyntaxError(
                f"Syntax error at line {p.slice[1].lineno}, column {find_column(data, p.slice[1])}: Variable '{variable_name}' must be numerical")
        p[0] = str(env[variable_name][1])
    elif p.slice[1].type == 'view_signal_function':
        p[0] = str(p[1])

class BRSyntaxError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

def p_error(p):
    if p:
        raise BRSyntaxError(f"Syntax error at line {p.lineno}, column {find_column(data, p)}: Unexpected token {p.value}")
    else:
        raise BRSyntaxError("Syntax error: Unexpected end of input")

# Create the parser
parser = yacc.yacc()
parser.token = None
env = {}
env[1] = 0
env[2] = 0
env[3] = 0
env[4] = 0
env[5] = 0
env[6] = 0

# Test the parser
with open("code.txt", "r") as file:
    data = file.read()

result1 = parser.parse(data)
print(env)