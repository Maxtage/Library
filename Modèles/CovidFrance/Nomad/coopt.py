#!/usr/bin/env python3
import PyNomad
import os

region=input('choose the region studied among : IDF, CVL, BFC, NOR, HDF, GRE, PDL, BRE, NAQ, OCC, ARA, PACA : ')
seed=int(input('give the seed as an int, default 0 : ') or 0)
nb_runs=int(input('give the number of run of the simulation, default 500 : ') or 500)
Nom_Runs=int(input('number of Nomad runs. default 100 : ') or 100)

with open('run.py','w') as exe:
    exe.write ("""import sys\n"""+
               """from CovidPostLD import post\n"""+
               """import warnings\n"""
               """warnings.filterwarnings("ignore")\n\n""")
    exe.write ("""region='"""+str(region)+"""'\n""" +
               """seed="""+str(seed)+"""\n""" +
               """nb_runs="""+str(nb_runs)+"""\n\n""")
    exe.write ("""filename = sys.argv[1]\n""" +
               """file = open(filename, 'r')\n""" +
               """x = file.read().split()\n""" +
               """file.close()\n\n""")
    exe.write ("""post(region,seed,nb_runs,x)""")

params = ["DISPLAY_DEGREE 2", "BB_INPUT_TYPE (R)", "DIMENSION 1", "X0 (1.2828)", "LOWER_BOUND (1)", "UPPER_BOUND (1.5)", "MAX_BB_EVAL "+str(Nom_Runs), "BB_EXE \"$python run.py\"" , "BB_OUTPUT_TYPE OBJ"]

with open('run.py','r') :
    
    os.system("run.py")
    
    PyNomad.optimizeWithMainStep(params)