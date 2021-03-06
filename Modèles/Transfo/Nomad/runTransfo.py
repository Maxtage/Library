import PyNomad


params = ["DISPLAY_ALL_EVAL TRUE", "DISPLAY_DEGREE 2", "BB_INPUT_TYPE (R R R R R I R R)", "DIMENSION 8", "X0 (0.018 0.054 0.018 0.0335 8.0 722 0.3318 2.835)", "LOWER_BOUND (0.002 0.006 0.0035 0.0052 8 200 0.05515 0.05515)", "UPPER_BOUND (0.0225 0.095 0.04 0.465 8.5 1200 19.635 19.635)", "MAX_BB_EVAL 5000", "BB_EXE \"$python bb5.py\"" , "BB_OUTPUT_TYPE OBJ PB PB PB PB PB PB PB PB PB", "DISPLAY_STATS BBE [BBO] (SOL)", "VNS_MADS_SEARCH true"]
#params = ["DISPLAY_ALL_EVAL TRUE", "DISPLAY_DEGREE 2", "BB_INPUT_TYPE (R R R R R I R R)", "DIMENSION 8", "X0 (0.012 0.050 0.0217 0.235 8.25 700 10 10)", "LOWER_BOUND (0.002 0.006 0.0035 0.0052 8 200 0.05515 0.05515)", "UPPER_BOUND (0.0225 0.095 0.04 0.465 8.5 1200 19.635 19.635)", "MAX_BB_EVAL 1000", "BB_EXE \"$python bb5.py\"" , "BB_OUTPUT_TYPE OBJ PB PB PB PB PB PB PB PB PB", "DISPLAY_STATS BBE [BBO] (SOL)", "VNS_MADS_SEARCH true"]
#params = ["DISPLAY_DEGREE 2", "BB_INPUT_TYPE (R R R R R I R R)", "DIMENSION 8", "X0 ( 0.0225 0.006 0.0317 0.0052 8 1100 12 19.635 )", "LOWER_BOUND (0.002 0.006 0.0035 0.0052 8 200 0.05515 0.05515)", "UPPER_BOUND (0.0225 0.095 0.04 0.465 8.5 1200 19.635 19.635)", "MAX_BB_EVAL 1000", "BB_EXE \"$python bb5.py\"" , "BB_OUTPUT_TYPE OBJ EB EB EB EB EB EB EB EB EB"]
#params = ["DISPLAY_DEGREE 3"] "X0 (0.0123 0.05 0.022 0.250 8 700 9.85 9.85)" 

PyNomad.optimizeWithMainStep(params)