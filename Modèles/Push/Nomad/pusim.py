# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 11:19:12 2021

@author: maxim
"""
import push_optim as po 
import argparse
import sys
import warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, prog='Rover Simulator', add_help=False)
parser.add_argument('X', type=str, default='void', nargs='?', help='Point at which the model is evaluated.')
parser.add_argument('S', type=int, default=0, nargs='?', help='Choose the seed for the random functions, default 0.')
parser.add_argument('-h', '--help', action='store_true', help='Show help and exit')
parser.add_argument('-i', '--info', action='store_true', help='Show information about the program')
parser.add_argument('-t', '--test', action='store_true', help='Starts a text with a prewritten point and hard-coded results. Should display "Objective function value should be:" then twice the same value.')
args = parser.parse_args()

if not len(sys.argv) > 1:
    print('\nRun PuSim (basic) : pusim X=x.txt',
          '\nHelp : pusim -h ',
          '\nInfo : pusim -i \n')
elif args.info :
    print('PuSim, the Robot pushing Simulator, version 0.2, 2022-02-22\n\n',
          'Copyright (c) 2017 Zi Wang\n\n',
          'Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\n', 
          'The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\n',
          'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n\n',
          'Based on the following article : https://arxiv.org/abs/1706.01445 \nGithub of the model : https://github.com/zi-w/Ensemble-Bayesian-Optimization \n\n',
          'Contributors of the wrapper : M. Gras, S. Le Digabel, L. Salomon; GERAD and Polytechnique Montreal.\n\n',
          'This code is part of the optimization benchmark library : https://gitlab.univ-nantes.fr/chenouard-r/optimizationbenchmarklibrary.git \n\n',
          'Please report bugs to maxime.gras@eleves.ec-nantes.fr')
    
    
else:
    if not(args.help) :
        if args.test:
            print('Objectif function value should be : -1.6292807695299496')
            po.push('x0.txt',0)
        else :
            po.push(args.X,args.S)
    else :
        print('Displaying help : \n\n',
              'Problem : Robot pushing simulation.   n=14   m=1 \n',
              '\n-----\n\n',
              'Parameters :\n',
              '\tPrinciple of the model : The model simulates two robots hands pushing two objects using python library Box2D.\n',
              '\tObjective function     : The objective function is defined to be the progress made toward pushinf the objects to the goal.\n',
              '\tMaximize the reward function (output) by tuning the push parameters (variables) to push the two objects as close as possible to the objective.\n',
              '\nVariables :\n',
              '\tThe 14 variables are floats representing the location and rotation of the robot hands..\n',
              '\n-----\n\n',
              'NOMAD parameters :\n\n',
              '\tDIMENSION       14\n',
              '\tBB_EXE          push_optim.py\n'
              '\tBB_OUTPUT_TYPE  OBJ\n',
              '\tBB_INPUT_TYPE   * R\n',
              '\tLOWER_BOUND     (-5 -5 -10 -10 2 0 -5 -5 -10 -10 2 0 -5 -5)\n',
              '\tx0              (0 0 0 0 16 1 0 0 0 0 16 1 0 0)\n',
              '\tUPPER_BOUND     (5 5 10 10 30 2 5 5 10 10 30 2 5 5)\n',
              '\n-----\n\n')