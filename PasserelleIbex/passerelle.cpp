#include <iostream>
#include <fstream>
using namespace std;

#include "ibex.h"
using namespace ibex;

ifstream in_config;
string ibex_fname;

int main (int argc, char ** argv)
{
	//declare the obrjective value and the contraints that will be returned
	double goal=1e20;
	
	in_config.open("nomad2ibex.txt", ios::in);
	in_config>>ibex_fname;
	in_config.close();

	//cout<<"Loading model "<<ibex_fname<<endl;

	// Build the system of equations from desired minibex file
	System s(ibex_fname.c_str());
	CtcHC4 hc4(s);
	CtcFixPoint fp(hc4);

	const int N = s.nb_var;
	const int M = s.nb_ctr;

	//cout<<N<<" variables and "<<M<<" constraints"<<endl;

	//declare and array as long as there are variables
	IntervalVector x(N,Interval(goal,goal));
	IntervalVector ctrs(M,Interval(goal,goal));

	bool in_fail=false;
	float prec=2; //consider you have a doubt on the third decimal after the comma in scientific writing
	
	if(argc >= 2 ) {
		ifstream in (argv[1]);
		for ( int i = 0 ; i < N ; i++) {
			double a;
			in >> a;
			//cout<<"x_"<<i<<": "<<a<<" ";
			x[i]=Interval(a,a).inflate(pow(10,int(log10(a))-prec));
		}
		//cout<<endl;
		
		in_fail = in.fail();
		in.close();
		
		//x.inflate(1e-5);
		
		fp.contract(x);
		
		if (!in.fail() && !x.is_empty()) {
			//Affect desired values to goal and constraints
			goal = s.goal->eval(x).ub();
			ctrs = s.f_ctrs.eval_vector(x);
		} 
		in.close();
	}
	cout<<goal<<" ";
	for(int i=0;i<ctrs.size();i++){
        cout<<ctrs[i].mid()<<" ";
	}
	cout<<endl;

	return 0;
}

// g++ passerelle.cpp `pkg-config --cflags ibex` `pkg-config --libs  ibex`  -std=c++11 -o passerelle.exe