#!/usr/bin/env python3
import PyNomad
import os

Nom_Runs=int(input('number of Nomad runs. default 100 : ') or 100)

with open('run.py','w') as exe:
    exe.write ("""import sys\n"""+
               """import rover_optim as ro\n"""+
               """import warnings\n"""
               """warnings.filterwarnings("ignore")\n\n""")
    exe.write ("""filename = sys.argv[1]\n""" +
               """file = open(filename, 'r')\n""" +
               """x = file.read().split()\n""" +
               """file.close()\n\n""")
    exe.write ("""for i in range (len(x)):\n"""+
               """    x[i]=float(x[i])\n\n""")
    exe.write ("""ro.rover(x)""")

params = ["DISPLAY_DEGREE 2", "BB_INPUT_TYPE * R", "DIMENSION 60", "X0 (0.196275 0.00460902 0.000104099 0.301908 0.357301 0.40352 0.295307 1.07921e-06 0.549243 0.515977 0.423745 0.201415 0.499178 0.200396 0.601782 0.299531 0.695436 0.699813 0.397904 0.00497444 0.497893 0.497883 0.203057 0.000121708 0.400321 0.00000537574 0.503713 0.50027 0.297856 0.398333 0.498088 0.298664 0.401263 0.49931 0.599467 0.497856 0.500049 0.401324 0.398875 0.396479 0.49812 0.495891 0.70049 0.394929 0.494932 0.398395 0.502055 0.402533 0.500692 0.40003 0.601128 0.398947 0.698649 0.496742 0.401329 0.399861 0.396769 0.397281 0.400146 0.899988)", "LOWER_BOUND * 0", "UPPER_BOUND * 1", "MAX_BB_EVAL "+str(Nom_Runs), "BB_EXE \"$python run.py\"" , "BB_OUTPUT_TYPE OBJ"]

with open('run.py','r') :
    
    os.system("run.py")
    
    PyNomad.optimizeWithMainStep(params)