#include <assert.h>
#include <iostream>

#include <stdio.h>
#include <string.h>
#include "rw_top_trumps.h"
#include "simulation/Game.h"
#include "utils/Hoy.h"
#include <algorithm>

using namespace std;

#define LARGE_VALUE 1e10-1

#ifdef __cplusplus
extern "C" {
#endif

size_t m = 4;
int rep = 2000;
int players = 2;

/**
 * The evaluator for problems from the rw_top_trumps suite
 */
void evaluate_rw_top_trumps(char *suite_name, size_t number_of_objectives,
    size_t function, size_t instance, size_t dimension, const double *x,
    double *y) {
  unsigned int seed = (unsigned int) instance;
  srand(seed);
  size_t n = dimension / m;
  vector<double> y_vector(number_of_objectives);
  vector<double> x_vector(dimension);
  bool outOfBounds = false;
  vector<double> min_vector(m);
  vector<double> max_vector(m);
  double maxHyp = 1;
  double maxSD = 0;

  double *min = (double *) malloc(m * sizeof(double));
  double *max = (double *) malloc(m * sizeof(double));
  rw_top_trumps_bounds(instance, m, min, max);

  // Check if out of bounds
  for (size_t i = 0; i < m; i++) {
    min_vector[i] = min[i];
    max_vector[i] = max[i];
    for (size_t j = 0; j < n; j++) {
      x_vector[j * m + i] = x[j * m + i];
      if (x_vector[j * m + i] < min_vector[i] || x_vector[j * m + i] > max_vector[i]) {
        fprintf(stderr, "Out of bounds for instance %lu, ", instance);
        fprintf(stderr, "i = %lu, ", j * m + i);
        fprintf(stderr, "x[%lu] = %f, min[%lu] = %f, max[%lu] = %f\n",
            j * m + i, x_vector[j * m + i], i, min_vector[i], i, max_vector[i]);
        outOfBounds = true;
        break;
      }
    }
  }

  free(min);
  free(max);


  for(std::size_t i=0; i<m; i++){
    maxHyp *= max_vector[i] +1 - min_vector[i];
  }

  vector<double> mean_vector(m);
  double mean=0;
  for(std::size_t i=0; i<m; i++){
    if(i%2==0){
      mean_vector[i] = *std::min_element(min_vector.begin(), min_vector.end());    
    }else{
      mean_vector[i] = *std::max_element(max_vector.begin(), max_vector.end());
    }
    mean += mean_vector[i];
  }


  mean/=m;
  for(std::size_t i=0; i<m; i++){
      maxSD+=(mean_vector[i] - mean)*(mean_vector[i] -mean);
  }

  maxSD/=(m-1);
  maxSD = std::sqrt(maxSD);

  // If out of bounds, return a large value
  if (outOfBounds) {
    for (size_t i = 0; i < number_of_objectives; i++)
      y[i] = LARGE_VALUE;
    return;
  }

  Deck deck(x_vector, (int) n, (int) m, min_vector, max_vector);

  if ((strcmp(suite_name, "rw-top-trumps") == 0) && (number_of_objectives == 1)
      && (function <= 2)) {
    if (function == 1) {
      y_vector[0] = -deck.getHV2() / maxHyp +1;
    } else if (function == 2) {
      y_vector[0] = -deck.getSD() / maxSD +1;
    }
  } else if ((strcmp(suite_name, "rw-top-trumps-biobj") == 0)
      && (number_of_objectives == 2) && (function <= 1)) {
    if (function == 1) {
      y_vector[0] = -deck.getHV2() / maxHyp +1;
      y_vector[1] = -deck.getSD() / maxSD +1;
    }
  } else {
    vector<Agent> agents((size_t) players);
    vector<int> playerLevel1(4, 0);
    agents[0] = Agent(playerLevel1, deck);
    vector<int> playerLevel2(4, 1);
    agents[1] = Agent(playerLevel2, deck);

    Game game(deck, players, agents, (int) seed);
    Outcome out(rep);
    for (int i = 0; i < rep; i++) {
      out = game.run(out, 0);
    }

    if ((strcmp(suite_name, "rw-top-trumps") == 0)
        && (number_of_objectives == 1)) {
      if (function == 3) {
        y_vector[0] = -out.getFairAgg() +1;
      } else if (function == 4) {
        y_vector[0] = -players * out.getLeadChangeAgg() / n +1;
      } else if (function == 5) {
        y_vector[0] = out.getTrickDiffAgg()/n;
      } else {
        fprintf(stderr,
            "evaluate_rw_top_trumps(): suite %s does not have function %lu",
            suite_name, function);
        exit(EXIT_FAILURE);
      }
    } else if ((strcmp(suite_name, "rw-top-trumps-biobj") == 0)
        && (number_of_objectives == 2)) {
      if (function == 2) {
        y_vector[0] = -out.getFairAgg() +1;
        y_vector[1] = -players * out.getLeadChangeAgg() / n +1;
      } else if (function == 3) {
        y_vector[0] = -out.getFairAgg()+1;
        y_vector[1] = out.getTrickDiffAgg()/n;
      } else {
        fprintf(stderr,
            "evaluate_rw_top_trumps(): suite %s does not have function %lu",
            suite_name, function);
        exit(EXIT_FAILURE);
      }
    } else {
      fprintf(stderr,
          "evaluate_rw_top_trumps(): suite %s cannot have %lu objectives",
          suite_name, number_of_objectives);
      exit(EXIT_FAILURE);
    }
  }
  for (size_t i = 0; i < number_of_objectives; i++)
    y[i] = y_vector[i];
}

/**
 * Bounds are defined based on instance in a deterministic way.
 */
void rw_top_trumps_bounds(size_t instance, size_t mm, double *min, double *max) {

  double l[15][4] = {
      { 39,  78,  20,  34},
      { 70,   9,  35,   7},
      { 22,  39,  14,  56},
      { 13,  19,  21,  42},
      {  5,   8,   8,  28},
      { 14,  40,   9,  25},
      { 49,  21,   1,   3},
      { 35,   4,  25,  84},
      { 21,  20,  46,  63},
      { 57,  18,  18,  42},
      { 53,  31,  41,  22},
      { 44,  12,  13,  31},
      { 34,  13,  33,  16},
      { 26,  22,   5,   3},
      { 35,  28,  78,  39}
  };
  double u[15][4] = {
      { 84,  80,  91,  77},
      { 81,  12,  42,  70},
      { 56,  44,  29,  86},
      { 92,  26,  36,  65},
      { 27,  99,  15,  45},
      { 96,  80,  81,  65},
      { 87,  59,  51, 100},
      { 79,  91,  95,  87},
      { 70,  36,  88,  72},
      { 61,  51,  82,  58},
      { 93,  50,  75,  45},
      { 79,  82,  69,  52},
      { 63,  90,  61,  79},
      {100,  46,  57,  60},
      { 67,  52,  98,  39}
  };

  assert(mm == 4);
  assert(instance <= 15);
  for (size_t i = 0; i < mm; i++) {
    min[i] = l[instance - 1][i];
    max[i] = u[instance - 1][i];
    //cout << "lower " << l[i] << ", upper " << u[i] << endl;
  }
}

#ifdef __cplusplus
}
#endif

