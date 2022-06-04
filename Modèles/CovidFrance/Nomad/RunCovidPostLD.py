# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 09:32:38 2021

@author: maxim
"""

import PyNomad

params = ["DISPLAY_DEGREE 2", "BB_INPUT_TYPE (R)", "DIMENSION 1", "X0 (1.2828)", "LOWER_BOUND (1)", "UPPER_BOUND (1.5)", "MAX_BB_EVAL 100", "BB_EXE \"$python CovidPostLD.py\"" , "BB_OUTPUT_TYPE OBJ"]

PyNomad.optimizeWithMainStep(params)