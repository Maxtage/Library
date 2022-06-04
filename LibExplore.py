import PyNomad
import subprocess
import argparse
import sys
import os
import shutil
#import MiNomad.py as MN
#import Lecteurs.py as L
from PasserelleIbex.Lecteurs import LecteurJson


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, prog='Library Explorer', add_help=False)
parser.add_argument('M', type=str, nargs='?', help='The name of the model to launch. To display the list of the models, type "python LibExplore.py -l".')
parser.add_argument('-h', '--help', action='store_true', help='Show help and exit')
parser.add_argument('-i', '--info', action='store_true', help='Show information about the program')
parser.add_argument('-l', '--list', action='store_true', help='Display the list of the models available in the library.')

args = parser.parse_args()

Models=[m for m in os.listdir("Modèles")]

#Define the function to call the suitable algorithm for the desired model

def call_algo(algo,model,algos):
    if algo=="Ibex":
        active="None"
        files=[f for f in os.listdir("Modèles/"+model+"/Ibex/")]
        for f in files :
            if f[f.find('.'):]==".mbx" :
                active=f
        if active=="None" :
            for f in files :
                if f[f.find('.'):]==".json" :
                    active=f
            if active=="None" :
                print('The model has no Minibex or Json file.')
            else :
                LecteurJson(active,True,0)
                with open('nomad2ibex.txt','r') as line :
                    active = line.readline()
                os.remove('nomad2ibex.txt')
                os.replace(active,"Modèles/"+model+"/Ibex/")
                print('A Minibex file was created from a Json file and will be used for optimization.')
        if active!="None" :
            rigor=bool(input('Should rigor mod be activated (default True) ? True/False : ') or True)
            time=int(input('Number of seconds allowed for optimization (default 600) : ') or 600)
            if rigor :
                print(subprocess.Popen(["ibexopt","Modèles/"+model+"/Ibex/"+active,"--trace","--rigor","-t"+str(time)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True).communicate()[0])
            else :
                print(subprocess.Popen(["ibexopt","Modèles/"+model+"/Ibex/"+active,"--trace","-t"+str(time)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True).communicate()[0])
    
    if algo=="Nomad":
        active="None"
        files=[f for f in os.listdir("Modèles/"+model+"/Nomad/")]
        for f in files :
            if f[f.find('.')-3:]=="opt.py" :
                active=f
        if active=="None" :
            for f in files :
                if f=="param.txt" :
                    active=f
            if active=="None" :
                if "Ibex" in algos :
                    files=[f for f in os.listdir("Modèles/"+model+"/Ibex/")]
                    for f in files :
                        if f[f.find('.'):]==".mbx" :
                            active=f
                    if active=="None" :
                        for f in files :
                            if f[f.find('.'):]==".json" :
                                active=f
                    if active=="None" :
                        print('The model has no optimization file for Ibex or Nomad. A simulation file sim.py might be available in its file and can be run with "python [name_of_sim.py_file]"')
                    else :
                        shutil.move("PasserelleIbex/MiNomad.py",os.getcwd())
                        shutil.move("PasserelleIbex/Lecteurs.py",os.getcwd())
                        shutil.move("PasserelleIbex/passerelle.exe",os.getcwd())
                        shutil.move("Modèles/"+model+"/Ibex/"+active,os.getcwd())
                         
                        nb_runs=int(input('Number of Nomad runs allowed for optimization (default 100) : ') or 100)
                        os.system("python MiNomad.py -file="+active+" -nb_eval="+str(nb_runs))
                        
                        shutil.move(active,"Modèles/"+model+"/Ibex")
                        shutil.move("MiNomad.py","PasserelleIbex")
                        shutil.move("Lecteurs.py","PasserelleIbex")
                        shutil.move("passerelle.exe","PasserelleIbex")
                            
                        os.remove("nomad2ibex.txt")
                        os.remove(active[:active.find('.')]+".txt")
                            
                        if active[active.find('.'):]=='.json' :
                            os.remove(active[:active.find('.')]+".mbx")
                else :    
                    print('The model has no param.txt or opt.py file. A simulation file sim.py might be available in its file and can be run with "python [name_of_sim.py_file]"')
            else :
                print('A param.txt file was found and will be launched. If the optimization seems to fail, the starting point might not be suitable. Please check if there is any sim.py or pdf (in a Doc file) for this model.')
                os.chdir("Modèles/"+model+"/Nomad")
                params=[]
                with open(active) as P:
                    for line in P:
                        if line == "\n":
                            pass
                        else :
                            line=line[:line.find("#")].replace('\n','')
                            params.append(line.replace('\t',' '))
                print(params)
                PyNomad.optimizeWithMainStep(params)
                os.chdir("../../../")
        else :
            print('A opt.py file was found and will be launched. For more information, please run the sim.py file with "python [name_of_sim.py_file]"')
            os.chdir("Modèles/"+model+"/Nomad")
            os.system("python "+active)
            os.remove("run.py")
            os.chdir("../../../")
    return 0

#Body of the parser
        
if not len(sys.argv) > 1:
    print('\nRun LibExplore : python LibExplore M=name_of_the_model\n'
          '\n                 M : Name of a file in the Modèles directory. Contains all the information and programs relative to a model.\n'
          '\nList of the models : python LibExplore -l\n',
          '\n              Help : python LibExplore -h\n',
          '\n              Info : python LibExplore -i\n')
        
elif args.list :
    print('The available models are : ')
    for m in Models :
        if m.find('.')==-1 and m!="Template":
            print(m)
            
elif args.info :
    print('LibExplore, the tool too explore and run preset instances of the Optimization Benchmark Library models, version 0.1, 2022-03-02\n\n',
          'Contributors of the wrapper : M. Gras, S. Le Digabel, L. Salomon; GERAD and Polytechnique Montreal.\n\n',
          'This code is part of the optimization benchmark library : https://gitlab.univ-nantes.fr/chenouard-r/optimizationbenchmarklibrary.git \n\n',
          'Please report bugs to maxime.gras@eleves.ec-nantes.fr')

elif not(args.help) :
    
    model=args.M
    have=False
    for m in Models :
        if m==model :
            have=True
    if not have :
        print('Error : Model '+model+' unrecognized. Please check writing and consult the list of models with "python LibExplore.py -l".')
    else :
        algos=["Ibex","Nomad"]
        algos_avail=[]
        for file in os.listdir("Modèles/"+model):
            if file in algos :
                algos_avail.append(file)
        if len(algos_avail)==0:
            print('Error : No algorithm available for this model.')
        elif len(algos_avail)==1:
            call_algo(algos_avail[0],model,algos_avail)
        else:
            print(algos_avail)
            choice=input("Are the available algorithms, please choose one : ")
            call_algo(choice,model,algos_avail)
            
else :
    print('LibExplore, the tool too explore and run preset instances of the Optimization Benchmark Library models, version 0.1, 2022-03-02\n\n',
          'You have launched the help of the explorer for the Optimization Benchmark Library.',
          'This module aims to launch the default instances of the desired black or white box of the Library.',
          'To run a model, simply type "python LibExplore.py name_of_the_model"',
          'If more than one algorithm is available for the model, you will be asked which one to use.'
          'To have the name of each model available type "python LibExplore.py -l"')