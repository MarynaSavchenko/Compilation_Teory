#!/usr/bin/python
from collections import defaultdict

import AST
from SymbolTable import SymbolTable, VectorType, VariableSymbol

_type = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
standard_ops = ['+', '-', '*', '/']
matrix_ops = ['.+', '.-', '.*', './']
relation_ops = ['<', '>', '>=', '<=', '==', '!=']
assign_ops = ['+=', '-=', '*=', '/=']

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


#_type['+']['string']['string'] = 'string'

_type['\'']['vector'][None] = 'vector'
_type['-']['vector'][None] = 'vector'
_type['-']['int'][None] = 'int'
_type['-']['float'][None] = 'float'



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

    def visir_String(self, node):
        return 'string'

    def visit_Return(self, node):
        return self.visit(node.value)

    def visit_Variable(self, node):
        print('wow')
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
        op = node.op
        result_type = _type[op][str(type1)][None]
        ###
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

    def visit_Vector(self, node):
        vectors = node.elements
        first_vector = vectors[0]
        if type(first_vector) == AST.Vector:
            for vector in vectors:
                if not len(vector.elements) == len(first_vector.elements):
                    print("Error in line. Different length")
                    return ErrorType()
                for el in vector.elements:
                    if not type(el) == type(first_vector.elements[0]):
                        print("Wrong type in vector")
                        return ErrorType()
            return VectorType([len(vectors), len(first_vector)], type(first_vector), 2)
        else:
            for vector in vectors:
                if not type(vector) == type(first_vector):
                    print("error in vector.Different types")
                    return ErrorType()
            return VectorType([len(first_vector)], type(first_vector), 1)


    def visit_Print(self, node):
        self.visit(node.values)

    def visit_Instructions(self, node):
        for instruction in node.next:
            self.visit(instruction)

    def visit_MatrixFunc(self, node):
        type = self.visit(node.arg)
        if type == 'int':
            return VectorType([node.arg, node.arg], 'int', 2)
        else:
            print("Wrong type in matrix function")
            return ErrorType()

    def visit_If(self, node):
        self.visit(node.condition)
        self.symbol_table.pushScope('if')
        self.visit(node.if_body)
        self.symbol_table.popScope()
        if node.else_body is not None:
            self.symbol_table.pushScope('else')
            self.visit(node.else_body)
            self.symbol_table.popScope()

    def visit_Ref(self, node):
        type_name = self.visit(node.var)
        if not isinstance(type_name, VectorType):
            print("Error")
            return ErrorType()
        type1 = self.visit(node.first_el)
        if self.second_el is not None:
            type2 = self.visit(node.second_el)
            val1 = node.first_el.value
            val2 = node.second_el.value
            if type2 == 'int' and type1 == 'int':
                if type_name.dimension != 2:
                    print("Wrong dimision")
                    return ErrorType()
                if val1 >= type_name.size[0] or val2 >= type_name.size[1]:
                    print("Index out")
                    return ErrorType()
                return type_name.type
            else:
                print("Wrong types")
                return ErrorType()
        else:
            if type1 == 'int':
                val = node.first_el.value
                if type_name.dimension != 1:
                    print("Error dimension")
                    return ErrorType()
                if val >= type_name.size or val < 0:
                    print("Index out")
                    return ErrorType()
                return type_name.type
            else:
                print("Error")
                return ErrorType()



    def visit_While(self, node):
        self.loop_entry += 1
        self.symbol_table.pushScope('while')
        self.visit(node.condition)
        self.visit(node.while_body)
        self.symbol_table.popScope()
        self.loop_entry -= 1

    def visit_For(self, node):
        self.loop_entry += 1
        self.symbol_table.pushScope('for')
        type1 = self.visit(node.range)
        self.symbol_table.put(node.iter, type1)
        self.visit(node.for_body)
        self.symbol_table = self.symbol_table.popScope()
        self.loop_entry -= 1

    def visit_Range(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        if not isinstance(type1, int):
            print("Error in type of left el")
            return ErrorType()
        if not isinstance(type1, int):
            print("Error in type of right el")
            return ErrorType()
        return type2


    def visit_LoopFunction(self, node):
        if self.loop_entry <= 0:
            print("Error. Break or Continue outside the loop")

