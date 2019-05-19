from __future__ import print_function
import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

class TreePrinter:

    @classmethod
    def make_indent(self, indent):
        return ''.join('| ' * indent)

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + str(self.value))

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + str(self.value))

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + self.value)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass

    @addToClass(AST.Assigment)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + 'RETURN')
        self.value.printTree(indent + 1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + 'PRINT')
        for value in self.values:
            value.printTree(indent + 1)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + self.name)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for n in self.next:
            n.printTree(indent)

    @addToClass(AST.UnaryExpr)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + self.op)
        self.right.printTree(indent + 1)

    @addToClass(AST.MatrixFunction)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + self.func_name)
        self.arg.printTree(indent + 1)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + 'VECTOR')
        for el in self.elements:
            el.printTree(indent + 1)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + 'IF')
        self.condition.printTree(indent + 1)
        print(TreePrinter.make_indent(indent) + 'THEN')
        self.if_body.printTree(indent + 1)
        if self.else_body is not None:
            print(TreePrinter.make_indent(indent) + 'ELSE')
            self.else_body.printTree(indent + 1)

    @addToClass(AST.Ref)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + 'REF')
        self.var.printTree(indent + 1)
        self.first_el.printTree(indent + 1)
        if self.second_el is not None:
            self.second_el.printTree(indent + 1)

    @addToClass(AST.CompExpr)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + 'WHILE')
        self.condition.printTree(indent + 1)
        self.while_body.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + 'FOR')
        self.iter.printTree(indent + 1)
        self.range.printTree(indent + 1)
        self.for_body.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + 'RANGE')
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.LoopFunction)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + self.name)





