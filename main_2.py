#!/usr/bin/python
import sys
import parser
import scanner

if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/example1.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)


    parser = parser.parser
    text = file.read()
    parser.parse(text, lexer=scanner.lexer)



