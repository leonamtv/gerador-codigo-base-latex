clc;
clear;
figure;

pkg load control;
pkg load signal;

a1 = tf([ 10 ], [ 1 2 5 ]);
b1 = tf([ 1 3 ], [ 1 5 1 ]);
c1 = tf([ 6 0 1 ], [ 1 3 3 1 ]);

a2 = zpk([ -2 -4 ], [ 0 -3 -5 ], 10);
b2 = zpk([ -2 -4 ], [ 1 2 3 ], 1);
c2 = zpk([ -2 -4 ], [ -7 -8 -9 ], 20);

a = figure();
step(a1);
print('-dtex', 'plot/plot_1.tex');
b = figure();
step(b1);
print('-dtex', 'plot/plot_2.tex');
c = figure();
step(c1);
print('-dtex', 'plot/plot_3.tex');
d = figure();
step(a2);
print('-dtex', 'plot/plot_4.tex');
e = figure();
step(b2);
print('-dtex', 'plot/plot_5.tex');
f = figure();
step(c2);
print('-dtex', 'plot/plot_6.tex');

pzmap(a1, 'r')
figure;
pzmap(b1, 'r')
figure;
pzmap(c1, 'r')
figure;
pzmap(a2, 'r')
figure;
pzmap(b2, 'r')
figure;
pzmap(c2, 'r')