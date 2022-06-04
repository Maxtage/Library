# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 11:19:12 2021

@author: maxim
"""
import argparse
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

"""import warnings
warnings.filterwarnings("ignore")"""

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, prog='Top Trumps Simulator', add_help=False)
parser.add_argument('I', type=int, choices=[i+1 for i in range (15)], default=int(1), nargs='?', help='Chose among the 15 instances (seeds) provided by the model.')
parser.add_argument('P', type=int, choices=[i+1 for i in range (5)], nargs='?', help='There are 5 mono-objective functions and 3 bi-objective.')
parser.add_argument('X', type=str, default='void', nargs='?', help='Point at which the model is evaluated. x0 must have x0_size values and it represents a number of cards with 4 values each.')
parser.add_argument('T', type=int, choices=[1, 2], default=1, nargs='?', help='Choose whether the output will be a mono or a bi-objective one')
parser.add_argument('S', type=int, choices=[88,128,168,208], default=88, nargs='?', help='Choose the number of variables used by the simulation.')
#parser.add_argument('-seed', type=int, default=0, help='Choose the seed for the random functions')
parser.add_argument('-h', '--help', action='store_true', help='Show help and exit')
parser.add_argument('-i', '--info', action='store_true', help='Show information about the program')
parser.add_argument('-t', '--test', action='store_true', help='Starts a text with a prewritten point and hard-coded results. Should display "Objective function value should be:" then twice the same value.')
args = parser.parse_args()

if not len(sys.argv) > 1:
    print('\nRun TopSim (basic) : topsim P=pb_id X=x.txt',
          '\nRun TopSim (advanced) : topsim P=pb_id X=x.txt T=pb_typ I=inst_id S=x_size',
          '\n\tT : Problem type : chose weather the objctive function will be mono or bi-ojective',
          '\n\tI : Instance id : choose the instance (seed) among 15',
          '\n\tS : Number of variables in the simulation, reflects the number of cards in the deck (dividing by 4); Default=88 \n',
          '\nHelp : topsim -h \n',
          '\nHelp(instance) : topsim -h I=inst_id \n',
          '\nInfo : topsim -i \n')
elif args.info :
    print('TopSim, the Top Trumps Simulator, version 0.2, 2022-02-22\n\n',
          'The model appears in the work of Vanessa Volz, Günter Rudolph and Boris Naujoks. Link to the publication : https://arxiv.org/pdf/1603.03795.pdf\n\n',
          'Github of the model : https://github.com/ttusar/top-trumps \n\n',
          'Contributors of the wrapper : M. Gras, S. Le Digabel, L. Salomon; GERAD and Polytechnique Montreal.\n\n',
          'This code is part of the optimization benchmark library : https://gitlab.univ-nantes.fr/chenouard-r/optimizationbenchmarklibrary.git \n\n',
          'Please report bugs to maxime.gras@eleves.ec-nantes.fr')
else:
    nom_typ=b"rw-top-trumps"
    if (args.T==2) :
        nom_typ=b"rw-top-trumps-biobj"
        if (args.P>=3) :
            print('There are only 3 bi-objective functions. Please change the type of problem or choose another problem.')
    if not(args.help) :
        if args.test or args.X=='void':
            resx0=[[0.90656566,0.72292513,0.4865,0.49618182,0.12595455],[0.92708333,0.38606396,0.488,0.49454545,0.12354545],[0.93364055,0.51072458,0.5175,0.49495455,0.12409091],
                   [0.9375,0.64766669,0.526,0.50422727,0.11795455],[0.93478261,0.64006219,0.5095,0.50104545,0.12481818],[0.93271458,0.85068528,0.4845,0.50031818,0.11981818],
                   [0.93296464,0.68784773,0.5145,0.50063636,0.12431818],[0.93521127,0.68942675,0.487,0.50190909,0.12495455],[0.93228454,0.51387104,0.503,0.49704545,0.12372727],
                   [0.91936652,0.73072363,0.4905,0.49190909,0.12095455],[0.93414634,0.57256364,0.4965,0.49572727,0.12045455],[0.93550778,0.76010206,0.5,0.49195455,0.12068182],
                   [0.93534483,0.95140705,0.4945,0.50122727,0.12631818],[0.93289057,0.72530077,0.493,0.50363636,0.12259091],[0.85968254,0.43125631,0.4895,0.49686364,0.12240909]]
            
            print('Objectif function value should be : ',resx0[args.I-1][args.P-1])
            file = open('x'+str(args.I)+'.txt', 'r')
            x = file.read().split()
            file.close()
            for i in range(args.S):
                x[i]=float(x[i])
            x=np.asarray(x)
            y=[0]*args.T
            for i in range(args.T):
                y[i]=float(0)
            y=np.asarray(y)
            compute_tt(nom_typ, 1, args.P, args.I, 88, x, y)
            print(y)
        else:    
            file = open(args.X, 'r')
            x = file.read().split()
            file.close()
            if args.S!=len(x):
                print('ERROR: x_size and len(x) do not match')
            else :
                for i in range(args.S):
                    x[i]=float(x[i])
                x=np.asarray(x)
                y=[0]*args.T
                for i in range(args.T):
                    y[i]=float(0)
                y=np.asarray(y)
                compute_tt(nom_typ, args.T, args.P, args.I, args.S, x, y)
                print(y)
            
    else :
        if args.I>=1 :
            bounds=[[[ 39,  78,  20,  34],[ 84,  80,  91,  77]],
                    [[ 70,   9,  35,   7],[ 81,  12,  42,  70]],
                    [[ 22,  39,  14,  56],[ 56,  44,  29,  86]],
                    [[ 13,  19,  21,  42],[ 92,  26,  36,  65]],
                    [[  5,   8,   8,  28],[ 27,  99,  15,  45]],
                    [[ 14,  40,   9,  25],[ 96,  80,  81,  65]],
                    [[ 49,  21,   1,   3],[ 87,  59,  51, 100]],
                    [[ 35,   4,  25,  84],[ 79,  91,  95,  87]],
                    [[ 21,  20,  46,  63],[ 70,  36,  88,  72]],
                    [[ 57,  18,  18,  42],[ 61,  51,  82,  58]],
                    [[ 53,  31,  41,  22],[ 93,  50,  75,  45]],
                    [[ 44,  12,  13,  31],[ 79,  82,  69,  52]],
                    [[ 34,  13,  33,  16],[ 63,  90,  61,  79]],
                    [[ 26,  22,   5,   3],[100,  46,  57,  60]],
                    [[ 35,  28,  78,  39],[ 67,  52,  98,  39]]]
            print('The bounds for x represents the bounds for the 4 values of each card which is the same for every card in the deck.\n',
                  'We will thus give the bounds for the 4 first values of x.\n',
                  'For instance number',args.I,' the bounds are :\n'
                  'lower bounds :',bounds[args.I][1],'\n',
                  'Upper bounds :',bounds[args.I][2],'\n')
        else :
            print('TopSim, the Top Trumps Simulator, version 0.1, 2021-12-03\n\n',
                  'The model appears in the work of Vanessa Volz, Günter Rudolph and Boris Naujoks. Link to the publication : https://arxiv.org/pdf/1603.03795.pdf\n\n',
                  'Github of the model : https://github.com/ttusar/top-trumps/tree/master/utils \n\n',
                  'Run simulation : python topsim.py P=pb_id X=x.txt T=pb_typ I=inst_id S=x_size\n\n',
                  '     P : Problem ID (see list of problems below)\n\n',
                  '     X : Input vector : Point at which the simulation is evaluated.\n',
                  '         The vector must contain x_size values with boundaries depending on the inst_id\n',
                  '         Values separated with spaces\n',
                  '         It is possible to specify several vectors: Use one line for each in you .txt file.\n\n',
                  '     T : Problem type :\n',
                  '         The aim of the model is to find and equilibrated deck of Top Trumps Cards in a specifically defined search space.\n',
                  '         The finess of the decks is calculated via 5 functions (detailed in below) in mono objective mode regrouped as 3 pairs in bi-objective mod. \n',
                  '         To switch between mode, just set -pb_typ=1 or -pb_typ=2 respectiveley for mono and bi objective. \n',
                  '         All said functions aim to be minimised.\n',
                  '         Default value is 1 i.e. mono-objective.\n\n',
                  '     I : Instance ID :\n',
                  '         The model offers 15 instances of the problem changing the boundaries of variables and the seed.\n',
                  '         To change the instance you want to use, just set I=inst_id with I an integer between 1 and 15.\n',
                  '         The default instance used is the number 1.\n\n',
                  #'         If covid is run twice at the same point with the same seed, it will give the same output.\n',
                  '     S : Number of variables :\n',
                  '         Number of cards in the deck timed by 4 for the number of values in each cards.\n',
                  #'         Each replication uses a different random seed dependent on the -seed option\n',
                  '         The default value of 88 values for 22 cards is set as default.\n\n',
                  'List of objectiv functions :\n\n',
                  '         P        bi_obj problem        function description\n',
                  '         1                     1        deck hypervolume\n',
                  '         2                     1        standard deviation of category averages\n',
                  '         3                   2&3        winrate of better player\n',
                  '         4                     2        switches of trick winner\n',
                  '         5                     3        trick difference at the end of the game\n',)
