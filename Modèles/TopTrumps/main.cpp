/* 
 * File:   main.cpp
 * Author: volz
 *
 * Created on 20. Juni 2018, 12:18
 */

#include <cstdlib>
#include <fstream>
#include <iostream>
#include "simulation/Game.h"
#include "rw_top_trumps.h"

using namespace std;

/*
 * Prints the value of the middle of the domain for the given problem.
 *
 * Requires arguments: number_of_objectives, function, instance, dimension
 */
int main(int argc, char** argv) {

  if (argc != 5) {
    cout << "Incorrect arguments, expected usage:" << endl;
    cout << "TopTrumpsExec number_of_objectives function instance dimension";
    cout << endl;
    cout << "For example:" << endl;
    cout << "./TopTrumpsExec 1 1 1 88" << endl;
    return 0;
  }

  size_t num_objectives = (size_t) atoi(argv[1]);
  size_t function = (size_t) atoi(argv[2]);
  size_t instance = (size_t) atoi(argv[3]);
  size_t dimension = (size_t) atoi(argv[4]);
  size_t m = 4;

  double *min { new double[m] { } };
  double *max { new double[m] { } };
  double *x { new double[dimension] { } };
  double *y { new double[num_objectives] { } };

  rw_top_trumps_bounds(instance, m, min, max);

  // Set x to be the middle of the domain
  for (size_t i = 0; i < dimension; i++) {
    x[i] = int((max[i % m] + min[i % m]) / 2);
  }

  char *suite_name;
  if (num_objectives == 1)
    suite_name = (char *) "rw-top-trumps";
  else if (num_objectives == 2)
    suite_name = (char *) "rw-top-trumps-biobj";
  else {
    cerr << "Incorrect number of objectives (" << num_objectives
        << ") supported 1 or 2" << endl;
    return -1;
  }

  evaluate_rw_top_trumps(suite_name, num_objectives, function, instance,
      dimension, x, y);

  cout << "x = ";
  for (size_t i = 0; i < dimension; i++) {
    cout << x[i] << " ";
  }
  cout << endl << "y = ";
  for (size_t i = 0; i < num_objectives; i++) {
    cout << y[i] << " ";
  }
  cout << endl;

  delete[] min;
  delete[] max;
  delete[] x;
  delete[] y;
  return 0;
}

