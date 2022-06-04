#include <cmath>
#include <iostream>
#include <fstream>
#include <cstdlib>
using namespace std;
//THIS IS JUST AN EXAMPLE
//declaration of constants
int main ( int argc , char ** argv ) {
	//declaration of variables
	double f=1e20;
	double x[X];
	if ( argc >= 2) {
		ifstream in (argv[1]);
		for ( int i = 0 ; i < X ; i++) {
			in >> x[i];
		}
		if (in.fail() )
			f = 1e20;
		else {
			c1 = 1;
		}
		in.close();
	}
	cout << f << " " << endl;
	return 0;
}