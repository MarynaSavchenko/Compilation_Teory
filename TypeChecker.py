#!/usr/bin/python
import AST
from SymbolTable import SymbolTable, VectorType, VariableSymbol


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)

class ErrorType:
    pass


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit_IntNum(self, node):
        return 'int'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_Return(self, node):
        return self.visit(node.value)

    def visit_Variable(self, node):
        variable_val = self.symbol_table.get(node.name)
        if variable_val is None:
            print(f"Error in line . Unknown variable")
            return ErrorType()
        return variable_val.type

    def visit_BinExpr(self, node):
        # alternative usage,
        # requires definition of accept method in class Node
        type1 = self.visit(node.left)  # type1 = node.left.accept(self)
        type2 = self.visit(node.right)  # type2 = node.right.accept(self)
        op = node.op
        if isinstance(type1, ErrorType) or isinstance(type2, ErrorType):
            return ErrorType()
        result_type = _type[op][str(type1)][str(type2)]
        if result_type is not None:
            if result_type == 'vector':
                if isinstance(type1, VectorType) and isinstance(type2, VectorType):
                    if type1.size != type2.size or type1.type != type2.type:
                        print(f"Error in line . Different size of matrix")
                        return ErrorType()
                    #else:
            return result_type
        else:
            print(f"Error at line. Wrong type")
            return ErrorType()

    def visit_CompExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        if isinstance(type2, ErrorType) or isinstance(type1, ErrorType):
            return ErrorType
        result_type = _type[op][str(type1)][str(type2)]
        if result_type is not None:
            return result_type
        else:
            print(f"Error in line")
            return ErrorType()

    def visit_UnaryExpr(self, node):
        type1 = self.visit(node.right)
        result_type = _type['-'][str(type1)][None]
        if result_type is not None:
            return result_type
        else:
            print(f"Error in line")
            return ErrorType()

    def visit_Assigment(self, node):
        type1 = self.visit(node.right)
        op = node.op
        if isinstance(type1, ErrorType):
            return ErrorType
        if op == '=':
            self.symbol_table.put(node.left.name, VariableSymbol(node.left.name, type1))
        else:
            type2 = self.visit(node.left)
            result_type = _type[op][str(type2)][str(type1)]
            if result_type is not None:
                if result_type == 'vector':
                    if isinstance(type1, VectorType) and isinstance(type2, VectorType):
                        if type1.size != type2.size:
                            print(f"Error in line ")
                            return ErrorType()
                        #else:
                return result_type
            else:
                print(f"Error in line")
                return ErrorType()

    def visit_Matrix(self, node):
        pass

    def visit_Print(self, node):
        pass

    def visit_Instructions(self, node):
        pass

    def visit_MatrixFunc(self, node):
        pass

    def visit_If(self, node):
        pass

    def visit_Ref(self, node):
        pass

    def visit_While(self, node):
        pass

    def visit_For(self, node):
        pass

    def visit_Range(self, node):
        pass

    def visit_LoopFunction(self, node):
        pass

