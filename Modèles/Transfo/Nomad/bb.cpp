#include <cmath>
#include <iostream>
#include <fstream>
#include <cstdlib>
using namespace std;

//déclaration des constantes
const double eisol=1e-3, freq=50, fp=0.8, h=10, mvc=8800, mvi=7800, q=1, Text=40, V1=230, V2=24, alpha=3.8*1e-3, lambda=0.15, mu0=4*M_PI*1e-7, rho=1.72*1e-8, phi=sin(acos(fp));

int main ( int argc , char ** argv ) {
	
	//déclaration des variables
	double f=1e20, c1=1e20, c2=1e20, c3=1e20, c4=1e20, c5=1e20, c6=1e20, c7=1e20, c8=1e20, c9=1e20, eta=1e20, RapI=1e20, RapV=1e20, f1=1e20, f2=1e20, Bm=1e20, l1=1e20, l2=1e20, r1=1e20, r2=1e20, Sca=1e20, Sia=1e20, Rca=1e20, Ria=1e20, Rcond=1e20, R2=1e20, Mc=1e20, Mi=1e20, Lmu=1e20, X2=1e20, Q1=1e20, DV2=1e20, Pi=1e20, Pj=1e20, P1=1e20, I1=1e20, I10=1e20;
	double x[11]; //x[0]=a x[1]=b x[2]=c x[3]=d x[4]=I2 x[5]=n1 x[6]=n2 x[7]=s1 x[8]=s2 x[9]=Tc x[10]=Ti
	
	if ( argc >= 2) {
		ifstream in (argv[1]);
		for ( int i = 0 ; i < 8 ; i++) {
			in >> x[i];
		}
		x[5]=floor(x[5]);
		Bm = (V1*sqrt(2))/(4*M_PI*x[5]*x[0]*x[3]*freq);
		double Bmm = (1/((2.12*1e-4)+(((1-2.12*1e-4)*pow(Bm,2*7.358))/(pow(Bm,2*7.358)+1.18*1e6))));
		l1 = 2*(x[3]+2*x[0])+M_PI*x[2]*(1/2);
		l2 = 2*(x[3]+2*x[0])+M_PI*x[2]*(3/2);
		r1 = rho*(1+alpha*x[9])*x[5]*l1/(x[7]);
		r2 = rho*(1+alpha*x[9])*x[6]*l2/(x[8]);
		Sca = x[1]*(4*x[0]+2*M_PI*x[2]);
		Sia = 4*x[0]*(x[1]+4*x[0]+2*x[2])+2*x[3]*(6*x[0]+2*x[2]+x[1]);
		Ria = 1/(h*Sia);
		Rca = 1/(h*Sca);
		Rcond = eisol/(lambda*x[1]*(4*x[0]+2*x[3]));
		R2 = r2 + r1*pow(x[6]/x[5],2);
		Mc = mvc*(x[5]*x[7]*l1+x[6]*x[8]*l2);
		Mi = mvi*4*x[0]*x[3]*(2*x[0]+x[1]+x[2]);
		f = Mi + Mc;
		f1 = (2*x[5]*x[7])/(x[1]*x[2]);
		f2 = (2*x[6]*x[8])/(x[1]*x[2]);
		Lmu = pow(mu0*Bmm*x[0]*x[3]*x[5],2)/(2*x[0]+x[1]+x[2]);
		X2 = mu0*pow(x[6],2)*x[2]*(4*x[0]+2*x[3]+M_PI*x[2])*2*M_PI*freq/(3*x[1]);
		Q1 = pow(V1,2)/(Lmu*2*M_PI*freq)+X2*pow(x[4],2)+V2*x[4]*phi;
		DV2 = x[4]*(R2*fp+X2*phi);
		RapV = DV2/V2;
		x[6] = floor(x[5]*(V2+DV2)/V1);
		Pi = q*Mi*(freq/50)*pow(Bm,2);
		Pj = R2*pow(x[4],2);
		P1 = Pj + Pi + V2*x[4]*fp;
		I1 = sqrt(pow(P1,2)+pow(Q1,2))/V1;
		I10 = sqrt(pow(P1/V1,2)+pow(V1/(Lmu*2*M_PI*freq),2));
		RapI = I10/I1;
		eta = (V2*x[4]*fp)/(V2*x[4]*fp+Pi+Pj);
		x[9] = Text + Rca*(Rcond*Pj+Ria*(Pj+Pi))/(Rca+Ria+Rcond);
		x[10] = Text + Ria*(Rca*Pj+(Rca+Rcond)*Pi)/(Rca+Ria+Rcond);
		if (in.fail() )
			f=1e20;
			//f = 1e20, c1=1e20, c2=1e20, c3=1e20, c4=1e20, c5=1e20, c6=1e20, c7=1e20, c8=1e20, c9=1e20, Tc=1e20, Ti=1e20, eta=1e20, f1=1e20, f2=1e20, Bm=1e20, l1=1e20, l2=1e20, r1=1e20, r2=1e20, Sca=1e20, Sia=1e20, Rca=1e20, Ria=1e20, Rcond=1e20, R2=1e20, Mc=1e20, Mi=1e20, Lmu=1e20, X2=1e20, Q1=1e20, DV2=1e20, Pi=1e20, Pj=1e20, P1=1e20, I1=1e20, I10=1e20;
		else {
			c1 = x[9] - 120;
			c2 = x[10] - 100;
			c3 = eta - 1;
			c4 = 0.8 - eta;
			c5 = (DV2/V2) - 0.1;
			c6 = (I10/I1) - 0.1;
			c7 = f - 2.6;
			c8 = f1 - 0.5;
			c9 = f2 - 0.5;
		}
		in.close();
	}
	//cout << f << " " << c1 << " " << c2 << " " << c3 << " " << c4 << " " << c5 << " " << c6 << " " << c7 << " " << c8 << " " << c9 << " " << x[4] << endl;
	cout << V2 << " " << DV2 << " " << Mi << " " << Mc << " " << x[10] << " " << x[9] << " " << eta << " " << l1 << " " << l2 << " " << f1 << " " << f2 << endl;
	return 0;
}