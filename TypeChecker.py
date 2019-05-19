#!/usr/bin/python
from collections import defaultdict

import AST
from SymbolTable import SymbolTable, VectorType, VariableSymbol

_type = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

for op in ['+', '-', '*', '/', '+=', '-=', '*=', '/=']:
    _type[op]['float']['float'] = 'float'
    _type[op]['int']['int'] = 'int'
    _type[op]['int']['float'] = 'float'
    _type[op]['float']['int'] = 'float'
    _type[op]['vector']['vector'] = 'vector'

for op in ['<', '>', '>=', '<=', '==', '!=']:
    _type[op]['float']['float'] = 'float'
    _type[op]['int']['int'] = 'int'
    _type[op]['int']['float'] = 'float'
    _type[op]['float']['int'] = 'float'

for op in ['.+', '.-', '.*', './']:
    _type[op]['vector']['vector'] = 'vector'

_type['\'']['vector'][None] = 'vector'
_type['-']['vector'][None] = 'vector'
_type['-']['int'][None] = 'int'
_type['-']['float'][None] = 'float'
_type['+']['string']['string'] = 'string'


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
        self.symbol_table = SymbolTable(None, 'main')
        self.loop_entry = 0

    def visit_IntNum(self, node):
        return 'int'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Return(self, node):
        return self.visit(node.value)

    def visit_Variable(self, node):
        variable_val = self.symbol_table.get(node.name)
        if variable_val is None:
            print(f"Error in line {node.line}. Unknown variable")
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
                        print(f"Error in line {node.line}. Different size or type of matrix")
                        return ErrorType()
            return result_type
        else:
            print(f"Error in line {node.line}. Wrong type")
            return ErrorType()

    def visit_CompExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        if isinstance(type2, ErrorType) or isinstance(type1, ErrorType):
            return ErrorType()
        result_type = _type[op][str(type1)][str(type2)]
        if result_type is not None:
            return result_type
        else:
            print(f"Error in line {node.line}")
            return ErrorType()

    def visit_UnaryExpr(self, node):
        type1 = self.visit(node.right)
        op = node.op
        if op == ['\'']:
            result_type = _type[op][str(type1)][None]
            if result_type is 'vector':
                if type1.dimension != 2:
                    print(f"Error in line {node.line}. Transpose for 2 dimension.")
                    return ErrorType()
                type1.size[0], type1.size[1] = type1.size[1], type1.size[0]
                return result_type
            else:
                print(f"Error in line {node.line}. Wrong type for transpose")
                return ErrorType()
        else:
            result_type = _type[op][str(type1)][None]
            if result_type is not None:
                return result_type
            else:
                print(f"Error in line {node.line}")
                return ErrorType()

    def visit_Assigment(self, node):
        type2 = self.visit(node.right)
        op = node.op
        if isinstance(type2, ErrorType):
            return ErrorType()
        if op == '=':
            if type(node.left) == AST.Variable:
                self.symbol_table.put(node.left.name, VariableSymbol(node.left.name, type2))
            else:
                self.symbol_table.put(node.left.var, VariableSymbol(node.left.var, type2))
        else:
            type1 = self.visit(node.left)
            result_type = _type[op][str(type1)][str(type2)]
            if result_type is not None:
                if result_type == 'vector':
                    if isinstance(type1, VectorType) and isinstance(type2, VectorType):
                        if type1.size != type2.size:
                            print(f"Error in line {node.line}")
                            return ErrorType()
                return result_type
            else:
                print(f"Error in line {node.line}. Wrong op with such types")
                return ErrorType()

    def visit_Vector(self, node):
        elements = node.elements
        first_element = elements[0]
        if type(first_element) == AST.Vector:
            for vector in elements:
                if len(vector.elements) != len(first_element.elements):
                    print(f"Error in line {node.line}. Different length")
                    return ErrorType()
                for el in vector.elements:
                    if type(el) != type(first_element.elements[0]):
                        print(f"Error in line {node.line}.Wrong type in vector")
                        return ErrorType()
            return VectorType([len(elements), len(first_element.elements)], type(first_element), 2)
        else:
            for element in elements:
                if type(element) != type(first_element):
                    print(f"Error in line {node.line}. Different types")
                    return ErrorType()
            return VectorType([len(elements)], type(first_element), 1)

    def visit_Print(self, node):
        self.visit(node.values)

    def visit_Instructions(self, node):
        for instruction in node.next:
            self.visit(instruction)

    def visit_MatrixFunction(self, node):
        type = self.visit(node.arg)
        if type == 'int':
            return VectorType([node.arg, node.arg], 'int', 2)
        else:
            print(f"Error in line {node.line}. Wrong type in matrix function {node.func_name}")
            return ErrorType()

    def visit_If(self, node):
        self.visit(node.condition)
        self.symbol_table = self.symbol_table.pushScope('if')
        self.visit(node.if_body)
        self.symbol_table = self.symbol_table.popScope()
        if node.else_body:
            self.symbol_table.pushScope('else')
            self.visit(node.else_body)
            self.symbol_table.popScope()

    def visit_Ref(self, node):
        type_var = self.visit(node.var)
        if not isinstance(type_var, VectorType):
            print(f"Error in line {node.line}. Vector is needed in ref")
            return ErrorType()
        type1 = self.visit(node.first_el)
        if self.second_el:
            type2 = self.visit(node.second_el)
            row = node.first_el.value
            column = node.second_el.value
            if type2 == 'int' and type1 == 'int':
                if type_var.dimension != 2:
                    print(f"Error in line {node.line}. Wrong dimension")
                    return ErrorType()
                if row >= type_var.size[0] or column >= type_var.size[1]:
                    print(f"Error in line {node.line}. Index out")
                    return ErrorType()
                return type_var.type
            else:
                print(f"Error in line {node.line}. Wrong types")
                return ErrorType()
        else:
            if type1 == 'int':
                el = node.first_el.value
                if type_var.dimension != 1:
                    print(f"Error in line {node.line}. Error dimension")
                    return ErrorType()
                if el >= type_var.size:
                    print(f"Error in line {node.line}. Index out")
                    return ErrorType()
                return type_var.type
            else:
                print(f"Error in line {node.line}. Index should be int")
                return ErrorType()

    def visit_While(self, node):
        self.loop_entry += 1
        self.symbol_table = self.symbol_table.pushScope('while')
        self.visit(node.condition)
        self.visit(node.while_body)
        self.symbol_table = self.symbol_table.popScope()
        self.loop_entry -= 1

    def visit_For(self, node):
        self.loop_entry += 1
        self.symbol_table = self.symbol_table.pushScope('for')
        type1 = self.visit(node.range)
        self.symbol_table.put(node.iter.name, VariableSymbol(node.iter.name, type1))
        self.visit(node.for_body)
        self.symbol_table = self.symbol_table.popScope()
        self.loop_entry -= 1

    def visit_Range(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        if type1 != 'int' or isinstance(type1, ErrorType):
            print(f"Error in line {node.line}. Error in type of left el")
            return ErrorType()
        if type2 != 'int' or isinstance(type2, ErrorType):
            print(f"Error in line {node.line}. Error in type of right el")
            return ErrorType()
        return type2

    def visit_LoopFunction(self, node):
        if self.loop_entry <= 0:
            print(f"Error in line {node.line}. Break or Continue outside the loop")
