# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 11:19:12 2021

@author: maxim
"""
from CovidPreLD import pre
from CovidPostLD import post
import argparse
import sys

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, prog='Covid Simulator', add_help=False)
parser.add_argument('P', choices=[1, 2], nargs='?', type=int, help='Problem n°1 is pre lockdown, problem n°2 is post lockdown.')
parser.add_argument('X', default='void', nargs='?', help='Point at which the model is evaluated. Examples are given by typing : covid -h P')
parser.add_argument('R', type=str, nargs='?', choices=['IDF', 'CVL', 'BFC', 'NOR', 'HDF', 'GRE', 'PDL', 'BRE', 'NAQ', 'OCC', 'ARA', 'PACA'], default='PDL', help='Choose the region where the simulation takes place')
parser.add_argument('S', type=int, nargs='?', default=0, help='Choose the seed for the random functions, default 0')
parser.add_argument('I', type=int, nargs='?', default=500, help='Choose the number of stochastics runs for the simulation')
parser.add_argument('-h', '--help', action='store_true', help='Show help and exit')
parser.add_argument('-i', '--info', action='store_true', help='Show information about the program')
parser.add_argument('-t', '--test', action='store_true', help='Starts a text with a prewritten point and hard-coded results. Should display "Objective function value should be:" then twice the same value.')

args = parser.parse_args()
    
if not len(sys.argv) > 1:
    print('\nRun CoSim (basic) : cosim P=pb_id X=x.txt',
          '\nRun CoSim (advanced) : cosim P=pb_id X=x.txt R=chosen_region S=seed I=number_runs',
          '\n\tX : Point where the simulation is evaluated. '
          '\n\tR : region of simulation : string in a list selecting the data that will be used; Default=44 ',
          '\n\tS : Random seed : integer >=0; Default=0 ',
          '\n\tI : Number >=1 of stochastic runs in the simulation; Default=500 \n',
          '\nHelp(1) : cosim -h ',
          '\nHelp(2) : cosim -h P ',
          '\nInfo    : cosim -i \n')
elif args.info :
    print('CoSim, the Covid spreading Simulator, version 0.3, 2022-02-22\n\n',
          'Copyright (c) 2020, EPIcx lab\n\nRelated scientific article:\nPullano, G., Di Domenico, L., Sabbatini, C.E. et al. \nUnderdetection of COVID-19 cases in France threatens epidemic control. \nNature (2020). https://doi.org/10.1038/s41586-020-03095-6 \n\nAll rights reserved.\n\n',
          'Github of the model : https://github.com/EPIcx-lab/COVID-19/tree/master/Underdetection_France . \n\n',
          'Contributors of the wrapper : M. Gras, S. Le Digabel, L. Salomon; GERAD and Polytechnique Montreal.\n\n',
          'This code is part of the optimization benchmark library : https://gitlab.univ-nantes.fr/chenouard-r/optimizationbenchmarklibrary.git \n\n',
          'Please report bugs to maxime.gras@eleves.ec-nantes.fr')

elif not(args.help) :
    
    y=[7224.681271893356,134.99708663909936]
    if args.P==1 :
        if args.test or args.X=='void':
            print('Objective function value should be :',y[args.P-1])
            pre('PDL',0,500,'x0pre.txt')
        else :
            pre(args.R,args.S,args.I,args.X)
    elif args.P==2 :
        if args.test or args.X=='void':
            print('Objective function value should be :',y[args.P-1])
            post('PDL',0,500,'x0post.txt')
        else :
            post(args.R,args.S,args.I,args.X)
            
elif args.P == 1 :
    print('Display help for problem 1 \n\n',
          'Problem : Parameter tuning for pre lockdown COVID-19 spreading in France.   n=4   m=1 \n',
          '\n-----\n\n',
          'Parameters :\n',
          '\tConsidered region :          select the set of data that will be used to calculate likelihood (how close to reality are the values of beta, delay, lag and alpha1).\n',
          '\tNumber of stochastic runs :  this problem uses random functions to simulate contacts between populations. To avoid statistics anomaly a great number of stochastic runs (500) is used and the median is used to compute the result.\n',
          '\nObjective (first output, stochastic)\n',
          '\tMaximize the likelihood (output) by tuning the values of the variables to fit the data of the region as much as possible.\n',
          '\nVariables (a suitable starting point is given with x0pre.txt):\n',
          '\tbeta :    epidemiological parameter.                       Float in [0.07;0.1]\n',
          '\tlag :     number of days before march 1st.                 Integer in [[18;34]]\n',
          '\tdelay :   number of days before application of lockdown.   Integer in [[6;9]]\n',
          '\talpha1 :  scaling factor of the pre-LD transmission rate.  Float in [1.2;1.6]\n',
          '\n-----\n\n',
          'NOMAD parameters :\n\n',
          '\tDIMENSION       4\n',
          '\tBB_EXE          RunCovidPreLD.py\n'
          '\tBB_OUTPUT_TYPE  OBJ\n',
          '\tBB_INPUT_TYPE   ( R I I R)\n',
          '\tLOWER_BOUND     ( 0.07 18 6 1.2)\n',
          '\tx0              ( 0.085 26 8 1.4)\n',
          '\tUPPER_BOUND     ( 0.1 34 9 1.6)\n',
          '\n-----\n\n')
elif args.P == 2 :
    print('Display help for problem 2 \n\n',
          'Problem : Parameter tuning for post lockdown COVID-19 spreading in France.   n=1   m=1 \n',
          '\n-----\n\n',
          'Parameters :\n',
          '\tPreLD fitting parameters :   this second part uses the value of beta, delay, lag and alpha1 as parameters to tune the value of alpha2.\n'
          '\tConsidered region :          select the set of data that will be used to calculate likelihood (how close to reality is the value of alpha2).\n',
          '\tNumber of stochastic runs : this problem uses random functions to simulate contacts between populations. To avoid statistics anomaly a great number of stochastic runs (500) is used and the median is used to compute the result.\n',
          '\nObjective (first output, stochastic)\n',
          '\tMaximize the likelihood (output) by tuning the values of the variables to fit the data of the region as much as possible.\n',
          '\nVariables (a suitable starting point is given with x0post.txt ):\n',
          '\talpha2 :  scaling factor of the pre-LD transmission rate, fitted after lifting lockdown\n',
          '\n-----\n\n',
          'NOMAD parameters :\n\n',
          '\tDIMENSION       1\n',
          '\tBB_EXE          RunCovidPostLD.py\n'
          '\tBB_OUTPUT_TYPE  OBJ\n',
          '\tBB_INPUT_TYPE   ( R)\n',
          '\tLOWER_BOUND     ( 1)\n',
          '\tX0              ( 1.25)\n',
          '\tUPPER_BOUND     ( 1.5)\n',
          '\n-----\n\n')
else :
    print('CoSim, the Covid spreading Simulator, version 0.2, 2021-11-11\n\n',
          'Copyright (c) 2020, EPIcx lab\n\nRelated scientific article:\nPullano, G., Di Domenico, L., Sabbatini, C.E. et al. \nUnderdetection of COVID-19 cases in France threatens epidemic control. \nNature (2020). https://doi.org/10.1038/s41586-020-03095-6 \n\nAll rights reserved.\n\n',
          'Github of the model : https://github.com/EPIcx-lab/COVID-19/tree/master/Underdetection_France. \n\n',
          'Run simulation : python covid.py P=pb_id X=x.txt R=chosen_region S=seed I=nb_runs\n\n',
          '     P : Problem ID (see list of problems below)\n\n',
          '     X : Input vector : Point at which the simulation is evaluated\n',
          '         Values separated with spaces\n',
          '         It is possible to specify several vectors: Use one line for each in you .txt file.\n\n',
          '     R : Region of study :\n',
          '         The aim of both problem is to determine what were the values of epidemiologic parameters in France by comparing the simualtion bred by those parameters to true data depending on the chosen region.\n',
          '         The region can be chosen in the following list : IDF, CVL, BFC, NOR, HDF, GRE, PDL, BRE, NAQ, OCC, ARA, PACA\n',
          '         Important to note that the point maximizing the likelihood heavily depends ont the chosen region.\n',
          '         Default value is arbitrarily set at PDL.\n\n',
          '     S : Random seed :\n',
          '         The covid simulation uses binomial law to model the spread of the virus in the population.\n',
          '         To ensure the reproductibility of the results despite the randomness, a seed has been introduced to the blackbox.\n',
          '         A seed is a natural integer with a default value of 0.\n',
          '         If covid is run twice at the same point with the same seed, it will give the same output.\n',
          '     I : Number of stochastic runs :\n',
          '         Number of iteration of the simulation at the same point before taking the median of the result to calculate the likelihood.\n',
          '         Each replication uses a different random seed dependent on the seed option\n',
          '         The default value of 500 iteration is adviced.\n\n',
          'Help for a problem : python cosim.py -h P=pb_id\n\n',
          'List of problems :\n\n',
          '     pb_id      # of var\n',
          '         1             4\n',
          '         2             1\n')
