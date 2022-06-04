import json



#Reads a Json file and gives the corresponding mbx file plus param.txt for Nomad Optimisation

def LecteurJson(name, annexe, nb_eval):
    
    fileObject = open(name,'r')
    jsonContent = fileObject.read()
    Source = json.loads(jsonContent)
    
    res=[[],[],[],[],[]] #res is a vector containing x0 lower_bounds upper_bounds input_type output_type
    
    Titrembx = str(Source['name'])+'.mbx'
    Output = open(Titrembx, "w")
    
    Output.write("Constants\n")
    
    for c in range(len(Source['constants'])) :
        Output.write(Source['constants'][c]['name']+'='+Source['constants'][c]['value']+';\n')
        
    Output.write("\nVariables\n")
    
    integer=[]
    
    for v in range(len(Source['variables'])) :
        Output.write(Source['variables'][v]['name']+' in ['+Source['variables'][v]['lower_bound']+','+Source['variables'][v]['upper_bound']+'];\n')
        res[0].append(Source['variables'][v]['initial_guess'])
        
        if Source['variables'][v]['integer'] :
            integer.append(Source['variables'][v]['name'])
            
        if annexe :
            res[1].append(Source['variables'][v]['lower_bound'])
            res[2].append(Source['variables'][v]['upper_bound'])
            res[3].append('I' if Source['variables'][v]['integer'] else 'R')
    if not annexe :
        res=res[0]

    Output.write('\nMinimize '+Source['objective_function']+'\n')
    if annexe :
        res[4].append('OBJ')
    
    Output.write('\nConstraints\n')
    
    for i in integer :
        Output.write('integer('+i+');\n')
        if annexe:
            res[4].append('EB')
    
    for c in range(len(Source['constraints'])) :
        Output.write(Source['constraints'][c]['expression']+' '+Source['constraints'][c]['type']+' 0;\n')
        if annexe :
            res[4].append('PB' if Source['constraints'][c]['relaxable'] else 'EB')
    
    Output.write('\nEnd\n')
    
    Output.close()
    fileObject.close()
    
    #Second part, running nomad with previously created mb and txt files.
    
    config = open('nomad2ibex.txt', 'w')
    config.write(Titrembx)
    config.close()
    
    params = WriteInfo(name[:name.find('.')],res,nb_eval) if annexe else 0

    return(params)



#Reads and mbx file and creates a param.txt file for Nomad Optimisation with

def LecteurMbx(name, nb_eval):
    file=open(name,'r')
    res=[[],[],[],[],["OBJ"],[]]
    
    Sections=['Constants','Variables','Minimize','Constraints','End','function']
    Section=None
    
    while Section != 'End' :
        
        line=str(file.readline())
        
        if line == '\n' or line[:2]=='//':
            pass
        elif line[:line.find(" ")] in Sections :
            Section = line[:line.find(" ")]
            if Sections=='function' :
                while line != 'end' :
                    line=str(file.readline())
        else :
            ReadSection(Section,line,res)
    
    config = open('nomad2ibex.txt', 'w')
    config.write(name)
    config.close()
    
    params = WriteInfo(name[:name.find('.')],res,nb_eval)
    
    return(params)



#Reads a section in a mbx file and extract usefull information for the param.txt

def ReadSection(Section,line,res):
    
    if Section == 'Variables':
        
        In=line.find(" in ")
        Start=line.find("[")
        Mid=line.find(",")
        End=line.find("]")
        #print(line, In, Start, Mid, End)
        low = float(line[Start+1:Mid])
        up = float(line[Mid+1:End])
        i_g = (low+up)/2
        res[0].append(i_g)
        res[1].append(low)
        res[2].append(up)
        res[3].append("R")
        res[5].append(str(line[:In]))
        
    elif Section == 'Constraints' :
        
        par=line.find("(")
        
        if line[:par] == 'integer' :
            var = str(line[par+1:line.find(")")])
            i=0
            while res[5][i] != var :
                i+=1
            res[3][i] = 'I'
            res[0][i] = int(res[0][i])
        
        res[4].append("EB")
        
    else :
        
        pass
    
    return(0)



#Creates a param.txt file for Nomad Optimisation using a number of evaluations and a res vector modified by the Lecteur functions

def WriteInfo(name,res,nb_eval):
    params = name+'.txt'
    Infos = open(params,'w')
    Infos.write("DIMENSION       "+str(len(res[0]))+"\n\n")
    Infos.write("BB_EXE          passerelle.exe\n\n")
    Infos.write("BB_OUTPUT_TYPE  ")
    for i in res[4] :
        Infos.write(str(i)+" ")
    Infos.write("\n\nBB_INPUT_TYPE   ( ")
    for i in res[3] :
        Infos.write(str(i)+" ")
    Infos.write(")\n\nX0              ( ")
    for i in res[0] :
        Infos.write(str(i)+" ")
    Infos.write(")\n\nLOWER_BOUND     ( ")
    for i in res[1] :
        Infos.write(str(i)+" ")
    Infos.write(")\n\nUPPER_BOUND     ( ")
    for i in res[2] :
        Infos.write(str(i)+" ")
    Infos.write(")\n\nMAX_BB_EVAL     "+str(nb_eval))
    
    return(params)