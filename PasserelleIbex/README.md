# PasserelleIbex

Welcome to MiNomad, the hybrid optimizer between Nomad and Ibex.

The point of this tool is to use Ibex' method of equation system calculation as a blackbox for Nomad. Indeed, the binary file passerelle takes in inputs the point given by Nomad and gives as an output the evaluation of an objective function and constraints of a mbx file of which name's is written in a nomad2ibex.txt file.

## Using the Passerelle

This tool is highly customizable as you can use only the Nomad "shell" with you own solver as long as your executable prints the output the way Nomad expects it (Objective value followed by the different constraints as "<=0") or change the shell to optimize your own model (as a json representation) with another optimizer.

To use minomad as conceived, you must first compile the passerelle.exe file using the following command 

'''bash
g++ passerelle.cpp `pkg-config --cflags ibex` `pkg-config --libs  ibex`  -std=c++11 -o passerelle.exe
'''

You can then use the command python minomad.py to start using our tool as you will be guided by the python script. The passerelle executable suppose that every variable of your initial guess is AT LEAST precise at the third decimal. If not you'll have to change the prec value to be number of the highest decimal you have a doubt in, in the passerelle.cpp file and recompile it. 

minomad can use a classical minibex file or a model in a suitable json format. What is a suitable .mbx or .json file is for minomad is a file having the same structure as (respectively) Model.mbx and Model.json.

The File Lecteurs.py contains several useful and independant functions : LecteurMbx and LecteurJson.
We will now detail the usage of those functions :

LecteurMbx : Reads a suitable .mbx file together with a number of evaluation to provide a .txt file containing the instructions to conduct a Nomad optimization. As the .txt file requires a starting point, it will be created as the middle of the space for each variable.

LecteurJson : Reads a suitable .json file together with a number of evaluation and a boolean to provide a suitable .mbx file and, if the boolean is true, a .txt file containing the instructions to conduct a Nomad optimization (using the initial guess of the .json file to create the strating point).

## Contributing

Thank you for reading. Please visit the websites of Nomad and Ibex :
Link for Nomad : https://www.gerad.ca/fr/software/nomad/
Link for Ibex  : http://www.ibex-lib.org/

Contributors of the linker : M. Gras, R. Chenouard, J. Bigeon; OGRE and Ecole Centrale de Nantes.
This code is part of the optimization benchmark library : https://gitlab.univ-nantes.fr/chenouard-r/optimizationbenchmarklibrary.git
Please report bugs to maxime.gras@eleves.ec-nantes.fr