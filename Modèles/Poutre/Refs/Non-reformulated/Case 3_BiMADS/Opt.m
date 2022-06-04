%% Problem Definition

clear all;
close all;
clc;

format long;

% Objective Function
fun = @(x) ibeam_nrf(x);

% Constraints
nlcon = @(x) ibeam_nrf_con(x);
nlrhs = [12.8e6;0];
nle = [-1,1]; %Constraint type: -1 <=, 0 ==, 1 >=

% Bounds, In. vector = [a;b;c;delta;n]
lb = [0.10;0.10;0.01;0.01];
ub = [0.80;0.60;0.05;0.05];

%Constraint types, C for continuous, I for integer, B for binary
xtype = 'CCCC';

% Initial Guess
x0 = [0.30;0.20;0.015;0.015];

%% BiMADS (from whithin the NOMAD package)

% Further Info.:
% checkSolver('NLP');
% checkSolver('config');
% checkSolver('nomad');

opts = nomadset('display_degree',2,'multi_nb_mads_runs',1000000,'bb_output_type',{'PEB' 'PEB'});

[x,fval,ef,iter] = nomad(fun,x0,lb,ub,nlcon,nlrhs,xtype,opts);

%% Displaying Output & Plotting the Pareto Front

% All IOs (Only used for the purpose of displaying IOs in the Command Window of Matlab)
[y] = ibeam_nrf_out(x);
ibeam_nrf_out_display;

% Pareto Front
xlabel('Objective Function 1','fontsize', 9);
ylabel('Objective Function 2','fontsize', 9);
title ('Pareto Front Approximation');
grid off;
hold on;
%xlim([0 2]);
%ylim([0 2]);

for i=1:size(fval,2)
    plot(fval(1,i),fval(2,i),'ro')
end
legend('Bi-MADS','location','NE');

