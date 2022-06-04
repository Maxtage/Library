import math
import sys
from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D 

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
    Bm = (V1*math.sqrt(2))/(4*math.pi*n1*a*d*freq)
    Bmm = (1/((2.12*1e-4)+(((1-2.12*1e-4)*pow(Bm,2*7.358))/(pow(Bm,2*7.358)+1.18*1e6))))
    Lmu = mu0*Bmm*a*d*pow(n1,2)/(2*a+b+c)
    l1 = 2*(d+2*a)+math.pi*c*(1/2)
    l2 = 2*(d+2*a)+math.pi*c*(3/2)   
    Mi = mvi*4*a*d*(2*a+b+c)
    Pi = q*Mi*(freq/50)*pow(Bm,2)
    Rcond = eisol/(lambd*b*(4*a+2*d)) 
    Sca = b*(4*a+2*math.pi*c)
    Sia = 4*a*(b+4*a+2*c)+2*d*(6*a+2*c+b)
    Ria = 1/(h*Sia)
    Rca = 1/(h*Sca) 
    
    #♣On résout le système d'équations liées
    
    x0 = [(mu0*pow((n1*((V2+1)/V1)),2)*c*(4*a+2*d+math.pi*c)*2*math.pi*freq/(3*b)),(rho*(1+alpha*100)*n1*l1/(s1))+pow((V2+1)/V1,2)*(rho*(1+alpha*100)*n1*((V2+1)/V1)*l2/(s2))]
    
    def fun(y):
        
        X2,R2 = y
        
        EqX2 = X2 - (mu0*pow((n1*(V2+(I2*(R2*fp+X2*phi)))/V1),2)*c*(4*a+2*d+math.pi*c)*2*math.pi*freq/(3*b))
        EqR2 = R2 - rho*(1+alpha*(Text + Rca*(Rcond*R2*pow(I2,2)+Ria*(R2*pow(I2,2)+Pi))/(Rca+Ria+Rcond)))*((V2+(I2*(R2*fp+X2*phi)))/V1)*n1*((l2/s2)+(l1/s1)*((V2+(I2*(R2*fp+X2*phi)))/V1))
        
        return [EqX2,EqR2]
    
    [X2,R2],infodict,ier,mesg = optimize.fsolve(fun,x0,full_output=True)
    
    if ier!=1 :
        
        [X2,R2],infodict,ier,mesg = optimize.broyden1(fun,x0,full_output=True)
        
        if ier!=1 :
            
            [X2,R2],infodict,ier,mesg = optimize.broyden2(fun,x0,full_output=True)
            
            if ier!=1 :
                
                [X2,R2],infodict,ier,mesg = optimize.broyden3(fun,x0,full_output=True)
            
                if ier!=1 :
                    
                    [X2,R2],infodict,ier,mesg = optimize.broyden_generalized(fun,x0,full_output=True)
            
                    if ier!=1 :
                 
                        [X2,R2],infodict,ier,mesg = optimize.newton_krylov(fun,x0,full_output=True)
                 
                        if ier!=1 :
                     
                            [X2,R2],infodict,ier,mesg = optimize.anderson(fun,x0,full_output=True)
                     
                            if ier !=1 :
                                
                                [X2,R2],infodict,ier,mesg = optimize.anderson2(fun,x0,full_output=True)
                     
                                if ier !=1 :
                         
                                    print()
                                    
    #On trace la surface de la fonction fun
    
    def Plotteur(f,xmax,precx,ymax,precy) :
        
        X = np.arange(-1,xmax,precx)
        Y = np.arange(-1,ymax,precy)
        
        nX = len(X)
        nY = len(Y)
        nf = len(f([0,0]))
    
        xx = np.zeros([nX,nY],dtype='d')
        yy = np.zeros([nX,nY],dtype='d')
        zz=[]
        
        for k in range (nf):
            
            zz.append((np.zeros([nX,nY],dtype='d')))
        
        fig = plt.figure(figsize=(6,6))
        ax = Axes3D(fig)
        
        for i in range(nX):
            for j in range(nY):
                xx[i,j] = X[i]
                yy[i,j] = Y[j]
                xp = xx.flatten()
                yp = yy.flatten()
                
        for k in range(nf): 
            for i in range(nX):
                for j in range(nY):
    
                    zz[k][i,j] = f([xx[i,j],yy[i,j]])[k]
                
                zp = zz[k].flatten()
                ax.plot_trisurf(xp, yp, zp, cmap=cm.jet, linewidth=0,antialiased=False)
        
        ax.set_title(r'trisurf example',fontsize=16, color='k')
        ax.view_init(45, 45)
        plt.tight_layout()
        plt.show()
    
    #Plotteur(fun, 0.1, 1e-3, 1e-4, 1e-6)
    
    #On déduit les reste des variables causales
    Pj = (R2*pow(I2,2))
    Tc = (Text + Rca*(Rcond*Pj+Ria*(Pj+Pi))/(Rca+Ria+Rcond))
    Ti = (Text + Ria*(Rca*Pj+(Rca+Rcond)*Pi)/(Rca+Ria+Rcond))
    DV2 = (I2*(R2*fp+X2*phi))
    n2 = ((n1*(V2+DV2)/V1))
    Mc = mvc*(n1*s1*1e-6*l1+n2*s2*1e-6*l2)
    f = Mi + Mc
    f1 = (2*n1*s1*1e-6)/(b*c)
    f2 = (2*n2*s2*1e-6)/(b*c)
    P1 = Pj + Pi + V2*I2*fp
    I1 = math.sqrt(pow(P1,2)+pow((pow(V1,2)/(Lmu*2*math.pi*freq)+X2*pow(I2,2)+V2*I2*phi),2))/V1
    I10 = math.sqrt(pow(P1/V1,2)+pow(V1/(Lmu*2*math.pi*freq),2))
    eta = (V2*d*fp)/(V2*d*fp+Pi+Pj)
    
    #On crée les contraintes de sortie
    c1 = Tc - 120
    c2 = Ti - 100
    c3 = 0.8 - eta
    c4 = (DV2/V2) - 0.10
    c5 = (I10/I1) - 0.10
    c6 = f1 + f2 - 1
    #c7 = 2.6 - f

    #on affiche la sortie pour l'execution
    #print(f)
    print(f,c1,c2,c3,c4,c5,c6)
bb()