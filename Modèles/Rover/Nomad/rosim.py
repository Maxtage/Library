# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 11:19:12 2021

@author: maxim
"""
import rover_optim as ro 
import argparse
import sys
import warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, prog='Rover Simulator', add_help=False)
parser.add_argument('X', type=str, nargs='?', default='void', help='Point at which the model is evaluated.')
parser.add_argument('-h', '--help', action='store_true', help='Show help and exit')
parser.add_argument('-i', '--info', action='store_true', help='Show information about the program')
parser.add_argument('-t', '--test', action='store_true', help='Starts a text with a prewritten point and hard-coded results. Should display "Objective function value should be:" then twice the same value.')
args = parser.parse_args()

if not len(sys.argv) > 1:
    print("""\nRun RoSim (basic) : rosim X=...""",
          """\nHelp : rosim -h """,
          """\nInfo : rosim -i \n""")
elif args.info :
    print("""RoSim, the Rover trajectory Simulator, version 0.1, 2021-12-15\n\n""",
          """Copyright (c) 2017 Zi Wang\n\n""",
          """Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\n""", 
          """The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\n""",
          """THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n\n""",
          """Based on the following article : https://arxiv.org/abs/1706.01445 \nGithub of the model : https://github.com/zi-w/Ensemble-Bayesian-Optimization \n\n""",
          """Contributors of the wrapper : M. Gras, S. Le Digabel, L. Salomon; GERAD and Polytechnique Montreal.\n\n""",
          """This code is part of the optimization benchmark library : https://gitlab.univ-nantes.fr/chenouard-r/optimizationbenchmarklibrary.git \n\n""",
          """Please report bugs to maxime.gras@eleves.ec-nantes.fr""")
    
    
else:
    if not(args.help):
        
        if args.test or args.X=='void':
            print('Objectif function value should be : 1.21136189921953')
            ro.rover('x0.txt')
        else :
            ro.rover(args.X)
    else :
        print("""Displaying help : \n\n""",
              """Problem : Rover trajectory tuning simulation.   n=60   m=1 \n""",
              """\n-----\n\n""",
              """Parameters :\n""",
              """\tPrinciple of the model : Given a particular map, the model generates a trajectory from a point A to a point B that tests this trajectory. To evaluate the quality of a trajectory, a penality is given in case of collision.\n""",
              """\tObjective function     : The objective function is non smooth, discontinuous and concave over the first two and the last two variables.\n""",
              """\tMaximize the reward function (output) by tuning the trajectory to avoid obstacles .\n""",
              """\nVariables :\n""",
              """\tThe 60 variables are floats between 0 and 1 and represent the trajectory of the rover.\n""",
              """\n-----\n\n""",
              """NOMAD parameters :\n\n""",
              """\tDIMENSION       60\n""",
              """\tBB_EXE          rover_optim.py\n""",
              """\tBB_OUTPUT_TYPE  OBJ\n""",
              """\tBB_INPUT_TYPE   * R\n""",
              """\tLOWER_BOUND     * 0\n""",
              """\tx0              (0.196275 0.00460902 0.000104099 0.301908 0.357301 0.40352 0.295307 1.07921e-06 0.549243 0.515977 0.423745 0.201415 0.499178 0.200396 0.601782 0.299531 0.695436 0.699813 0.397904 0.00497444 0.497893 0.497883 0.203057 0.000121708 0.400321 0.00000537574 0.503713 0.50027 0.297856 0.398333 0.498088 0.298664 0.401263 0.49931 0.599467 0.497856 0.500049 0.401324 0.398875 0.396479 0.49812 0.495891 0.70049 0.394929 0.494932 0.398395 0.502055 0.402533 0.500692 0.40003 0.601128 0.398947 0.698649 0.496742 0.401329 0.399861 0.396769 0.397281 0.400146 0.899988)\n""",
              """\tUPPER_BOUND     * 1\n""",
              """\n-----\n\n""")