clc;
clear;
pkg load control;
pkg load signal;
printf("Letra a\n");
[ z, p, k ] = tf2zp([ 10 ], [ 1 2 5 ])
zpk(z, p, k)
printf("Letra b\n");
[ z, p, k ] = tf2zp([ 1 3 ], [ 1 5 0 1 ]) 
zpk(z, p, k)
printf("Letra c\n");
[ z, p, k ] = tf2zp([ 6 0 1 ], [ 1 3 3 1 ])
zpk(z, p, k)