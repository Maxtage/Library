#include <cmath>
#include <iostream>
#include <fstream>
#include <cstdlib>
using namespace std;
// x[0]=a, x[1]=b x[2]=c x[3]=n x[4]=delta
const double mv=8800, rho=1.724*1e-8;

int main ( int argc , char ** argv ) {
	//déclaration des variables
	double f=1e20, c1=1e20, c2=1e20, c3=1e20, c4=1e20, c5=1e20, I=1e20, L=1e20, Pj=1e20, W=1e20;
	double x[5];
	if ( argc >= 2) {
		ifstream in (argv[1]);
		for ( int i = 0 ; i < 5 ; i++) {
			in >> x[i];
		}
		x[3]=floor(x[3]*1e3);
		L=(50.8*1e-9*pow(x[0],2)*pow(x[3],2))/(3*x[0]+9*x[1]+10*x[2]);
		Pj=rho*pow(x[4]*1e5,2)*M_PI*x[0]*x[1]*x[2];
		I=x[3]*(x[1]*x[2])/x[3];
		W=0.5*L*pow(I,2);
		f=mv*M_PI*x[0]*x[1]*x[2];
		if (in.fail() )
			f = 1e20;
		else {
			c1 = 20 - f;
			c2 = f - 100;
			c3 = 70 - Pj;
			c4 = Pj - 90;
			c5 = 1e-3 - L;
		}
		in.close();
	}
	cout << f << " " << c1 << " " << c2 << " " << c3 << " " << c4 << " " << c5 << " " << I << " " << L << " " << Pj << " " << W << endl;
	return 0;
}