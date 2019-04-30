

class Node(object):
    pass


class IntNum(Node):
    def __init__(self, value):
        self.value = value

class String(Node):
    def __init__(self, value):
        self.value = value

class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class Return(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class CompExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class UnaryExpr(Node):
    def __init__(self, op, right):
        self.op = op
        self.right = right


class Assigment(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Vector(Node):
    def __init__(self, elements):
        self.elements = elements


class Error(Node):
        pass


class Print(Node):
    def __init__(self, values):
        self.values = values


class Instructions(Node):
    def __init__(self, next):
        self.next = next


class MatrixFunc(Node):
    def __init__(self, func_name, arg):
        self.func_name = func_name
        self.arg = arg


class If(Node):
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body


class Ref(Node):
    def __init__(self, var, first_el, second_el=None):
        self.var = var
        self.first_el = first_el
        self.second_el = second_el

class While(Node):
    def __init__(self, condition, while_body):
        self.condition = condition
        self.while_body = while_body

class For(Node):
    def __init__(self, iter, range, for_body ):
        self.iter = iter
        self.range = range
        self.for_body = for_body

class Range(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class LoopFunction(Node):
    def __init__(self, name):
        self.name = name.upper()


