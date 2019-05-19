

import ply.yacc as yacc;
import scanner


tokens = scanner.tokens

precedence = (
    #('left', '='),
    ('right', 'UMINUS'),
    ('left', 'MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', "'"),
    ('left', 'IFELSE')
 )
symtab = {}

def p_error(p):
    print(  "syntax error in line %d" % p.lineno)

def p_start(p):
    """start : VAR
             | start VAR"""
    if   len(p)==2: print("p[1]=", p[1])
    else:           print("p[2]=", p[2])


def p_expression_matrix(p):
    """ARRAY : EYE LPAREN INTNUM RPAREN
                  | ONES LPAREN INTNUM RPAREN
                  | ZEROS LPAREN INTNUM RPAREN"""
    p[0] = (p[1], p[2], p[3], p[4])

def p_expression_print_return(p):
    """VAR :  PRINT values ';'
            | RETURN INTNUM ';'
            | PRINT STRING ';'
            | PRINT VAR ';' """
    p[0] = (p[1], p[2])

def p_expression_continue_break(p):
    """VAR : CONTINUE ';'
           | BREAK ';' """
    p[0] = (p[1])

def p_if_statement(p):
    """VAR : IF LPAREN COMPARE RPAREN VAR
                  | IF LPAREN COMPARE RPAREN VAR  ELSE VAR %prec IFELSE"""
    #if p[3]:
     #   p[0] = p[5]
    #else:
     #   if len(p) == 10:
      #      p[0] = p[8]
    p[0] = p[5]

def p_while_statement(p):
    """VAR : WHILE LPAREN COMPARE RPAREN VAR """
    #while (p[3]):
    p[0] = p[5]#p[5]

def p_for_statement(p):
    """VAR : FOR VAR VAR """
    p[0] = p[3]

def p_expression_id(p):
    """VAR : ID"""
    val = symtab.get(p[1])
    if val:
        p[0] = val
    else:
        p[0] = 0
        print("%s not used\n" %p[1])

def p_expression_assignment(p):
    """VAR : ID '=' VAR ';'
                  | ID '=' ARRAY ';'
                  | ID ARRAY '=' VAR ';'
                  | ID '=' VAR ':' VAR """
    if (len(p) == 5):
        p[0] = p[3]
        symtab[p[1]] = p[3]
    else:
        p[0] = p[4]
        symtab[p[1]] = p[4]


def p_expression_sum(p):
    """VAR : VAR '+' VAR
                  | VAR '-' VAR"""
    if   p[2]=='+': p[0] = (p[1] ,'+', p[3]);
    elif p[2]=='-': p[0] = (p[1] ,'-', p[3]);


def p_expression_mul(p):
    """VAR : VAR '*' VAR
                  | VAR '/' VAR"""
    if   p[2]=='*':
        p[0] = (p[1] ,"*", p[3]);
    elif p[2]=='/':
        p[0] = (p[1] ,"/", p[3]);

def p_matrix_foo(p):
    """VAR : VAR DOTADD VAR
            | VAR DOTSUB VAR
            | VAR DOTMUL VAR
            | VAR DOTDIV VAR"""
    p[0] = (p[1],p[2],p[3])

def p_special_assign(p):
    """VAR : ID MULASSIGN VAR ';'
           | ID DIVASSIGN VAR ';'
           | ID SUBASSIGN VAR ';'
          | ID ADDASSIGN VAR ';'"""
    p[0] = (p[1],p[2],p[3])


def p_comparison_binop(p):
    """COMPARE : VAR EQUAL VAR
                          | VAR NOTEQUAL VAR
                          | VAR '>' VAR
                          | VAR '<' VAR
                          | VAR LE VAR
                          | VAR GE VAR"""
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

def p_expr_uminus(p):
    """VAR : '-' VAR %prec UMINUS """
    p[0] = ('-', p[2])

def p_transpoz(p):
    """VAR : VAR "'" """
    p[0] = (p[1], "'")


def p_values(p):
    """values :
              | values VAR ','
              | values VAR
              | values VAR ';' """
    if len(p) == 1:
        p[0] = list()
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_array(p):
    """ARRAY : '[' values ']' """
    p[0] = p[2]

def p_num(p):
    """VAR : INTNUM
            | FLOATNUM"""
    p[0] = p[1]



def p_expression_group(p):
    """VAR : '{' values '}' """
    p[0] = ('group-expression', p[2])



parser = yacc.yacc()