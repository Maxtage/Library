#include <cmath>
#include <iostream>
#include <fstream>
#include <cstdlib>
using namespace std;
#include <python2.7/Python.h>

int main (int argc, char *argv[]) {
	
	PyObject* pName = PyUnicode_FromString((char*)"script");
	
	PyObject* pModule = PyImport_Import(pName);
	
	PyObject* pFunc = PyObject_GetAttrString(pModule, (char*)"test");
	
	PyObject* pArgs = PyTuple_Pack(2, 10, 5);
	
	PyObject* pValue = PyObject_CallObject(pFunc, pArgs);
	
	auto result = PyFloat_AsString(pValue);
	
	cout << "les resultats sont" << result << endl;
	
return 0;
}