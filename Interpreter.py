import numpy

import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys

sys.setrecursionlimit(10000)

binOps = {
    "+": (lambda x, y: x + y),
    "-": (lambda x, y: x - y),
    "*": (lambda x, y: x * y),
    "/": (lambda x, y: x / y),

}

comprOps = {
    ">": (lambda x, y: x > y),
    "<": (lambda x, y: x < y),
    ">=": (lambda x, y: x >= y),
    "<=": (lambda x, y: x <= y),
    "==": (lambda x, y: x == y),
    "!=": (lambda x, y: x != y),
}

assignOps = {
    "+=": (lambda x, y: x + y),
    "-=": (lambda x, y: x - y),
    "*=": (lambda x, y: x * y),
    "/*": (lambda x, y: x / y),
}


class Interpreter(object):

    def __init__(self):
        self.memoryStack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.IntNum)
    def visit(self, node):
        return int(node.value)

    @when(AST.FloatNum)
    def visit(self, node):
        return float(self.value)

    @when(AST.String)
    def visit(self, node):
        return str(node.value)

    @when(AST.Variable)
    def visit(self, node):
        return self.memoryStack.get(node.name)

    @when(AST.BinExpr)  # TODO matrix
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return binOps[node.op](r1, r2)

    @when(AST.CompExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return comprOps[node.op](r1, r2)

    @when(AST.UnaryExpr)
    def visit(self, node):
        op = node.op
        if op == '-':
            return - node.right.accept(self)
        else:
            array = numpy.array(self.memoryStack.get(node.right))
            return array.transpose()

    @when(AST.Assigment)
    def visit(self, node):
        r1 = node.right.accept(self)
        if node.op == '=':
            if isinstance(node.left, AST.Variable):  # set var
                if self.memoryStack.get(node.left.name):
                    self.memoryStack.set(node.left.name, r1)
                else:
                    self.memoryStack.insert(node.left.name, r1)
            else:  # assign elements in matrix
                array = self.memoryStack.get(node.left.var.name)
                first_el = node.left.first_el.accept(self)
                if node.left.second_el:
                    second_el = node.left.second_el.accept(self)
                    array[first_el][second_el] = r1
                else:
                    array[first_el] = r1
        else:
            if isinstance(node.left, AST.Variable):
                r2 = self.memoryStack.get(node.left.name)

                result = assignOps[node.op](r2, r1)  # TODO matrix
                self.memoryStack.set(node.left.name, result)
            else:  # Ref
                array = self.memoryStack.get(node.left.var.name)
                first_el = node.left.first_el.accept(self)
                if node.left.second_el:  # TODO matrix
                    second_el = node.left.second_el.accept(self)
                    array[first_el][second_el] = assignOps[node.op](array[first_el][second_el], r1)
                else:
                    array[first_el] = assignOps[node.op](array[first_el], r1)

    @when(AST.Vector)
    def visit(self, node):
        return [element.accept(self) for element in node.elements]

    @when(AST.Error)
    def visit(self, node):
        pass

    @when(AST.Print)
    def visit(self, node):
        values = []
        for value in node.values:
            values.append(value.accept(self))
        print(*values)

    @when(AST.Instructions)
    def visit(self, node):
        for instr in node.next:
            instr.accept(self)

    @when(AST.MatrixFunction)
    def visit(self, node):
        r1 = node.arg.accept(self)
        if node.func_name == 'ones':
            return numpy.ones((r1, r1))
        elif node.func_name == 'zeros':
            return numpy.zeros((r1, r1))
        else:
            return numpy.eye(r1)

    @when(AST.If)
    def visit(self, node):
        if node.condition.accept(self):
            self.memoryStack.push(Memory("if"))
            result = node.if_body.accept(self)
            self.memoryStack.pop()
            return result
        else:
            if node.else_body:
                self.memoryStack.push(Memory("else"))
                result = node.else_body.accept(self)
                self.memoryStack.pop()
                return result

    @when(AST.Ref)
    def visit(self, node):
        array = self.memoryStack.get(node.var)
        first_el = node.first_el.accept(self)
        if node.second_el:
            second_el = node.second_el.accept(self)
            return array[first_el][second_el]
        else:
            return array[first_el]

    # simplistic while loop interpretation
    @when(AST.While)
    def visit(self, node):
        while node.condition.accept(self):
            try:
                self.memoryStack.push(Memory("while"))
                node.while_body.accept(self)
            except ContinueException:
                pass
            except BreakException:
                break
            finally:
                self.memoryStack.pop()

    @when(AST.For)
    def visit(self, node):
        range = node.range.accept(self)

        if self.memoryStack.get(node.iter.name):
            self.memoryStack.set(node.iter.name, range['left'])
        else:
            self.memoryStack.insert(node.iter.name, range['left'])

        while self.memoryStack.get(node.iter.name) <= range['right']:
            try:
                self.memoryStack.push(Memory("for"))
                node.for_body.accept(self)
            except ContinueException:
                pass
            except BreakException:
                break
            finally:
                self.memoryStack.pop()

            new_range = self.memoryStack.get(node.iter.name) + 1
            self.memoryStack.set(node.iter.name, new_range)

    @when(AST.Range)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        return {'left': left, 'right': right}

    @when(AST.LoopFunction)
    def visit(self, node):
        if node.name == 'break':
            raise BreakException
        else:
            raise ContinueException

    @when(AST.Return)
    def visit(self, node):
        return node.value.accept(self)
