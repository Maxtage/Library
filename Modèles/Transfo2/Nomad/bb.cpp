#include <cmath>
#include <iostream>
#include <fstream>
#include <cstdlib>
using namespace std;
//déclaration des constantes

// h=x[0] N1=x[1]

const double D1=0.05, D2=0.05, D3=0.05, D4=0.05, D5=0.05, Bt=1.7, freq=50, F1=0.7, F2=0.7, FI=0.8, J=4500000, Pc=25, Pi=12, pspc=5, pspi=25, St=40000000, U1=60000, rho=2.6*1e-8, rhoc=8900, rhoi=7800, mu=4*M_PI*1e-7;
// const double D1=0.0127, D2=0.127, D3=0.165, D4=0.165, D5=0.063, Bt=1.7, freq=50, F1=0.435, F2=0.597, FI=0.95, J=4000000, Pc=25, Pi=12, pspc=5, pspi=25, St=4*1e7, U1=6*1e4, rho=2.6*1e-8, rhoc=8900, rhoi=7800, mu=4*M_PI*1e-7;

int main ( int argc , char ** argv ) {
	
	//déclaration des variables
	
	double f=1e20, A=1e20, Al=1e20, Dm=1e20, Ff=1e20, G=1e20, Ld=1e20, PC=1e20, PI=1e20, PCc=1e20, PCi=1e20, PSPC=1e20, PSPI=1e20, S=1e20, TC=1e20, TI=1e20, V1=1e20, VC=1e20, VI=1e20, X=1e20, X2=1e20;
	double x[2];
	
	if ( argc >= 2) {
		ifstream in (argv[1]);
		for ( int i = 0 ; i < 2 ; i++) {
			in >> x[i];
		}
		double h=x[0];
		double N1=x[1];
		S=St/3;
		V1=U1/sqrt(3);
		A=(N1*S)/(V1*h*F1*J);
		G=(N1*S)/(V1*h*F2*J);
		Ff=(D2+(A+G)/3)/h;
		Ld=sqrt((2*sqrt(2)*V1)/(pow(M_PI,2)*freq*Bt*N1*FI));
		Dm=Ld+2*D1+2*A+D2;
		X2=mu*pow(M_PI,2)*Dm*pow(N1,2)*2*freq*Ff,
		X=(X2*S)/pow(V1,2);
		Al=M_PI*pow(Ld,2)/4;
		VC=3*M_PI*Dm*h*(A*F1+G*F2);
		VI=Al*FI*(8*(D1+A+D2+G+D5)+6*Ld+3*(h+D4+D3));
		PC=Pc*rhoc*VC;
		PI=Pi*rhoi*VI;
		PCc=rho*VC*pow(J,2);
		PCi=rhoi*VI*(1.996-8.125*Bt+12.277*pow(Bt,2)-7.502*pow(Bt,3)+1.702*pow(Bt,4));
		TC=pspc*PCc;
		TI=pspi*PCi;
		
		f=PC+TC+PI+TI;
		
		if (in.fail() )
			f = 1e20;
		else {
		}
		in.close();
	}
	cout << f << " " << S << " " << V1 << " " << A << " " << G << " " << Ff << " " << Ld << " " << Dm << " " << X2 << " " << X << " " << Al << " " << VC << " " << VI << " " << PC << " " << PI << " " << PCc << " " << PCi << " " << TC << " " << TI << " " << endl;
	return 0;
}