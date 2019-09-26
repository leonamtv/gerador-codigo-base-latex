clc;
clear;
pkg load control;
pkg load signal;
printf("Letra a\n");
[ num, den ] = zp2tf([ -2 -4 ]', [ 0 -3 -5 ]', 10);
a = tf(num, den)
printf("Letra b\n");
[ num, den ] = zp2tf([ -2 -4 ]', [ 1 2 3 ]', 1);
b = tf(num, den)
printf("Letra c\n");
[ num, den ] = zp2tf([ -2 -4 ]', [ -7 -8 -9 ]', 20);
c = tf(num, den)