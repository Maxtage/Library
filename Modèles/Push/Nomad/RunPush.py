import PyNomad
from math import pi

params = ["DISPLAY_ALL_EVAL TRUE", 
          "DISPLAY_DEGREE 2", 
          "BB_INPUT_TYPE * R",
          "DIMENSION 14", 
          #"X0 (0.71412417 0.01737413 0.83787368 0.03375269 0.72641904 0.32773885 0.12704733 0.33536406 0.46173725 0.77908252 0.74224209 0.39324283 0.7636898  0.35976535 0.14093736 0.08919239 0.94767922 0.55762565 0.36298978 0.9919607  0.86099155 0.02714548 0.03162697 0.04021853 0.21778863 0.81216591 0.21428733 0.14657265 0.73184533 0.00540801 0.23606255 0.42255036 0.05413497 0.78821545 0.21381919 0.37630623 0.99136396 0.47840592 0.2886068  0.32256787 0.49661272 0.2818386 0.0149737  0.79663352 0.32182895 0.15547712 0.32149378 0.89132598 0.93927855 0.81450949 0.87161931 0.59662425 0.79324917 0.95474541 0.58367523 0.48771891 0.95151351 0.15836578 0.15152854 0.15895667)",
          "X0 * 2", 
          "LOWER_BOUND (-5 -5 -10 -10  2    0 -5 -5 -10 -10  2    0 -5 -5)", 
          "UPPER_BOUND ( 5  5  10  10 30 6.29  5  5  10  10 30 6.29  5  5)", 
          "MAX_BB_EVAL 5000", 
          "BB_EXE \"$python push_optim.py\"" , 
          "BB_OUTPUT_TYPE OBJ", 
          "DISPLAY_STATS BBE [BBO] (SOL) [CONS_H]", 
          "VNS_MADS_SEARCH true"]


PyNomad.optimizeWithMainStep(params)