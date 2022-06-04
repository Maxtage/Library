from cffi import FFI

ffibuilder = FFI()
ffibuilder.cdef("""
    void evaluate_rw_top_trumps(char *suite_name, size_t number_of_objectives, size_t function, size_t instance, size_t dimension, const double *x, double *y);;
""")
ffibuilder.set_source("_toptrumps_cffi",
"""
    #include "rw_top_trumps.h"
""",
    libraries=['toptrumps'])

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)