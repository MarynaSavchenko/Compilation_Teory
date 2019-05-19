import sys
import ply.yacc as yacc
import parser
from TreePrinter import TreePrinter


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/example1.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Mparser = parser.parser
    text = file.read()
    lexer = parser.scanner.lexer
    ast = Mparser.parse(text, lexer=lexer)
    ast.printTree()