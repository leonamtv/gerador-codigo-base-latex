clc;
clear;
x = [0:0.1:10];
y = (exp((-0.5).*x).*sin(10.*x));
plot(x, y);
title("exp((-0.5)*x)*sin(10*x)");
ylabel("y");
xlabel("x");