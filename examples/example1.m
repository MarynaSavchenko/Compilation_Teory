# special functions, initializations

A = zeros(5);  # create 5x5 matrix filled with zeros
B = ones(5);   # create 7x7 matrix filled with ones
I = eye(5);   # create 10x10 matrix filled with ones on diagonal and zeros elsewhere

I = B .+ I;

# initialize 3x3 matrix with specific values
E1 = [ 1, 2, 3;
       4, 5, 6;
       7, 8, 9 ] ;

E1[2,1] = 7;
C = [1,2,3];
C[2] = 6;
print C;
print E1;
print I;
x = 0;
print x+1;
