#include <cmath>
#include <iostream>
#include <fstream>
#include <cstdlib>
using namespace std;
//THIS IS JUST AN EXAMPLE
//declaration of constants
const double a=2.5, b=-8, c=7, alpha=0.1, beta=5;
int main ( int argc , char ** argv ) {
	//declaration of variables
	double f = 1e20, c1 = 1e20;
	double x[1];
	if ( argc >= 2) {
		ifstream in (argv[1]);
		for ( int i = 0 ; i < 1 ; i++) {
			in >> x[i];
		}
		f = a*pow(x[0],2)+b*x[0]+c;
		if (in.fail() )
			f = 1e20;
		else {
			c1=f-(alpha*x[0]+beta);
		}
		in.close();
	}
	cout << f << " " << c1 << endl;
	return 0;
}