import ply.lex as lex

reserved = {'if': 'IF',
            'else': 'ELSE',
            'while': 'WHILE',
            'break': 'BREAK',
            'continue': 'CONTINUE',
            'return': 'RETURN',
            'eye': 'EYE',
            'zeros': 'ZEROS',
            'ones': 'ONES',
            'print': 'PRINT',
            'for': 'FOR'}

tokens = ['FLOATNUM', 'INTNUM',  'ID', 'STRING', 'GE', 'LE', 'DOTADD', 'SUBASSIGN',
          'DOTSUB', 'MULASSIGN', 'DOTMUL', 'DIVASSIGN', 'DOTDIV',
          'EQUAL', 'ADDASSIGN', 'NOTEQUAL', 'LPAREN', 'RPAREN'] + list(reserved.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_GE = r'>='
t_LE = r'<='
t_DOTADD = r'\.\+'
t_SUBASSIGN = r'-='
t_ADDASSIGN = r'\+='
t_DOTSUB = r'\.-'
t_MULASSIGN = r'\*='
t_DOTMUL = r'\.\*'
t_DIVASSIGN = r'/='
t_DOTDIV = '\./'
t_EQUAL = r'=='
t_NOTEQUAL = r'!='

literals = "+-*/><;=[]{},':"

t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

def t_FLOATNUM(t):
    r'((\d+\.\d*)|(\d*\.\d+)([eE][+-]?\d+)?)'
    return t


def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_STRING(t):
    r'"([^"]+|\\"|\\\\)*"'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character: " + "'" +
          t.value[0] + "'" + " in line: " + str(t.lineno))
    t.lexer.skip(1)


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

lexer = lex.lex()
