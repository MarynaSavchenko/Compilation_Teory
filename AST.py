class Node(object):
    def accept(self, visitor):
        return visitor.visit(self)


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name, line):
        self.name = name
        self.line = line


class BinExpr(Node):
    def __init__(self, op, left, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line


class CompExpr(Node):
    def __init__(self, op, left, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line


class UnaryExpr(Node):
    def __init__(self, op, right, line):
        self.op = op
        self.right = right
        self.line = line


class Assigment(Node):
    def __init__(self, op, left, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line


class Vector(Node):
    def __init__(self, elements, line):
        self.elements = elements
        self.line = line


class Error(Node):
    pass


class Print(Node):
    def __init__(self, values):
        self.values = values


class Instructions(Node):
    def __init__(self, next):
        self.next = next

class MatrixFunction(Node):
    def __init__(self, func_name, arg, line):
        self.func_name = func_name
        self.arg = arg
        self.line = line


class If(Node):
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body


class Ref(Node):
    def __init__(self, line, var, first_el, second_el=None):
        self.var = var
        self.first_el = first_el
        self.second_el = second_el
        self.line = line


class While(Node):
    def __init__(self, condition, while_body):
        self.condition = condition
        self.while_body = while_body


class For(Node):
    def __init__(self, iter, range, for_body):
        self.iter = iter
        self.range = range
        self.for_body = for_body


class Range(Node):
    def __init__(self, left, right, line):
        self.left = left
        self.right = right
        self.line = line


class LoopFunction(Node):
    def __init__(self, name, line):
        self.name = name.upper()
        self.line = line


class Return(Node):
    def __init__(self, value):
        self.value = value
