# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 09:32:38 2021

@author: maxim
"""

import PyNomad

params = ["DISPLAY_DEGREE 2", "BB_INPUT_TYPE (R I I R)", "DIMENSION 4", "X0 (0.085 26 8 1.4)", "LOWER_BOUND (0.07 18 6 1.2)", "UPPER_BOUND (0.1 34 9 1.6)", "MAX_BB_EVAL 100", "BB_EXE \"$python CovidPreLD.py\"" , "BB_OUTPUT_TYPE OBJ"]

PyNomad.optimizeWithMainStep(params)