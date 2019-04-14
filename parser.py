import ply.yacc as yacc;
import scanner

import AST


tokens = scanner.tokens

precedence = (
    #('left', '='),
    ('right', 'UMINUS'),
    ('left', 'MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', "'"),
    ('nonassoc', 'IFELSE')
 )


def p_instructions(p):
    """instructions : instruction
                    | instruction instructions
                    | '{' instructions '}' """
    if len(p) == 2:
        p[0] = AST.Instructions([p[1]])
    elif len(p) == 3:
        p[0] = p[2]
        p[0].next = [p[1]] + p[0].next

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
    p[0] = AST.Return(p[1])


def p_print(p):
    """print : PRINT print_vals """
    p[0] = AST.Print(p[2])

def p_print_vals(p):
    """print_vals : STRING
                    | STRING ',' print_vals
                    | num
                    | num ',' print_vals """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_error(p):
    print("syntax error in line %d" % p.lineno)

def p_digit(p):
    """digit : INTNUM
            | FLOATNUM """
    if isinstance(p[1], int):
        p[0] = AST.IntNum(p[1])
    elif isinstance(p[1], float):
        p[1] = AST.FloatNum(p[1])

def p_var(p):
    """var : ID """
    p[0] = AST.Variable(p[1])

def p_num(p):
    """num : digit
            | matrix
            | matrix_function
            | uminus
            | var
            | transposition"""
    p[0] = p[1]

def p_matrix(p):
    """matrix : '[' values ']' """
    p[0] = AST.Matrix(p[2])

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

    p[0] = AST.BinExpr(p[2], p[1], p[3])


def p_compare_expression(p):
    """compare_expression : num EQUAL num
                | num NOTEQUAL num
                | num '>' num
                | num '<' num
                | num LE num
                | num GE num"""
    p[0] = AST.BinExpr(p[2], p[1], p[3])

def p_uminus(p):
    """uminus : '-' num %prec UMINUS """
    p[0] = AST.UnaryExpr(p[1], p[2])

def p_transposition(p):
    """transposition : num "'" """
    p[0] = AST.UnaryExpr(p[2], p[1])


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
    p[0] = AST.Assigment(p[2], p[1], p[3])


def p_matrix_function(p):
    """matrix_function : EYE LPAREN num RPAREN
                  | ONES LPAREN num RPAREN
                  | ZEROS LPAREN num RPAREN"""
    p[0] = AST.MatrixFunc(p[1], p[3])


def p_if_statement(p):
    """if_statement : IF LPAREN compare_expression RPAREN instructions
                  | IF LPAREN compare_expression RPAREN instructions ELSE instructions %prec IFELSE"""
    if len(p) == 6:
        p[0] = AST.If(p[3], p[5])
    else:
        p[0] = AST.If(p[3], p[5], p[7])

def p_range(p):
    """range : var '[' digit ',' digit ']' """
    p[0] = AST.Ref(p[1],p[3],p[5])


def p_while_statement(p):
    """while_statement : WHILE LPAREN compare_expression RPAREN instructions """
    #while (p[3]):
    p[0] = p[5]#p[5]

def p_for_statement(p):
    """for_statement : FOR var '=' num ':' num instructions """
    p[0] = p[3]



parser = yacc.yacc()