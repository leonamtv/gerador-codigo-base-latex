clc;
clear;

pkg load control;
pkg load signal;

a1 = tf([ 10 ], [ 1 2 5 ]);
b1 = tf([ 1 3 ], [ 1 5 1 ]);
c1 = tf([ 6 0 1 ], [ 1 3 3 1 ]);

a2 = zpk([ -2 -4 ], [ 0 -3 -5 ], 10);
b2 = zpk([ -2 -4 ], [ 1 2 3 ], 1);
c2 = zpk([ -2 -4 ], [ -7 -8 -9 ], 20);

printf("Zeros e polos da 1-a\n");
zeros = zero(a1)
polos = pole(a1)

printf("Zeros e polos da 1-b\n");
zeros = zero(b1)
polos = pole(b1)

printf("Zeros e polos da 1-c\n");
zeros = zero(c1)
polos = pole(c1)

printf("Zeros e polos da 2-a\n");
zeros = zero(a2)
polos = pole(a2)

printf("Zeros e polos da 2-b\n");
zeros = zero(b2)
polos = pole(b2)

printf("Zeros e polos da 2-c\n");
zeros = zero(c2)
polos = pole(c2)