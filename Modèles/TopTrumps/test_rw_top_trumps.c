#include <stdio.h>

#include "rw_top_trumps.h"

void perform_one_test(char *suite_name, size_t number_of_objectives, size_t function,
    size_t instance, size_t dimension, const double *x) {

  size_t i;
  double *y;
  y = (double *) malloc(dimension * sizeof(double));

  evaluate_rw_top_trumps(suite_name, number_of_objectives, function, instance, dimension, x, y);

  printf("function = %lu\ny = ", function);
  for (i = 0; i < number_of_objectives; i++)
    printf("%.4f\n", y[i]);
  printf("\n");
  fflush(stdout);
  free(y);
}

int main(void) {

  size_t function;
  size_t instance = 3;
  size_t dimension = 88;
  size_t number_of_objectives = 1;
  size_t i, m = 4;
  double *x;
  double *lb;
  double *ub;

  x = (double *) malloc(dimension * sizeof(double));
  lb = (double *) malloc(m * sizeof(double));
  ub = (double *) malloc(m * sizeof(double));
  rw_top_trumps_bounds(instance, m, lb, ub);
  /* Set x to be the middle of the domain */
  for (i = 0; i < dimension; i++) {
    if (i < 3)
      printf("%lu lb = %f ub = %f\n", i, ub[i], lb[i]);
    x[i] = (ub[i % m] + lb[i % m]) / 2;
  }
  free(lb);
  free(ub);

  printf("instance = %lu, objectives = %lu\n",
      (unsigned long) instance,
      (unsigned long) number_of_objectives);
  printf("x = ");
  for (i = 0; i < dimension; i++)
    printf("%.0f ", x[i]);
  printf("\n");
  
  for (function = 1; function <= 5; function++) {
    perform_one_test("rw-top-trumps", number_of_objectives, function, instance, dimension, x);
  }
  free(x);
  
  printf("Done!\n");
  fflush(stdout);

  return 0;
}

