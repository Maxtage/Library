#!/usr/bin/env python3
import PyNomad
import os

pb_id=int(input('There are 28 mono-objective functions and 10 bi-objective. Default 1 : ') or 1)
pb_typ=int(input('Choose whether the output will be a mono or a bi-objective one as 1 or 2. Default 1 : ') or 1)
inst_id=int(input('Chose among the 7 instances provided by the model. Default 1 : ') or 1)
nb_var=int(input('Choose the number of variable among 10, 20, 30 and 40. Default 10 : ') or 10)
Nom_Runs=int(input('number of Nomad runs. default 100 : ') or 100)
typ=['mario-gan','mario-gan-biobj']
pb_typ=typ[pb_typ-1]
with open('run.py','w') as exe:
    exe.write ("""import sys\n"""+
               """from mario_gan_evaluator import evaluate_mario_gan\n"""+
               """import warnings\n"""
               """warnings.filterwarnings("ignore")\n\n""")
    exe.write ("""pb_id="""+str(pb_id)+"""\n""" +
               """pb_typ='"""+str(pb_typ)+"""'\n""" +
               """inst_id="""+str(inst_id)+"""\n\n""")
    exe.write ("""filename = sys.argv[1]\n""" +
               """file = open(filename, 'r')\n""" +
               """x = file.read().split()\n""" +
               """file.close()\n\n""")
    exe.write ("""for i in range (len(x)):\n"""+
               """    x[i]=float(x[i])\n\n""")
    exe.write ("""res=evaluate_mario_gan(pb_typ, pb_id, inst_id, x)\n"""+
               """print(res[0])""")

params = ["DISPLAY_DEGREE 2", "BB_INPUT_TYPE * R", "DIMENSION "+str(nb_var), "X0 * 0.5", "LOWER_BOUND * 0", "UPPER_BOUND * 1", "MAX_BB_EVAL "+str(Nom_Runs), "BB_EXE \"$python run.py\"" , "BB_OUTPUT_TYPE OBJ"]

with open('run.py','r') :
    
    os.system("run.py")
    
    PyNomad.optimizeWithMainStep(params)