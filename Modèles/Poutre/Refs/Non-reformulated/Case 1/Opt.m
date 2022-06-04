%% Problem Definition

clear all;
close all;
clc;

format long;

% Objective Function
fun = @(x) ibeam_nrf(x);

% Constraints
nlcon = @(x) ibeam_nrf_con(x);
nlrhs = [];
nle = []; %Constraint type: -1 <=, 0 ==, 1 >=

% Bounds, In. vector = [a;b;c;delta;n]
lb = [0.10;0.10;0.01;0.01];
ub = [0.80;0.60;0.05;0.05];

%Constraint types, C for continuous, I for integer, B for binary
xtype = 'CCCC';

% Initial Guess
x0 = [0.30;0.20;0.015;0.015];

%% NOMAD

% Further Info.:
% checkSolver('NLP');
% checkSolver('config');
% checkSolver('nomad');

% When using nomad solver, it ALWAYS considers nlcon<=nlrhs!

% Options
opts = optiset('solver','nomad','display','iter');

% Options for plotting purposes
%opts = optiset('solver','nomad','display','iter','iterfun',@optiplotfval);

% Create OPTI Object
Opt = opti('fun',fun,'bounds',lb,ub,'nlmix',nlcon,nlrhs,nle,'xtype',xtype,'options',opts);

% Solve the problem
[x,fval,exitflag,info] = solve(Opt,x0)

% Checking the Solution
[ok,msg] = checkSol(Opt)

% All IOs (Only used for the purpose of displaying IOs in the Command Window of Matlab)
[y] = ibeam_nrf_out(x);
ibeam_nrf_out_display;

%% SCIP

% Further Info.:
% checkSolver('NLP');
% checkSolver('config');
% checkSolver('scip');

% Options
opts = optiset('solver','scip','display','iter');

% Plotting not supported
% opts = optiset('solver','scip','display','iter','iterfun',@optiplotfval);

% Create OPTI Object
%Opt = opti('fun',fun,'bounds',lb,ub,'nlmix',nlcon,nlrhs,nle,'xtype',xtype,'options',opts);
Opt = opti('fun',fun,'bounds',lb,ub,'xtype',xtype,'options',opts);

% Solve the problem
[x,fval,exitflag,info] = solve(Opt,x0)

% Checking the Solution
[ok,msg] = checkSol(Opt)

% All IOs (Only used for the purpose of displaying IOs in the Command Window of Matlab)
[y] = ibeam_nrf_out(x);
ibeam_nrf_out_display;

%% NLOPT(Algorithm: ISRES)

% Further Info.:
% checkSolver('NLP');
% checkSolver('config');
% checkSolver('nlopt');

% Options
opts = optiset('solver','nlopt','solverOpts',nloptset('algorithm','GN_ISRES'),'display','iter');

% Options for plotting purposes
%opts = optiset('solver','nlopt','solverOpts',nloptset('algorithm','GN_ISRES'),'display','iter','iterfun',@optiplotfval);

% Create OPTI Object
%Opt = opti('fun',fun,'bounds',lb,ub,'nlmix',nlcon,nlrhs,nle,'xtype',xtype,'options',opts);
Opt = opti('fun',fun,'bounds',lb,ub,'xtype',xtype,'options',opts);

% Solve the problem
[x,fval,exitflag,info] = solve(Opt,x0)

% Checking the Solution
[ok,msg] = checkSol(Opt)

% All IOs (Only used for the purpose of displaying IOs in the Command Window of Matlab)
[y] = ibeam_nrf_out(x);
ibeam_nrf_out_display;

%% GMatlab(Algorithm: PATTERNSERACH - Global Direct Search)

% Further Info.:
% checkSolver('NLP');
% checkSolver('config');
% checkSolver('gmatlab');

% Options
opts = optiset('solver','gmatlab','display','iter');

% Options for plotting purposes
% opts = optiset('solver','gmatlab','display','iter','iterfun',@optiplotfval);

% Create OPTI Object
Opt = opti('fun',fun,'bounds',lb,ub,'nlmix',nlcon,nlrhs,nle,'xtype',xtype,'options',opts);

% Solve the problem
[x,fval,exitflag,info] = solve(Opt,x0)

% Checking the Solution
[ok,msg] = checkSol(Opt)

% All IOs (Only used for the purpose of displaying IOs in the Command Window of Matlab)
[y] = ibeam_nrf_out(x);
ibeam_nrf_out_display;

%% BARON

% Further Info.:
% checkSolver('NLP');
% checkSolver('config');
% checkSolver('baron');

% Options
opts = optiset('solver','baron','display','iter');

% Plotting not supported
% opts = optiset('solver','baron','display','iter','iterfun',@optiplotfval);

% Create OPTI Object
%Opt = opti('fun',fun,'bounds',lb,ub,'nlmix',nlcon,nlrhs,nle,'xtype',xtype,'options',opts);
Opt = opti('fun',fun,'bounds',lb,ub,'xtype',xtype,'options',opts);

% Solve the problem
[x,fval,exitflag,info] = solve(Opt,x0)

% Checking the Solution
[ok,msg] = checkSol(Opt)

% All IOs (Only used for the purpose of displaying IOs in the Command Window of Matlab)
[y] = ibeam_nrf_out(x);
ibeam_nrf_out_display;

%% NLOPT(Algorithm: AUGLAG with LN_PRAXIS)

% Further Info.:
% checkSolver('NLP');
% checkSolver('config');
% checkSolver('nlopt');

% Options
opts = optiset('solver','nlopt','solverOpts',nloptset('algorithm','AUGLAG'),'display','iter');

% Options for plotting purposes
%opts = optiset('solver','nlopt','solverOpts',nloptset('algorithm','AUGLAG'),'display','iter','iterfun',@optiplotfval);

% Create OPTI Object
Opt = opti('fun',fun,'bounds',lb,ub,'nlmix',nlcon,nlrhs,nle,'xtype',xtype,'options',opts);

% Solve the problem
[x,fval,exitflag,info] = solve(Opt,x0)

% Checking the Solution
[ok,msg] = checkSol(Opt)

% All IOs (Only used for the purpose of displaying IOs in the Command Window of Matlab)
[y] = ibeam_nrf_out(x);
ibeam_nrf_out_display;
