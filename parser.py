import ply.yacc as yacc;
import scanner

import AST

tokens = scanner.tokens

precedence = (
    ('nonassoc', 'IF'),
    ('nonassoc', 'IFELSE'),
    ('nonassoc', '<', '>', 'GE', 'LE', 'EQUAL', 'NOTEQUAL'),
    ('right', 'MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN'),
    ('left', '+', '-'),
    ('left', 'DOTADD', 'DOTSUB'),
    ('left', '*', '/'),
    ('left', 'DOTMUL', 'DOTDIV'),
    ('right', 'UMINUS'),
    ('left', "'"),
)


def p_instructions(p):
    """instructions : instruction
                    | instruction instructions """
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
                | loop_function ';'
                | return ';'
                | '{' instructions '}' """
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_error(p):
    print("syntax error in line %d" % p.lineno)


def p_loop_function(p):
    """loop_function : BREAK
                    | CONTINUE """
    p[0] = AST.LoopFunction(p[1], p.lineno(1))


def p_return(p):
    """return : RETURN expression """
    p[0] = AST.Return(p[2])


def p_print(p):
    """print : PRINT print_vals """
    p[0] = AST.Print(p[2])


def p_print_vals(p):
    """print_vals : string
                    | string ',' print_vals
                    | expression
                    | expression ',' print_vals """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_numer(p):
    """numer : INTNUM
            | FLOATNUM """

    if isinstance(p[1], int):
        p[0] = AST.IntNum(p[1])
    else:
        p[0] = AST.FloatNum(p[1])

def p_num_expression(p):
    """num_expression : numer
                    | var """
    p[0] = p[1]




def p_string(p):
    """string : STRING """
    p[0] = AST.String(p[1])


def p_var(p):
    """var : ID """
    p[0] = AST.Variable(p[1], p.lineno(1))


def p_expression(p):
    """expression : num_expression
            | matrix
            | matrix_function
            | uminus
            | transposition
            | ref """
    p[0] = p[1]


def p_matrix(p):
    """matrix : '[' matrix_body ']'
                | '[' vector_body ']' """
    p[0] = AST.Vector(p[2], p.lineno(1))


def p_matrix_body(p):
    """matrix_body : vector
                    | matrix_body ';' vector"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0] += [p[3]]


def p_vector(p):
    """vector : vector_body """
    p[0] = AST.Vector(p[1], p.lineno(1))


def p_vector_body(p):
    """vector_body : expression
                  | vector_body ',' expression """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0] += [p[3]]


def p_bin_expression(p):
    """expression : expression '+' expression
            | expression '-' expression
            | expression '*' expression
            | expression '/' expression
            | expression DOTADD expression
            | expression DOTSUB expression
            | expression DOTMUL expression
            | expression DOTDIV expression"""

    p[0] = AST.BinExpr(p[2], p[1], p[3], p.lineno(2))


def p_compare_expression(p):
    """compare_expression : expression EQUAL expression
                | expression NOTEQUAL expression
                | expression '>' expression
                | expression '<' expression
                | expression LE expression
                | expression GE expression"""
    p[0] = AST.CompExpr(p[2], p[1], p[3], p.lineno(2))


def p_uminus(p):
    """uminus : '-' expression %prec UMINUS """
    p[0] = AST.UnaryExpr(p[1], p[2], p.lineno(1))


def p_transposition(p):
    """transposition : expression "'" """
    p[0] = AST.UnaryExpr(p[2], p[1], p.lineno(1))


def p_assigment_op(p):
    """assigment_op : MULASSIGN
                   | DIVASSIGN
                   | SUBASSIGN
                   | ADDASSIGN
                   | '=' """
    p[0] = p[1]


def p_assigment(p):
    """assigment : var assigment_op expression
                | ref assigment_op expression """
    p[0] = AST.Assigment(p[2], p[1], p[3], p.lineno(1))


def p_matrix_function(p):
    """matrix_function : EYE LPAREN expression RPAREN
                  | ONES LPAREN expression RPAREN
                  | ZEROS LPAREN expression RPAREN"""
    p[0] = AST.MatrixFunction(p[1], p[3], p.lineno(1))

def p_if_statement(p):
    """if_statement : IF LPAREN compare_expression RPAREN instruction
                  | IF LPAREN compare_expression RPAREN instruction ELSE instruction %prec IFELSE"""
    if len(p) == 6:
        p[0] = AST.If(p[3], p[5])
    else:
        p[0] = AST.If(p[3], p[5], p[7])


def p_ref(p):
    """ref : var '[' num_expression ',' num_expression ']'
            | var '[' num_expression ']' """
    if len(p) == 7:
        p[0] = AST.Ref(p.lineno(1), p[1], p[3], p[5])
    else:
        p[0] = AST.Ref(p.lineno(1), p[1], p[3])


def p_while_statement(p):
    """while_statement : WHILE LPAREN compare_expression RPAREN instruction """
    p[0] = AST.While(p[3], p[5])


def p_for_statement(p):
    """for_statement : FOR var '=' range instruction """
    p[0] = AST.For(p[2], p[4], p[5])


def p_range(p):
    """range : expression ':' expression """
    p[0] = AST.Range(p[1], p[3], p.lineno(2))


parser = yacc.yacc()
