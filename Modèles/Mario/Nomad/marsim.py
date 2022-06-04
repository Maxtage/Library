# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 11:19:12 2021

@author: maxim
"""
from mario_gan_evaluator import evaluate_mario_gan
import argparse
import sys
import numpy as np
"""import warnings
warnings.filterwarnings("ignore")"""

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, prog='Mario Gan Simulator', add_help=False)
parser.add_argument('P', type=int, choices=[i+1 for i in range (28)], nargs='?', help='There are 28 mono-objective functions and 10 bi-objective.')
parser.add_argument('X', type=str, default='void', nargs='?', help='Point at which the model is evaluated. x0 can have either 10, 20, 30 or 40 values.')
parser.add_argument('T', type=str, choices=['mario-gan-biobj', 'mario-gan'], default='mario-gan', nargs='?', help='Choose whether the output will be a mono or a bi-objective one')
parser.add_argument('I', type=int, choices=[i+1 for i in range (7)], default=1, nargs='?', help='Chose among the 7 instances provided by the model.')
#parser.add_argument('-seed', type=int, default=0, help='Choose the seed for the random functions')
parser.add_argument('-h', '--help', action='store_true', help='Show help and exit')
parser.add_argument('-i', '--info', action='store_true', help='Show information about the program')
args = parser.parse_args()


if not len(sys.argv) > 1:
    print('\nRun MarSim (basic) : Marsim P=pb_id X=x.txt',
          '\nRun MarSim (advanced) : Marsim P=pb_id X=x.txt T=pb_typ I=inst_id',
          '\n\tX : Point where the simulation is evaluated. '
          '\n\tT : problem type : chose weather the objctive function will be mono or bi-ojective; Default=mario-gan i.e. mono objective ',
          '\n\tI : instance id : choose the instance among 7; Default=1 ',
          '\nHelp : marsim -h \n',
          '\nInfo : marsim -i \n')
elif args.info :
    print('MarSim, the Mario Gan Simulator, version 0.2, 2022-02-22\n\n',
          'The model appears in the work of Vanessa Volz, Jacob Schrum, Jialin Liu, Simon M. Lucas, Adam Smith and Sebastian Risi. Link to the publication : https://arxiv.org/pdf/1805.00728.pdf\n\n',
          'Github of the model : https://github.com/CIGbalance/mario-gan \n\n',
          'Contributors of the wrapper : M. Gras, S. Le Digabel, L. Salomon; GERAD and Polytechnique Montreal.\n\n',
          'This code is part of the optimization benchmark library : https://gitlab.univ-nantes.fr/chenouard-r/optimizationbenchmarklibrary.git \n\n',
          'Please report bugs to maxime.gras@eleves.ec-nantes.fr')
else:
    if (args.T=='mario-gan-biobj') and (args.P>=11) :
        print('There are only 10 bi-objective functions. Please change the type of problem or choose another problem.')
    elif not(args.help) and args.X!='void':

        file = open(args.X, 'r')
        x = file.read().split()
        file.close()
        for i in range (len(x)):
            x[i]=float(x[i])
        res=evaluate_mario_gan(args.T, args.P, args.I, x)
        
        print(res[0])
    else :
        print('MarSim, the Mario Gan Simulator, version 0.2, 2022-02-22\n\n',
              'The model appears in the work of Vanessa Volz, Jacob Schrum, Jialin Liu, Simon M. Lucas, Adam Smith and Sebastian Risi. Link to the publication : https://arxiv.org/pdf/1805.00728.pdf\n\n',
              'Github of the model : https://github.com/CIGbalance/mario-gan \n\n',
              'Run simulation : python marsim.py P=pb_id X=x.txt T=pb_type I=inst_id \n\n',
              '     P : Problem ID (see list of problems below)\n\n',
              '     X : Input vector : Point at which the simulation is evaluated.\n',
              '         The vector can contain either 10, 20, 30 or 40 values between 0 and 1\n',
              '         Values separated with spaces\n',
              '         It is possible to specify several vectors: Use one line for each in you .txt file.\n\n',
              '     T : Problem type :\n',
              '         The aim of the model is to find good Mario levels in a specifically defined search space.\n',
              '         The finess of the discovered levels calculated via 28 functions (detailed in -h_func) in mono objective mode regrouped as 10 pairs in bi-objective mod. \n',
              '         To switch between mode, just set -pb_typ=mario-gan-biobj or -pb_typ=mario-gan respectiveley for bi and mono objective. \n',
              '         All said functions aim to be minimised.\n',
              '         Default value is mario_gan i.e. mono-objective.\n\n',
              '     I : Instance ID :\n',
              '         The model offers seven instances of the problem changing the output for the same starting point.\n',
              '         To change the instance you want to use, just set inst_id=N with N an integer between 1 and 7.\n',
              '         The default instance used is the number 1.\n\n',
              '\nBecause the functions are stochastics, no test are available for this model.\n\n'
              'List of objectiv functions :\n\n',
              '     pb_id        bi_obj problem        function description\n',
              '         1                     /        enemyDistribution in overworld\n',
              '         2                     /        enemyDistribution in underworld\n',
              '         3                     /        positionDistribution in overworld\n',
              '         4                   1&2        positionDistribustion in underworld\n',
              '         5                     /        decorationFrequency in overworld\n',
              '         6                     1        decorationFrequency in underworld\n',
              '         7                     /        negativeSpace in overworld\n',
              '         8                     2        negativeSpace in underworld\n',
              '         9                     /        leniency in overworld\n',
              '         10                    /        leniency in underworld\n',
              '         11                  3&4        basicFitness in overworld with A* AI\n',
              '         12                  5&6        basicFitness in underworld with A* AI\n',
              '         13                  7&8        basicFitness in overworld concatenated with A* AI\n',
              '         14                 9&10        basicFitness in underworld concatenated with A* AI\n',
              '         15                    /        basicFitness in overworld with Scared AI\n',
              '         16                    /        basicFitness in underworld with Scared AI\n',
              '         17                    3        airTime in overworld with A* AI\n',
              '         18                    5        airTime in underworld with A* AI\n',
              '         19                    7        airTime in overworld concatenated with A* AI\n',
              '         20                    9        airTime in underworld concatenated with A* AI\n',
              '         21                    /        airTime in overworld with Scared AI\n',
              '         22                    /        airTime in underworld with Scared AI\n',
              '         23                    4        timeTaken in overworld with A* AI\n',
              '         24                    6        timeTaken in underworld with A* AI\n',
              '         25                    8        timeTaken in overworld concatenated with A* AI\n',
              '         26                   10        timeTaken in underworld concatenated with A* AI\n',
              '         27                    /        timeTaken in overworld with Scared AI\n',
              '         28                    /        timeTaken in underworld with Scared AI\n\n',
              'Description of functions  :\n',
              '     enemyDistribution    : standard dev. (std.) of enemy tiles (x-axis)\n',
              '     positionDistribution : std. of tiles you can stand on (y-axis)\n',
              '     decorationFrequency  : percentage of pretty tiles (Tube, Enemy, Destructible Block, Question Block, or Bullet Bill)\n',
              '     negativeSpace        : percentage of tiles you can stand on\n',
              '     leniency             : weighted sum of subjective leniency of tiles\n',
              '     basicFitness         : MarioAI championship score for AI\n',
              '     airTime              : ratio between ticks in air vs. total ticks (if level completed, otherwise 1)\n',
              '     timeTaken            : ratio between time taken and total time allowed (if level completed, otherwise 1)')
