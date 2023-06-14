import ply.lex as lex

lexical_errors = []
lexer = None

# language reserved words
keywords = {
   'New' : 'NEW',
   'Num' : 'NUM',
   'Bool' : 'BOOL',
   'String': 'STRING',
   'Proc' : 'PROC',
   'Call' : 'CALL',
   'Values' : 'VALUES',
   'Alter' : 'ALTER',
   'AlterB' : 'ALTER_B',
   'Signal' : 'SIGNAL',
   'EndSignal' : 'END_SIGNAL',
   'ViewSignal' : 'VIEW_SIGNAL',
   'PrintValues' : 'PRINT_VALUES',
   'Write' : 'WRITE',
   'IsTrue': 'IS_TRUE',
   'Repeat' : 'REPEAT',
   'Break' : 'BREAK',
   'Until' : 'UNTIL',
   'While' : 'WHILE',
   'If' : 'IF',
   'Case' : 'CASE',
   'When' : 'WHEN',
   'Then' : 'THEN',
   'Else' : 'ELSE',
}

# List of token names
tokens = [
   'NUMBER',
   'BOOLEAN',
   'COMMENT',
   'ID',
   'ADD',
   'SUB',
   'MUL',
   'DIV',
   'REL_OP',
   'LPAREN',
   'RPAREN',
   'COMMA',
   'SEMICOLON',
] + list(keywords.values())

# Regular expression rules for simple tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r'\,'
t_SEMICOLON = r'\;'

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


def t_NUMBER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


def t_BOOLEAN(t):
    r'True|False'
    t.value = (t.value == 'True')
    return t


def t_STRING(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t


def t_COMMENT(t):
    r'\/\/.*'
    return t


# Arithmetic Operators tokens
def t_ARITH_OP(t):
    r'ADD|SUB|MUL|DIV'
    t.type = t.value
    return t


# Relational Operators tokens
def t_REL_OP(t):
    r'>=|<=|==|<>|>|<'
    t.type = 'REL_OP'
    return t


# Handle variables or identification words
def t_ID(t):
    r'@[\w?]{1,11}'
    return t


# Handle reserved words
def t_reserved(t):
    r'[A-Za-z_][\w_]*'
    token_type = keywords.get(t.value)
    if token_type:
        t.type = token_type
    else:
        line = t.lineno
        column = find_column(lexer.lexdata, t)
        lexical_errors.append("Unrecognized token '%s' at line %d, column %d" % (t.value, line, column))
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Compute column
# input is the input text string
# token is a token instance
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


# Error handling rule
def t_error(t):
    line = t.lexer.lineno
    column = find_column(lexer.lexdata, t)
    lexical_errors.append("Illegal character '%s' at line %d, column %d" % (t.value[0], line, column))


def lexical_analysis():
    global lexer, lexical_errors
    lexical_errors = []
    lexer = lex.lex()
    return lexical_errors
