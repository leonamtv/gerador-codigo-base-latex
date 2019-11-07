clc;
clear;

data = [28 27 25 24 23 22 21 20 19 18 17 16 16 15 15 16 17 20 ...
        22 24 25 27 28 29 29 27 25 24 22 21 21 20 19 18 18 17 ...
        17 17 17 18 19 20 21 23 25 27 29 30 29 28 26 24 23 22 ...
        21 20 20];

% Letra a
figure();
plot(data);
title('Dados puros plotados');
grid on;
grid minor;

% Letra b
figure();
autocorr(data);
title('Autocorrelação');

% Letra c
ident = data(1:48);
valid = data(49:57);

% Letra d
sys_1 = arx(ident', 1);
sys_2 = arx(ident', 2);
sys_3 = arx(ident', 3);
sys_4 = arx(ident', 4);

fprintf('---------------------------------------------------------------------------------\n');
fprintf('Sistema ARX de primeira ordem: \n');
display(sys_1);
fprintf('Sistema ARX de segunda ordem: \n');
display(sys_2);
fprintf('Sistema ARX de terceira ordem: \n');
display(sys_3);
fprintf('Sistema ARX de quarta ordem: \n');
display(sys_4);

% Letra e: parâmetros
params_sys_1 = sys_1.Report.Parameters.ParVector;
params_sys_2 = sys_2.Report.Parameters.ParVector;
params_sys_3 = sys_3.Report.Parameters.ParVector;
params_sys_4 = sys_4.Report.Parameters.ParVector;

fprintf('---------------------------------------------------------------------------------\n');
fprintf('Parâmetros do sistema ARX de primeira ordem: \n');
disp(params_sys_1');
fprintf('Parâmetros do sistema ARX de segunda ordem: \n');
disp(params_sys_2');
fprintf('Parâmetros do sistema ARX de terceira ordem: \n');
disp(params_sys_3');
fprintf('Parâmetros do sistema ARX de quarta ordem: \n');
disp(params_sys_4');

% Letra e: simulação do modelo
y_ident_sys_1 = predict(sys_1, ident');
y_ident_sys_2 = predict(sys_2, ident');
y_ident_sys_3 = predict(sys_3, ident');
y_ident_sys_4 = predict(sys_4, ident');

% Letra f:
figure();
plot(y_ident_sys_1, '--b');
hold on;
plot(y_ident_sys_2, '--g');
hold on;
plot(y_ident_sys_3, '--m');
hold on;
plot(y_ident_sys_4, '--k');
hold on;
plot(ident, 'r');
title('Dados de identificação previstos e reais');
grid on;
grid minor;
legend('ARX ordem 1', 'ARX ordem 2', ...
       'ARX ordem 3', 'ARX ordem 4', ...
       'Dados Reais');
   
% Letra g: 
fprintf('---------------------------------------------------------------------------------\n');
fprintf('Letra g: O sistema mais próximo dos dados reais foi o sistema ARX de quarta ordem.\n\n');

% Letra h: obtendo simulações dos valores
y_valid_sys_1 = predict(sys_1, valid');
y_valid_sys_2 = predict(sys_2, valid');
y_valid_sys_3 = predict(sys_3, valid');
y_valid_sys_4 = predict(sys_4, valid');

% Letra i:
figure();
plot(y_valid_sys_1, '--b');
hold on;
plot(y_valid_sys_2, '--g');
hold on;
plot(y_valid_sys_3, '--m');
hold on;
plot(y_valid_sys_4, '--k');
hold on;
plot(valid, 'r');
title('Dados de validação previstos e reais');
grid on;
grid minor;
legend('ARX ordem 1', 'ARX ordem 2', ...
       'ARX ordem 3', 'ARX ordem 4', ...
       'Dados Reais');

% Letra j:
fprintf('---------------------------------------------------------------------------------\n');
fprintf(['Letra j: Assim como na letra (g), o sistema mais próximo dos dados reais foi o \n', ...
         'sistema ARX de quarta ordem.\n\nAparentemente, por mais que alguns casos outros', ...
         'modelos representam os dados reais \nde forma mais apurada, como o sistema ARX de', ...
         'primeira ordem por exemplo, a curva \nestá deslocada em relação aos dados reais, ', ...
         'deixando assim o sistema de quarta ordem \nvisualmente mais próximo dos dados reais.\n\n']);
     
% Letra k:
RMSE_erro_sys_1 = sqrt(mean((valid - y_valid_sys_1').^2));
RMSE_erro_sys_2 = sqrt(mean((valid - y_valid_sys_2').^2));
RMSE_erro_sys_3 = sqrt(mean((valid - y_valid_sys_3').^2));
RMSE_erro_sys_4 = sqrt(mean((valid - y_valid_sys_4').^2));

fprintf('---------------------------------------------------------------------------------\n');
fprintf(['Erro RMSE do sistema de primeira ordem: %f\n' ...
         'Erro RMSE do sistema de segunda ordem.: %f\n' ...
         'Erro RMSE do sistema de terceira ordem: %f\n' ...
         'Erro RMSE do sistema de quarta ordem..: %f\n\n'], ...
         RMSE_erro_sys_1, RMSE_erro_sys_2, RMSE_erro_sys_3, ...
         RMSE_erro_sys_4);
     
MAPE_erro_sys_1 = (sum((abs(y_valid_sys_1' - valid))/valid)/(max(size(valid)))) * 100;
MAPE_erro_sys_2 = (sum((abs(y_valid_sys_2' - valid))/valid)/(max(size(valid)))) * 100;
MAPE_erro_sys_3 = (sum((abs(y_valid_sys_3' - valid))/valid)/(max(size(valid)))) * 100;
MAPE_erro_sys_4 = (sum((abs(y_valid_sys_4' - valid))/valid)/(max(size(valid)))) * 100;

fprintf('---------------------------------------------------------------------------------\n');
fprintf(['Erro MAPE do sistema de primeira ordem: %f\n' ...
         'Erro MAPE do sistema de segunda ordem.: %f\n' ...
         'Erro MAPE do sistema de terceira ordem: %f\n' ...
         'Erro MAPE do sistema de quarta ordem..: %f\n'], ...
         MAPE_erro_sys_1, MAPE_erro_sys_2, MAPE_erro_sys_3, ...
         MAPE_erro_sys_4);

clear;