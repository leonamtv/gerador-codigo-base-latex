clc;
clear;
t = [0:0.5:4*pi];
x = sin(t);
y = cos(t);
plot(t,x, "-*", "color", "b");
hold on;
plot(t,y, "-o", "color", "r");
grid on;
title("Grafico das funcoes sen(t) e cos(t)");
ylabel("funcoes(t)");
xlabel("Tempo(s)");
legend("sen(t)", "cos(t)")