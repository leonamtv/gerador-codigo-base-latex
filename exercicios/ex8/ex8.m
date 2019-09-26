clc;
clear;

pkg load control;
pkg load signal;

g1 = tf([ 1 ], [ 500 0 0 ]);
g2 = tf([ 1 1 ], [ 1 2 ]);

g3 = series(g1, g2)

g3 = parallel(g1, g2)

g3 = feedback(g1, g2)