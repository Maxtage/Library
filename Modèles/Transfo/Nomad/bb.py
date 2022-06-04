import math
import sympy

eisol=1e-3
freq=50
fp=0.8
h=10
mvc=8800
mvi=7800
q=1
Text=40
V1=230
V2=24
alpha=3.8*1e-3
lambd=0.15
mu0=4*math.pi*1e-7
rho=1.72*1e-8
phi=math.sin(math.acos(fp))

def bb(x): #x[0]=a x[1]=b x[2]=c x[3]=d x[4]=I2 x[5]=n1 x[6]=s1 x[7]=s2
    x[5]=math.floor(x[5])
    Bm = (V1*math.sqrt(2))/(4*math.pi*x[5]*x[0]*x[3]*freq)
    Bmm = (1/((2.12*1e-4)+(((1-2.12*1e-4)*pow(Bm,2*7.358))/(pow(Bm,2*7.358)+1.18*1e6))))
    Lmu = pow(mu0*Bmm*x[0]*x[3]*x[5],2)/(2*x[0]+x[1]+x[2])
    l1 = 2*(x[3]+2*x[0])+math.pi*x[2]*(1/2)
    l2 = 2*(x[3]+2*x[0])+math.pi*x[2]*(3/2)   
    Sca = x[1]*(4*x[0]+2*math.pi*x[2])
    Sia = 4*x[0]*(x[1]+4*x[0]+2*x[2])+2*x[3]*(6*x[0]+2*x[2]+x[1])
    Ria = 1/(h*Sia)
    Rca = 1/(h*Sca) 
    Rcond = eisol/(lambd*x[1]*(4*x[0]+2*x[3])) 
    Mi = mvi*4*x[0]*x[3]*(2*x[0]+x[1]+x[2])
    Pi = q*Mi*(freq/50)*pow(Bm,2)
    X2, Q1, DV2, r1, r2, Tc, Ti, Pj, R2 = sympy.symbols('X2, Q1, DV2, r1, r2, Tc, Ti, Pj, R2', positive=True, real=True)
    n2 = sympy.symbols('n2', positive=True, integer=True)
    EqX2 = X2 - (mu0*pow(n2,2)*x[2]*(4*x[0]+2*x[3]+math.pi*x[2])*2*math.pi*freq/(3*x[1]))
    EqQ1 = Q1 - (pow(V1,2)/(Lmu*2*math.pi*freq)+X2*pow(x[4],2)+V2*x[4]*phi)
    EqDV2 = DV2 - (x[4]*(R2*fp+X2*phi))
    Eqr1 = r1 - (rho*(1+alpha*Tc)*x[5]*l1/(x[6]*1e-6))
    Eqr2 = r2 - (rho*(1+alpha*Tc)*n2*l2/(x[7]*1e-6))
    EqTc = Tc - (Text + Rca*(Rcond*Pj+Ria*(Pj+Pi))/(Rca+Ria+Rcond))
    EqTi = Ti - (Text + Ria*(Rca*Pj+(Rca+Rcond)*Pi)/(Rca+Ria+Rcond))
    EqPj = Pj - (R2*pow(x[4],2))
    EqR2 = R2 - (r2 + r1*pow(n2/x[5],2))
    Eqn2 = n2 - (math.floor(x[5]*(V2+DV2)/V1))
    sols = list(sympy.nonlinearsolve([EqX2,EqQ1,EqDV2,Eqr1,Eqr2,EqTc,EqTi,EqPj,EqR2,Eqn2], [X2, Q1, DV2, n2, r1, r2, Tc, Ti, Pj, R2]))
    if (len(sols)==0):
        X2=1e20
        Q1=1e20
        DV2=1e20
        n2=1e20
        r1=1e20
        r2=1e20
        Tc=1e20
        Ti=1e20
        Pj=1e20
        R2=1e20
    else:
        X2=sols[0][0]
        Q1=sols[0][1]
        DV2=sols[0][2]
        n2=sols[0][3]
        r1=sols[0][4]
        r2=sols[0][5]
        Tc=sols[0][6]
        Ti=sols[0][7]
        Pj=sols[0][8]
        R2=sols[0][9]
    Mc = mvc*(x[5]*x[6]*1e-6*l1+n2*x[7]*1e-6*l2)
    f = Mi + Mc
    f1 = (2*x[5]*x[6]*1e-6)/(x[1]*x[2])
    f2 = (2*n2*x[7]*1e-6)/(x[1]*x[2])
    P1 = Pj + Pi + V2*x[4]*fp
    I1 = math.sqrt(pow(P1,2)+pow(Q1,2))/V1
    I10 = math.sqrt(pow(P1/V1,2)+pow(V1/(Lmu*2*math.pi*freq),2))
    eta = (V2*x[4]*fp)/(V2*x[4]*fp+Pi+Pj)
    c1 = Tc - 120;
    c2 = Ti - 100;
    c3 = eta - 1;
    c4 = 0.8 - eta;
    c5 = (DV2/V2) - 0.1;
    c6 = (I10/I1) - 0.1;
    c7 = f - 2.6;
    c8 = f1 - 0.5;
    c9 = f2 - 0.5;
    out=[f,c1,c2,c3,c4,c5,c6,c7,c8,c9]
#    out2=""
#    for i in out:
#        out=out+str(i)+" "
#    print(out)
    return out


