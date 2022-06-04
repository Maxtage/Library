import argparse
import sys
import Lecteurs as L
import PyNomad

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, prog='Ibex and Nomad hybrid optimizer', add_help=False)
parser.add_argument('-file', type=str, help='Give the program used as a base for the optimisation. Can either be a minibex or a Json file. If a minibex is provided, some other information will be required')
parser.add_argument('-add_info', type=str, default='default', help='Gives a custom param.txt file for nomad optimisation. If no file are give, a default file will be created from the mbx or json file given')
parser.add_argument('-nb_eval', type=int, default=100, help='Choose the number of Nomad evaluation. The default value is set at 100. Please not that this value will be overwritten if a custom param.txt file is provided.')
parser.add_argument('-h', '--help', action='store_true', help='Show help and exit')
parser.add_argument('-i', '--info', action='store_true', help='Show information about the program')
args = parser.parse_args()

if not len(sys.argv) > 1:
    print("""\nRun minomad : python minomad -file=... """,
          """\nRun minomad (custom) : python minomad -file=... -add_info=... -nb_eval=...\n""",
          """\n\tfile     : name of the file containing the model. Can either be a suitable json or mbx file. What a suitable file is is explained in the help. type python minomad.py -help""",
          """\n\tadd_file : name of a .txt file containing custom instructions for Nomad Optimisation. If no file is given, one will be created by default.""",
          """\n\tnb_eval  : number of evaluation of the objective function authorized by Nomad. Defalut value is 100.\n""",
          """\nHelp : minomad -h \n""",
          """\nInfo : minomad -i \n""")
elif args.info :
    print("""MinNomad, the link between Nomad and Ibex, version 0.1, 2022-01-19\n\n""",
          """The program uses Nomad, the GERAD tool for optimisation and Ibex, the OGRE tool for optimisation\n\n""",
          """Link for Nomad : https://www.gerad.ca/fr/software/nomad/ \n""",
          """Link for Ibex  : http://www.ibex-lib.org/ \n\n""",
          """Contributors of the wrapper : M. Gras, S. Le Digabel, L. Salomon; GERAD and Polytechnique Montreal.\n\n""",
          """This code is part of the optimization benchmark library : https://gitlab.univ-nantes.fr/chenouard-r/optimizationbenchmarklibrary.git \n\n""",
          """Please report bugs to maxime.gras@eleves.ec-nantes.fr""")
else:
    
    if not(args.help) and args.file[(args.file).find("."):]=='.json':
        
        #params = L.LecteurJson(args.file, True, args.nb_eval) 
        
        #params = args.add_info if args.add_info != 'default' else params
        
        params = args.add_info if args.add_info != 'default' else L.LecteurJson(args.file, True, args.nb_eval)
        
        params_line=[]
        
        with open(params) as P:
            for line in P:
                if line == "\n":
                    pass
                else :
                    line=line[:line.find("/")]
                    params_line.append(line)
        
        PyNomad.optimizeWithMainStep(params_line)
        
    elif not(args.help) and args.file[(args.file).find("."):]=='.mbx':
        
        #params = L.LecteurMbx(args.file, args.nb_eval) 
        
        #params = args.add_info if args.add_info != 'default' else params
        
        params = args.add_info if args.add_info != 'default' else L.LecteurMbx(args.file, args.nb_eval)
        
        params_line=[]
        
        with open(params) as P:
            for line in P:
                if line == "\n":
                    pass
                else :
                    line=line[:line.find("/")]
                    params_line.append(line)
        
        PyNomad.optimizeWithMainStep(params_line)
        
    else :
        print("""minomad, the link between Nomad and Ibex, version 0.1, 2022-01-19\n\n""",
              """The program uses Nomad, the GERAD tool for optimisation and Ibex, the OGRE tool for optimisation\n\n""",
              """Link for Nomad : https://www.gerad.ca/fr/software/nomad/ \n""",
              """Link for Ibex  : http://www.ibex-lib.org/ \n\n""",
              """Run simulation : python minomad.py -file=... -add_info=... -nb_eval=... \n\n""",
              """    file : Model optimised : the name of a suitable .mbx or .json suitable file. A suitable file is one derived from the file Template.mbx or Template.json\n\n""",
              """add_info : facultative option : .txt file usable by Nomad. The file is compose of lines with a flag and its values.\n""",
              """           Example of line : FLAG_NOMAD   value_of_the_flag\n""",
              """           The following flags are required for any custom param file :\n""",
              """              DIMENSION        (number of variables)\n""",
              """              BB_EXE           (name of the executable file (You can use the executable PasserelleIbex to use a mbx file provided you have a nomad2ibex.config file containing the name of the .mbx file))\n""",
              """              BB_OUTPUT_TYPE   (gives the number of outputs and their type between OBJ (objective function) PB (relaxable constraint) and EB (unrelaxable coonstraint) separated by spaces.)\n""",
              """              X0               (initial guess of the variables in order and separated by spaces.)\n""",
              """              LOWER_BOUND      (lower bounds of the variable in order and separated by spaces)\n""",
              """              UPPER_BOUND      (upper bounds of the variable in order and separated by spaces)\n""",
              """              MAX_EVAL         (number of evaluation in Nomad)\n\n""",
              """ nb_eval : Number of Nomad iterations\n""",
              """           The default number in 100\n""",
              """           Caution is required as you modify this value as it can drastically increase the execution time.\n""",
              """\nFor more information on the flags available in Nomad, please read the complete list of parameters : https://nomad-4-user-guide.readthedocs.io/en/latest/Appendix.html#appendix-parameters""")
        