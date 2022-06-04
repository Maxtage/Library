import sys
import numpy as np
import ctypes
lib_toptrumps = ctypes.cdll.LoadLibrary('./librw_top_trumps.so')
compute_tt = lib_toptrumps.evaluate_rw_top_trumps
compute_tt.argtypes = [
    ctypes.c_char_p,
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_size_t,
    np.ctypeslib.ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
    np.ctypeslib.ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
    ]
compute_tt.restypes = [ctypes.c_void_p]
import warnings
warnings.filterwarnings("ignore")

pb_id=1
pb_typ=1
nb_var=88
inst_id=1

nom_typ=b"rw-top-trumps"
if (pb_typ==2) :
   nom_typ=b"rw-top-trumps-biobj"
filename = sys.argv[1]
file = open(filename, 'r')
x = file.read().split()
file.close()

for i in range (nb_var):
    x[i]=float(x[i])

x=np.asarray(x)
y=[0]*pb_typ
for i in range(pb_typ):
    y[i]=float(0)
y=np.asarray(y)
compute_tt(nom_typ, pb_typ, pb_id, inst_id, nb_var, x, y)
print(y[0])