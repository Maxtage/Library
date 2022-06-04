import PyNomad
import os

pb_typ=int(input('Choose whether the output will be a mono or a bi-objective one as 1 or 2. Default 1 : ') or 1)
pb_id=int(input('There are 5 mono-objective functions and 3 bi-objective. Default 1 : ') or 1)
inst_id=int(input('Chose among the 15 instances provided by the model. Default 1 : ') or 1)
nb_var=int(input('Choose the number of variable among 88, 128, 168 and 208. Default 88 : ') or 88)
Nom_Runs=int(input('number of Nomad runs. default 100 : ') or 100)

with open('run.py','w') as exe:
    exe.write ("""import sys\n"""+
               """import numpy as np\n"""+
               """import ctypes\n"""+
               """lib_toptrumps = ctypes.cdll.LoadLibrary('./librw_top_trumps.so')\n"""+
               """compute_tt = lib_toptrumps.evaluate_rw_top_trumps\n"""+
               """compute_tt.argtypes = [\n"""+
               """    ctypes.c_char_p,\n"""+
               """    ctypes.c_size_t,\n"""+
               """    ctypes.c_size_t,\n"""+
               """    ctypes.c_size_t,\n"""+
               """    ctypes.c_size_t,\n"""+
               """    np.ctypeslib.ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),\n"""+
               """    np.ctypeslib.ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),\n"""+   
               """    ]\n"""+
               """compute_tt.restypes = [ctypes.c_void_p]\n"""+
               """import warnings\n"""
               """warnings.filterwarnings("ignore")\n\n""")
    exe.write ("""pb_id="""+str(pb_id)+"""\n""" +
               """pb_typ="""+str(pb_typ)+"""\n""" +
               """nb_var="""+str(nb_var)+"""\n""" +
               """inst_id="""+str(inst_id)+"""\n\n""")
    exe.write ("""nom_typ=b"rw-top-trumps"\n"""+
               """if (pb_typ==2) :\n"""+
               """   nom_typ=b"rw-top-trumps-biobj"\n""")
    exe.write ("""filename = sys.argv[1]\n""" +
               """file = open(filename, 'r')\n""" +
               """x = file.read().split()\n""" +
               """file.close()\n\n""")
    exe.write ("""for i in range (nb_var):\n"""+
               """    x[i]=float(x[i])\n\n"""+
               """x=np.asarray(x)\n"""+
               """y=[0]*pb_typ\n"""+
               """for i in range(pb_typ):\n"""+
               """    y[i]=float(0)\n""")
    exe.write ("""y=np.asarray(y)\n"""+
               """compute_tt(nom_typ, pb_typ, pb_id, inst_id, nb_var, x, y)\n"""+
               """print(y[0])""")
lowbo='('
upbo='('
x0='('
bounds=[["39 78 20 34 ","84 80 91 77 ","62 79 55 55 "],
        ["70 9 35 7 ","81 12 42 70 ","75 11 38 38 "],
        ["22 39 14 56 ","56 44 29 86 ","39 42 22 71 "],
        ["13 19 21 42 ","92 26 36 65 ","57 23 28 58 "],
        ["5 8 8 28 ","27 99 15 45 ","16 58 12 37 "],
        ["14 40 9 25 ","96 80 81 65 ","55 60 45 45 "],
        ["49 21 1 3 ","87 59 51 100 ","68 40 26 52 "],
        ["35 4 25 84 ","79 91 95 87 ","57 48 60 86 "],
        ["21 20 46 63 ","70 36 88 72 ","45 28 77 68 "],
        ["57 18 18 42 ","61 51 82 58 ","59 35 50 50 "],
        ["53 31 41 22 ","93 50 75 45 ","73 40 58 34 "],
        ["44 12 13 31 ","79 82 69 52 ","62 47 41 42 "],
        ["34 13 33 16 ","63 90 61 79 ","48 52 47 48 "],
        ["26 22 5 3 ","100 46 57 60 ","63 34 31 32 "],
        ["35 28 78 39 ","67 52 98 39 ","52 40 88 39"]]
for i in range(int(nb_var/4)):
    lowbo+=bounds[inst_id-1][0]
    upbo+=bounds[inst_id-1][1]
    x0+=bounds[inst_id-1][2]
lowbo+=')'
upbo+=')'
x0+=')'
params = ["DISPLAY_DEGREE 2", "BB_INPUT_TYPE * R", "DIMENSION "+str(nb_var), "X0 "+x0, "LOWER_BOUND "+lowbo, "UPPER_BOUND "+upbo, "MAX_BB_EVAL "+str(Nom_Runs), "BB_EXE \"$python run.py\"" , "BB_OUTPUT_TYPE OBJ"]

with open('run.py','r') :
    
    os.system("run.py")
    
    PyNomad.optimizeWithMainStep(params)