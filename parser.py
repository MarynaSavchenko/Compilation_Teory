import ply.yacc as yacc;
import scaner


tokens = scaner.tokens

precedence = (
    #('left', '='),
    ('right', 'UMINUS'),
    ('left', 'MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', "'"),
    ('nonassoc', 'IFELSE')
 )



def p_start(p):
    """start : instruction
             | start instruction"""
    if   len(p)==2: print("p[1]=", p[1])
    else:           print("p[2]=", p[2])

def p_instruction(p):
    """instruction : assigment ';'
                | print ';'
                | if_statement
                | while_statement
                | for_statement
                | BREAK ';'
                | CONTINUE ';'
                | return ';' """
    p[0] = p[1]

def p_return(p):
    """return : RETURN digit """

def p_instructions(p):
    """instructions : instruction
                    | instruction instructions
                    | '{' instructions '}' """

def p_print(p):
    """print : PRINT print_vals """
    p[0] = (p[1], p[2])

def p_print_vals(p):
    """print_vals : STRING
                    | STRING ',' print_vals
                    | num
                    | num ',' print_vals """


def p_error(p):
    print(  "syntax error in line %d" % p.lineno)

def p_digit(p):
    """digit : INTNUM
            | FLOATNUM """
    p[0] = p[1]

def p_var(p):
    """var : ID """
    p[0] = p[1]

def p_num(p):
    """num : digit
            | matrix
            | matrix_function
            | uminus
            | var
            | transposition"""


def p_matrix(p):
    """matrix : '[' values ']' """
    p[0] = p[2]

def p_values(p):
    """values :
            | values num ','
            | values num
            | values num ';' """
    if len(p) == 1:
        p[0] = list()
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_num_expression(p):
    """num : num '+' num
            | num '-' num
            | num '*' num
            | num '/' num
            | num DOTADD num
            | num DOTSUB num
            | num DOTMUL num
            | num DOTDIV num"""

    """if p[2] == '+':
        p[0] = (p[1], '+', p[3]);
    elif p[2] == '-':
        p[0] = (p[1], '-', p[3]);
    elif p[2] == '*':
        p[0] = (p[1], "*", p[3]);
    elif p[2] == '/':
        p[0] = (p[1], "/", p[3]);"""

    p[0] = (p[1], p[2], p[3])


def p_compare_expression(p):
    """compare_expression : num EQUAL num
                | num NOTEQUAL num
                | num '>' num
                | num '<' num
                | num LE num
                | num GE num"""
    """if p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '!=':
        p[0] = p[1] != p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
        """
    p[0]=(p[1], p[2], p[3])

def p_uminus(p):
    """uminus : '-' num %prec UMINUS """
    p[0] = ('-', p[2])

def p_transposition(p):
    """transposition : num "'" """
    p[0] = (p[1], "'")


def p_assigment_op(p):
    """assigment_op : MULASSIGN
                   | DIVASSIGN
                   | SUBASSIGN
                   | ADDASSIGN
                   | '=' """
    p[0] = p[1]

def p_assigment(p):
    """assigment : var assigment_op num
                | range assigment_op num """
    p[0] = (p[1], p[2], p[3])


def p_matrix_function(p):
    """matrix_function : EYE LPAREN num RPAREN
                  | ONES LPAREN num RPAREN
                  | ZEROS LPAREN num RPAREN"""
    p[0] = (p[1], p[2], p[3], p[4])


def p_if_statement(p):
    """if_statement : IF LPAREN compare_expression RPAREN instructions
                  | IF LPAREN compare_expression RPAREN instructions ELSE instructions %prec IFELSE"""
    #if p[3]:
     #   p[0] = p[5]
    #else:
     #   if len(p) == 10:
      #      p[0] = p[8]
    p[0] = p[5]

def p_range(p):
    """range : var '[' digit ',' digit ']' """
    p[0] = (p[1],p[2],p[3],p[4],p[5],p[6])


def p_while_statement(p):
    """while_statement : WHILE LPAREN compare_expression RPAREN instructions """
    #while (p[3]):
    p[0] = p[5]#p[5]

def p_for_statement(p):
    """for_statement : FOR var '=' num ':' num instructions """
    p[0] = p[3]



parser = yacc.yacc()