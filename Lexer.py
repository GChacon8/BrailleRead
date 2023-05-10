import ply.lex as lex
import codecs

reserverdWords = ["New", "Num", "Bool", "True", "False", "Proc", "CALL", "Values", "Alter", "AlterB", "Signal", "ViewSignal", 
                  "IsTrue", "Repeat", "Until", "While", "Case", "When", "Then", "Else", "PrintValues", "Break", "Master"]

tokens = reserverdWords + ["ID", "INTERGER", "COMMA", "LPARENTHESIS", "RPARENTHESIS", "SEMMICOLOM",
                            "Less", "LessEqual", "Greater", "GreaterEqual", "Equals", "Different","TEXTVALUE", "ADD", "SUB", "MUL", "DIV", "Comment"]

#Reserved words
t_New = 'New'
t_Num = 'Num'
t_Bool = 'Bool'
t_True = "True"
t_False = "False"
t_Proc = 'Proc'
t_CALL = 'CALL'
t_Values = 'Values'
t_Alter = 'Alter'
t_AlterB = 'AlterB'
t_Signal = 'Signal'
t_ViewSignal = 'ViewSignal'
t_IsTrue = 'IsTrue'
t_Repeat = 'Repeat'
t_Until = 'Until'
t_While = 'While'
t_Case = 'Case'
t_When = 'When'
t_Then = 'Then'
t_Else = 'Else'
t_Break = 'Break'
t_PrintValues = 'PrintValues'

# t_Master = 'Master'

#ID
t_ID = r'@[a-zA-Z0-9_?][a-zA-Z0-9_?][a-zA-Z0-9_?]{0,10}'

#Ops
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'

#Symbols
t_ignore = '\t \r'
t_COMMA = r'\,'
t_SEMMICOLOM = r';'
t_LPARENTHESIS = r'\('
t_RPARENTHESIS = r'\)'
t_TEXTVALUE = r'\".+\"'

# Conditionals
t_Less = r'<'
t_LessEqual = r'<='
t_Greater = r'>'
t_GreaterEqual = r'>='
t_Equals = r'=='
t_Different = r'!='

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_Comment(t):
    r'//.*'
    pass

def t_error(t):
    print ("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
