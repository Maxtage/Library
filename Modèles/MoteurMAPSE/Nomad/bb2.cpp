#include <cmath>
#include <iostream>
#include <fstream>
#include <cstdlib>
using namespace std;

//Fichier d'optim du modèle "retourné" fonctionnel à utiliser avec param2.txt

//e=x[0], Jcu=x[1], la=x[2], L=x[3], beta=x[4]

const double Gamma=10, kr=0.7, P=0.9, Bi=1.5, Ech=1e+11, Deltap=0.1, rho=0.018e-6, epsilon=0.01, em=0.001, p=10;
const double Vu = 2.4991*1e-4, Va = 0.275*1e-4, Pj = 12.2349;

int main ( int argc , char ** argv) {

	double f = 1e20, c1 = 1e20, c2=1e20, c3=1e20, D=1e20, E=1e20, Be=1e20, C=1e20, Kf=1e20, lambda=1e20;
	double x[5];

	if ( argc >= 2 ) {
		ifstream in (argv[1]);
		for ( int i = 0 ; i < 5 ; i++) {
			in >> x[i];
		}
		D=Deltap*p/M_PI;
		E=Ech/(kr*pow(x[1]*1e7,2));
		Be=2*x[2]*P/(D*log((D+2*E)/(D-2*(x[2]+x[0]))));
		C=(M_PI*x[4]*Be*D)/(4*p*Bi);
		Kf=(1.5)*p*x[4]*((x[0]+E)/D);
		lambda=D/x[3];
		c1 = ((M_PI*x[3])/(2*D))*(1-Kf)*sqrt(kr*x[4]*Ech*E)*pow(D,2)*(D+E)*Be;
		
		//f = M_PI*x[3]*(D+E-x[0]-x[2])*(2*C+E+x[0]+x[2]);
		//f = M_PI*x[4]*x[2]*x[3]*(D-2*x[0]-x[2]);	
		//f = M_PI*rho*x[3]*(D+E)*Ech;
		f = (M_PI*x[3]*(D+E-x[0]-x[2])*(2*C+E+x[0]+x[2]))/Vu + M_PI*x[4]*x[2]*x[3]*(D-2*x[0]-x[2])/Va + M_PI*rho*x[3]*(D+E)*Ech/Pj;
		
		if ( in.fail() )
			f=c1=c2=c3=1e20;
		else {
			c3 = c1 - (Gamma + epsilon);
			c1 = Gamma - c1;
			c2 = 0.3 - Kf;
		}
		in.close();
	}
	cout << f << " " << c1 << " " << c2 << " " << c3 << " " << D << " " << E << " " << Be << " " << C << " " << lambda << endl;
	return 0;
}