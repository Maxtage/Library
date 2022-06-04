import sys
from scipy import optimize
import jax.numpy as jnp
from jax import grad

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
mu0=4*jnp.pi*1e-7
rho=1.72*1e-8
phi=jnp.sin(jnp.acos(fp))

def bb(): #x[0]=a x[1]=b x[2]=c x[3]=d x[4]=I2 x[5]=n1 x[6]=s1 x[7]=s2
   
    #On lit les valeurs de x
    filename = sys.argv[1]
    file = open(filename, 'r')
    x = file.read().split()
    file.close()
    
    dim = len(x)
    x = [float(x[i]) for i in range(dim)]
    a = x[0]
    b = x[1]
    c = x[2]
    d = x[3]
    I2 = x[4]
    n1 = x[5]
    s1 = x[6]
    s2 = x[7]
    
    #on crée les variables causales
    Bm = (V1*jnp.sqrt(2))/(4*jnp.pi*n1*a*d*freq)
    Bmm = (1/((2.12*1e-4)+(((1-2.12*1e-4)*pow(Bm,2*7.358))/(pow(Bm,2*7.358)+1.18*1e6))))
    Lmu = mu0*Bmm*a*d*pow(n1,2)/(2*a+b+c)
    l1 = 2*(d+2*a)+jnp.pi*c*(1/2)
    l2 = 2*(d+2*a)+jnp.pi*c*(3/2)   
    Sca = b*(4*a+2*jnp.pi*c)
    Sia = 4*a*(b+4*a+2*c)+2*d*(6*a+2*c+b)
    Ria = 1/(h*Sia)
    Rca = 1/(h*Sca) 
    Rcond = eisol/(lambd*b*(4*a+2*d)) 
    Mi = mvi*4*a*d*(2*a+b+c)
    Pi = q*Mi*(freq/50)*pow(Bm,2)
    
    #On définit une fonction auxiliaire représentant le système d'équations non causales
    def fun(x):
        X2 = x[0]
        Q1 = x[1]
        DV2 = x[2]
        r1 = x[3]
        r2 = x[4]
        Tc = x[5]
        Ti = x[6]
        Pj = x[7]
        R2 = x[8]
        n2 = x[9]
        
        EqX2 = X2 - (mu0*pow(n2,2)*c*(4*a+2*d+jnp.pi*c)*2*jnp.pi*freq/(3*b))
        EqQ1 = Q1 - (pow(V1,2)/(Lmu*2*jnp.pi*freq)+X2*pow(I2,2)+V2*I2*phi)
        EqDV2 = DV2 - (I2*(R2*fp+X2*phi))
        Eqr1 = r1 - (rho*(1+alpha*Tc)*n1*l1/(s1))
        Eqr2 = r2 - (rho*(1+alpha*Tc)*n2*l2/(s2))
        EqTc = Tc - (Text + Rca*(Rcond*Pj+Ria*(Pj+Pi))/(Rca+Ria+Rcond))
        EqTi = Ti - (Text + Ria*(Rca*Pj+(Rca+Rcond)*Pi)/(Rca+Ria+Rcond))
        EqPj = Pj - (R2*pow(I2,2))
        EqR2 = R2 - (r2 + r1*pow(n2/n1,2))
        Eqn2 = n2 - ((n1*(V2+DV2)/V1))
        return [EqX2,EqQ1,EqDV2,Eqr1,Eqr2,EqTc,EqTi,EqPj,EqR2,Eqn2]
    
    #On résout le système d'équations non causales
    x0=[0,0,0,0,0,0,0,0,0,0]
    sols=optimize.fsolve(fun,x0)
    
    #On récupère les sorties du système, les variables commentées ne sont pas réutilisées
    #X2 = sols[0]
    Q1 = sols[1]
    DV2 = sols[2]
    #r1 = sols[3]
    #r2 = sols[4]
    Tc = sols[5]
    Ti = sols[6]
    Pj = sols[7]
    #R2 = sols[8]
    n2 = sols[9]
    
    #On déduit les reste des variables causales
    Mc = mvc*(n1*s1*1e-6*l1+n2*s2*1e-6*l2)
    f = Mi + Mc
    return(f)

Gradbb=grad(bb)
print(Gradbb([1,1,1,1,1,1,1,1]))