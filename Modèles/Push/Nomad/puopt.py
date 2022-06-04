#!/usr/bin/env python3
import PyNomad
import os

Nom_Runs=int(input('number of Nomad runs. default 100 : ') or 100)
seed=int(input('seed of the simulation. default 0 : ') or 0)

with open('run.py','w') as exe:
    exe.write ("""import sys\n"""+
               """import push_optim as po\n"""+
               """import warnings\n"""
               """warnings.filterwarnings("ignore")\n\n""")
    exe.write ("""seed="""+str(seed))
    exe.write ("""\nfilename = sys.argv[1]\n""" +
               """file = open(filename, 'r')\n""" +
               """x = file.read().split()\n""" +
               """file.close()\n\n""")
    exe.write ("""for i in range (len(x)):\n"""+
               """    x[i]=float(x[i])\n\n""")
    exe.write ("""po.push(x,seed)""")

params = ["DISPLAY_DEGREE 2", "BB_INPUT_TYPE * R", "DIMENSION 14", "X0 (0 0 0 0 16 3.1415 0 0 0 0 16 3.1415 0 0)", "LOWER_BOUND (-5 -5 -10 -10 2 0 -5 -5 -10 -10 2 0 -5 -5)", "UPPER_BOUND (5 5 10 10 30 6.2832 5 5 10 10 30 6.2832 5 5)", "MAX_BB_EVAL "+str(Nom_Runs), "BB_EXE \"$python run.py\"" , "BB_OUTPUT_TYPE OBJ"]

with open('run.py','r') :
    
    os.system("run.py")
    
    PyNomad.optimizeWithMainStep(params)