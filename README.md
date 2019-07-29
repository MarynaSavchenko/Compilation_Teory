# Compilation_Theory
1) main - scanner:
Recognize lexems like:  +, -, *, /
                        .+, .-, .*, ./
                        =, +=, -=, *=, /=
                         <, >, <=, >=, !=, ==
                        (,), [,], {,}
                        :
                        '
                        , ;
                        if, else, for, while
                        break, continue oraz return
                        eye, zeros oraz ones
                        print
                        ID (first letter or '_', later possible digits)
                        int, float
                        strings
Return: token with lexem and line number.
Pass: space, tab, new line, comments(#)
2) main_2 - parser:
3) main_3 - create and print AST
4) main_4 - analizer:
Check for errors like:
init matrix with vectors of diifferent sizes
call out of range in matrix
wrong types for bin operations
bin ops on vectors/matrixes of different sizes
usage of functions 'eye', 'zeros', 'ones' with wrong args
wrong usage of 'break' or 'continue'
5) main_5 - interpreter
