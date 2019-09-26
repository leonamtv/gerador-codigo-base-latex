clc;
clear;
pkg load control;
printf("Letra a\n");
a = tf([ 10 ], [ 1 2 5 ])
printf("Letra b\n");
b = tf([ 1 3 ], [ 1 5 1 ])
printf("Letra c\n");
c = tf([ 6 0 1 ], [ 1 3 3 1 ])