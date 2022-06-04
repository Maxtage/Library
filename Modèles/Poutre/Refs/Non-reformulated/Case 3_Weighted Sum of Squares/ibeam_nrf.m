function [y] = ibeam_nrf(x)

% Input (x1,x2,x3,x4)
x1 = x(1);
x2 = x(2);
x3 = x(3);
x4 = x(4);


% Parameters
L = 4;
P = 1e4;
E = 2e11;
D = 7800;


% Equations
Area = x2*x1-((x1-(2*x4))*(x2-x3));
Ix = ((((x1-(2*x4))^3)*x3)+(2*(x4^3)*x2)+(6*x4*x2*((x1-x4)^2)))/12;
Iy = (2*x4*(x2^3)+(x1-(2*x4))*(x3^3))/12;
I = Ix+Iy;
Y = x1/2;
M = L*Area*D;
sigma_max = (P*L*Y)/(4*Ix);
w_max = (P*(L^3))/(48*E*Ix);


% Output [x1,x2,x3,x4,M,sigma_max,w_max]
y=[0.35*(M^2) + 0.65*(w_max^2)];

end
