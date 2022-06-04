% The portion of code below in only used to display outputs in Command Window of Matlab
syms x1_(m) x2_(m) x3_(m) x4_(m);
Alpha = [x1_(m), x2_(m), x3_(m), x4_(m)];
for i=1:numel(x)
    fprintf('%s = %e \n',char(Alpha(i)) ,x(i));
end
disp ------------------------
syms Mass_(Kg) Stress_Max_(Pa) Deflection_Max_(m);
Beta = [Mass_(Kg), Stress_Max_(Pa), Deflection_Max_(m)];
for i=1:numel(y)
    fprintf('%s = %e \n',char(Beta(i)) ,y(i));
end
