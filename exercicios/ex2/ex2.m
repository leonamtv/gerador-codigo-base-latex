clc;
clear;
pkg load control;
printf("Letra a\n");
a = zpk([ -2 -4 ], [ 0 -3 -5 ], 10)
printf("Letra b\n");
b = zpk([ -2 -4 ], [ 1 2 3 ], 1)
printf("Letra c\n");
c = zpk([ -2 -4 ], [ -7 -8 -9 ], 20)