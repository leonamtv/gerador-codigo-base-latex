clc;
clear;
A = [ 4 2*pi ;  6*j (10+sqrt(2)*j)];
B = [ 6*j -13*pi ; pi 16 ];
fprintf("A+B\n");
A + B
fprintf("AB\n");
A*B
fprintf("A²\n");
A.^2
fprintf("A'\n");
A'
fprintf("B-¹\n");
B.^(-1)
fprintf("B'A'\n");
(B')*(A')
fprintf("A² + B² - AB\n");
A.^2 + B.^2 - A*B