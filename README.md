# OptimizationBenchmarkLibrary

Welcome to the Optimization Benchmark Library. This library aims to provide a large panel of different models to test optimization tools.

## Required programs and Installation

Please, use the Installation Guide to make sure to setup correctly the library. All programs, packages and version are provided in here.

## Using the library

Two types of models are provided, black box and white box. Please refer to the internship report in the master directory. To summarize black box are optimization problems where we don't know the equations giving the constraints and the objective function and white box are the opposite.

To acquire the list of models, please run 

'''bash
python LibExplore.py -l
'''

The original 11 boxes are coded for Nomad and Ibex. The black boxes car be run with Nomad and the white ones can be run with both Ibex and Nomad.

To run a model from the Library, two options are available :

EASY RUN :

Working in the main directory, run the following command with X the name of a model to launch the basic version of a model. You'll be given the choice of the algorithm if several are available.

'''bash
python LibExplore.py X
'''

COMPLETE RUN :

To have more latitude when using models, you might want to bypass the LibExplore.py file. 

To run a white box with minibex, you'll need to install Ibex (http://www.ibex-lib.org/) and run a .mbx file with the command in a shell. 

'''bash
ibexopt model.mbx
'''

To run a black box, you'll have to use Nomad (https://nomad-4-user-guide.readthedocs.io/en/latest/). Three types of file are provided to do so : param.txt modsim.py and modopt.py. 

param.txt is the most basic file, it contains the name of the black box to execute, the bounds, initial guess and number of variables (ordered) the type of output and the number of nomad runs allowed. To run it, make sure that the param.txt and the black box file are both in you working directory 
	
modsim.py is just an example of sim.py file provided for the original 6 black box. This file allows the user to know the black box and explore all its instance and possibility through the evaluation of one desired point (and not the optimization). Therefore, Nomad is not ran but the file intends to be a good basis for other algorithm and be able to run the modopt.py. To run it, go into the Nomad directory of the desired model and enter the following command in a shell.

'''bash
python modsim.py
'''
	
modopt.py is the file used to run the optimization of the desired instance with Nomad. To run the following command in a shell. 

'''bash
python modopt.py
'''

The user will then be asked to enter some values related to the instance over which the optimization should be run. For this reason, it's better to have run modsim.py at least once before.
	
For some reasons, you might want to run a minibex model with Nomad (which is something LibExplore.py does when a nomad file is present for a model but no suitable nomad file are found and ibex file can be found). That is the point of PasserelleIbex directory. Moreover, a generalization of model under the form of a .json file can also be run by the passerelle. To do so, make sure the .mbx or .json file are in the PasserelleIbex directory, then run the suitable command in a shell. Note that in the case of a .json file, MiNomad.py will create a corresponding .mbx file.

'''bash
python MiNomad.py model.mbx
or
python MiNomad.py model.json
'''

## Adding a model

If you have a model you want to add to the library, please conform to the Template directory under /Modèles and follow the "Model creation guide".

The name of your model directory should be unique and indicate over the subject of the black box. This directory should contain one file per algorithm usable on the model with the same name as the algorithm (keep Nomad and Ibex written as is). 

## Contributing

Feel free to submit any new model or solver in the GitLab.