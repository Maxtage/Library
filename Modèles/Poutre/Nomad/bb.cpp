#include <cmath>
#include <iostream>
#include <fstream>
#include <cstdlib>
using namespace std;
//déclaration des constantes

const double E=2*1e11, L=4, P=1e4, rho=7800;

int main ( int argc , char ** argv ) {
	
	//déclaration des variables
	
	double x[4];
	double S=1e20, f=1e20, c1=1e20, Ix=1e20, Iy=1e20, I=1e20, sigma=1e20, w=1e20;
	
	if ( argc >= 2) {
		ifstream in (argv[1]);
		for ( int i = 0 ; i < 4 ; i++) {
			in >> x[i];
		}
		S=x[1]*x[0]-(x[0]-2*x[3])*(x[1]-x[2]);
		f=L*S*rho;
		Ix=(pow(x[0]-2*x[3],3)*x[2]+2*pow(x[3],3)*x[1]+6*x[3]*x[1]*pow(x[0]-x[3],2))/12;
		Iy=((2*x[3]*pow(x[1],3))+(x[1]-2*x[4])*pow(x[2],3))/12;
		I=Ix+Iy;
		sigma=P*L*(x[0]/2)/(4*I);
		w=(P*pow(L,3))/(48*E*I);
		if (in.fail() )
			f = 1e20;
		else {
			c1 = sigma - 12.8*1e6;
		}
		in.close();
	}
	cout << f << " " << c1 << " " << S << " " << w << " " << I << endl;
	return 0;
}