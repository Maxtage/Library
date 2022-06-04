# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 11:26:42 2021
    
@author: maxim
"""
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import datetime as dt
#import sys
from scipy.stats import poisson
#from scipy.stats import nbinom
import warnings
warnings.filterwarnings("ignore")

def post(region,seed,n_runs,x0):
    
    if type(x0)==list:
        x=x0
    else :
        filename = x0
        #filename = sys.argv[1]
        file = open(filename, 'r')
        x = file.read().split()
        file.close()

    alpha_exit=float(x[0])
    #n_runs = 500
    #region='PDL'
    rng=np.random.default_rng(seed)
    
    list_regions = {'IDF': 11,'CVL':24, 'BFC':27, 'NOR': 28, 'HDF':32, 'GRE':44, 'PDL':52, 'BRE':53,
                    'NAQ':75, 'OCC':76, 'ARA':84, 'PACA':93}
    # select region
    #region=input("Insert region acronym: ")  #e.g. IDF
    
    code_region = list_regions[region]
    
    # population
    df=pd.read_excel('./input/regional_pop_by_age.xlsx')
    df=df.set_index('Age')
    reg = df.loc[:,(df==code_region).any()]
    pop = reg*1000000
    pop = pop.drop('code')
    
    #name_reg = pop.columns[0] lag
    
    N = pop.sum().iloc[0]  #total population
    
    ages = 4 #number of age classes
    
    #population per age class
    N_c = pop.iloc[0][0]   #children   [0,11) years
    N_t = pop.iloc[1][0]   #teens     [11,19)
    N_a = pop.iloc[2][0]   #adults      [19,65)
    N_s = pop.iloc[3][0]   #seniors     over 65+ 
    
    #print('Region selected: ', name_reg)
    #print('Population:', N)
    
    # epidemiological parameters
    
    incubation = 3.7       # incubation period (days) 
    prodromic = 1.5        # prodromic phase (days)
    infection = 2.3        # infectious period (days)
    
    delta_t = 1   # one timestep = 1 day
    
    # compute transition rates
    sigma=1./incubation
    theta=1./prodromic
    gamma=1./infection    
    
    # fraction of asymptomatic
    asint = 0.4
    p_as = np.array([asint]*ages)
    
    #probability of developing pauci/mild/severe symptoms if not asymptomatic
    # explicit value for each age class
    ps = np.array([1.,1.,0.20,0.20])  
    ms = np.array([0.,0.,0.76,0.53])  
    ss = np.array([0.,0.,0.04,0.27])  
    
    # fraction entering I_ps, I_ms, I_ss compartments
    p_ps = np.multiply(1-p_as, ps)  
    p_ms = np.multiply(1-p_as, ms)
    p_ss = np.multiply(1-p_as, ss)
    
    # relative infectiousness
    r = np.array([0.25,0.55,0.55,0.55]) # explicit value for each age class
    
    # relative susceptibility
    susc = np.array([0.5,0.5,1,1])      # explicit value for each age class
    
    # read results of calibration pre-LD and LD
    
    # beta, lag (pre-lockdown), delay, alpha_LD (during lockdown)
    
    params=pd.read_excel("./input/params.xlsx")
    params=params[params["region"]==code_region]
    params=params.reset_index()
    
    # contact matrices
    
    #function to read matrix
    def read(df):
        C = []
        for i in range(ages*ages):
            c = df[0][i]
            C.append(c)
        C = np.array(C)
        C = np.reshape(C, (ages,ages))
        return C 
    
    #function to compute contact matrices w/ testing
    def extract_matrix(matrix, x_test_a,x_test_s):
        m_p = read(matrix) # for cases in the prodromic phase
        m_as = x_test_a*read(matrix)*0.1 + (1-x_test_a)*read(matrix) # apply testing for asymptomatic cases
        m_t = x_test_s*read(matrix)*0.1 + (1-x_test_s)*read(matrix)  # apply testing for pauci-symptomatic and mild cases
        m_ss = x_test_s*read(matrix)*0.1 + (1-x_test_s)*read(matrix)*0.25  # testing for severe cases
    
        return m_p,m_as,m_t,m_ss
    
    weeks=[20,21,22,23,24,25,26,27]
    
    def seirh(u, parms, t, intervention, LD, exit, scale1, scale2,
             BS_p, BS_as, BS_t, BS_ss,
             LD_p, LD_as, LD_t, LD_ss, 
             EX_p, EX_as, EX_t, EX_ss):
        
        """
        Simulation one time step (day) of the compartmental, age-stratified model.
        INPUT
        u: dict containing the number of individuals (incidence and prevalence) for each compartment in the previous timestep
        parms: list of epidemiological parameters
        t: current timestep
        intervention: boolean indicating if an intervention measure (e.g. lockdown) is put in place
        LD: list containing the timesteps corresponding to start and end of lockdown
        exit: list of lists containing the timesteps corresponding to start and end of each week after lifting lockdown
        scale1: scaling factor of the pre-LD transmission rate, fitted during lockdown (called alpha_LD in the paper)
        scale2: scaling factor of the pre-LD transmission rate, fitted after lifting lockdown (called alpha_exit in the paper)
        BS_p, BS_as, BS_t, BS_ss: contact matrices in the pre-lockdown phase
        LD_p, LD_as, LD_t, LD_ss: contact matrices during lockdown
        EX_p, EX_as, EX_t, EX_ss: contact matrices in the post-lockdown phase
        RETURNS: updated version of dict u
        """
    
        #quantities of interest
        S = u['S']
        new_E = u['Y_E']
        E = u['E']
        new_I_p = u['Y_I_p']  
        I_p = u['I_p'] 
        new_I_as = u['Y_I_as'] 
        I_as = u['I_as'] 
        new_I_ps = u['Y_I_ps'] 
        I_ps = u['I_ps'] 
        new_I_ms = u['Y_I_ms'] 
        I_ms = u['I_ms'] 
        new_I_ss = u['Y_I_ss'] 
        I_ss = u['I_ss'] 
        new_H = u['Y_H'] 
        H = u['H'] 
        new_R = u['Y_R'] 
        R = u['R'] 
        N_tot = u['N_tot'] 
    
        # epidemiological parameters
        bet, sigm, thet, gamm, N, dt = parms
        
        # contact matrices
        
        # pre-lockdown
        C_p = BS_p 
        C_as = BS_as
        C_t = BS_t
        C_ss = BS_ss        
        
        if intervention:
            for i in range(len(LD)):
                LD_start = LD[i][0]
                LD_end = LD[i][1]
                # during lockdown
                if (t >= LD_start) and (t < LD_end): 
                    C_p = LD_p*scale1
                    C_as = LD_as*scale1
                    C_t = LD_t*scale1
                    C_ss = LD_ss*scale1
            for week in range(len(weeks)):
                # post-lockdown, contact matrix changed every week
                start_week = exit[week][0]
                end_week = exit[week][1]
                if (t >= start_week) and (t < end_week): 
                    C_p = EX_p[week]*scale2[week]
                    C_as = EX_as[week]*scale2[week]
                    C_t = EX_t[week]*scale2[week]
                    C_ss = EX_ss[week]*scale2[week]
                        
        # force of infection
        lambd = []
        for age in range(ages):
            l = 0 
            for age2 in range(ages):
                l += susc[age]*r[age2]*bet*C_p[age,age2]*I_p[age2]/N
                l += susc[age]*r[age2]*bet*C_as[age,age2]*I_as[age2]/N
                l += susc[age]*r[age2]*bet*C_t[age,age2]*I_ps[age2]/N
                l += susc[age]*bet*C_t[age,age2]*I_ms[age2]/N
                l += susc[age]*bet*C_ss[age,age2]*I_ss[age2]/N
            lambd.append(l)
        lambd = np.array(lambd)
    
        # compute transition probabilities for entering in each comparment
        in_E = 1 - np.exp(-lambd*dt)
        in_I_p = np.array([sigm*dt]*ages)
        in_I = np.array([thet*dt]*ages)
        in_R = np.array([gamm*dt]*ages)
        in_H = np.array([gamm*dt]*ages)
        
        # transition events (sampled by binomial or multinomial distributions with corresponding transition probabilities)
        for age in range(ages):
            #transitions
            new_E[age] = rng.binomial(S[age],in_E[age])
            new_I_p[age] = rng.binomial(E[age],in_I_p[age])
            
            trans_I = np.array([p_as[age]*in_I[age], p_ps[age]*in_I[age], p_ms[age]*in_I[age], p_ss[age]*in_I[age], 1-in_I[age]])
            new_I_as[age], new_I_ps[age], new_I_ms[age], new_I_ss[age], res = rng.multinomial(I_p[age],trans_I)
            
            recovery_as = rng.binomial(I_as[age],in_R[age])
            recovery_ps = rng.binomial(I_ps[age],in_R[age])
            recovery_ms = rng.binomial(I_ms[age],in_R[age])
            
            new_H[age] = rng.binomial(I_ss[age], in_H[age])   
            recovery_h = rng.binomial(H[age], in_R[age])
                    
            new_R[age] = recovery_as + recovery_ps + recovery_ms + recovery_h 
            
            #update compartments
            S[age] = S[age] - new_E[age] 
            E[age] = E[age] + new_E[age] - new_I_p[age]
            I_p[age] = I_p[age] + new_I_p[age] - new_I_as[age] - new_I_ps[age] - new_I_ms[age] - new_I_ss[age]
            I_as[age] = I_as[age] + new_I_as[age] - recovery_as
            I_ps[age] = I_ps[age] + new_I_ps[age] - recovery_ps
            I_ms[age] = I_ms[age] + new_I_ms[age] - recovery_ms
            I_ss[age] = I_ss[age] + new_I_ss[age] - new_H[age] 
            H[age] = H[age] + new_H[age] - recovery_h
            R[age] = R[age] + new_R[age]
            N_tot[age] = S[age]+E[age]+I_p[age]+I_as[age]+I_ps[age]+I_ms[age]+I_ss[age]+H[age]+R[age]
       
        return  {'t':t, 'S': S, 'E':E, 'I_p':I_p, 'I_as':I_as,'I_ps':I_ps,'I_ms':I_ms,'I_ss':I_ss,
                'H':H,'R':R,'Y_E':new_E,'Y_I_p':new_I_p,'Y_I_as':new_I_as,
                'Y_I_ps':new_I_ps, 'Y_I_ms':new_I_ms, 'Y_I_ss':new_I_ss, 'Y_H':new_H,'Y_R':new_R,'N_tot':N_tot}
    
    def simulate(intervention, LD, exit, scale1, scale2,
                 BS_p, BS_as, BS_t, BS_ss,
                 LD_p, LD_as, LD_t, LD_ss, 
                 EX_p, EX_as, EX_t, EX_ss):
        
        """
        Simulation of one single stochastic run of the compartmental, age-stratified model.
        INPUT
        intervention: boolean indicating if an intervention measure (e.g. lockdown) is put in place
        LD: list containing the timesteps corresponding to start and end of lockdown
        exit: list of lists containing the timesteps corresponding to start and end of each week after lifting lockdown
        scale1: scaling factor of the pre-LD transmission rate, fitted during lockdown 
        scale2: scaling factor of the pre-LD transmission rate, fitted after lifting lockdown
        BS_p, BS_as, BS_t, BS_ss: contact matrices in the pre-lockdown phase
        LD_p, LD_as, LD_t, LD_ss: contact matrices during lockdown
        EX_p, EX_as, EX_t, EX_ss: contact matrices in the post-lockdown phase
        RETURNS: dict containing the number of individuals for each compartment, for each timestep
        """
        
        parms = [beta, sigma, theta, gamma, N, delta_t]
        
        tf = t_stop
        
        t = np.arange(tf)
        S = np.zeros((tf,ages))
        E = np.zeros((tf,ages))
        I_p = np.zeros((tf,ages))   
        I_as = np.zeros((tf,ages))
        I_ps = np.zeros((tf,ages)) 
        I_ms = np.zeros((tf,ages))
        I_ss = np.zeros((tf,ages))
        H = np.zeros((tf,ages))
        R = np.zeros((tf,ages))
        
        Y_E = np.zeros((tf,ages))
        Y_I_p = np.zeros((tf,ages))
        Y_I_as = np.zeros((tf,ages))
        Y_I_ps = np.zeros((tf,ages))
        Y_I_ms = np.zeros((tf,ages))
        Y_I_ss = np.zeros((tf,ages))
        Y_H = np.zeros((tf,ages))
        Y_R = np.zeros((tf,ages))
    
        N_tot = np.zeros((tf,ages))
        
        result = {'t':t, 'S': S, 'E':E, 'I_p':I_p, 'I_as':I_as,'I_ps':I_ps,'I_ms':I_ms,'I_ss':I_ss,
                  'H':H,'R':R,'Y_E':Y_E,'Y_I_p':Y_I_p,'Y_I_as':Y_I_as,'Y_I_ps':Y_I_ps, 
                  'Y_I_ms':Y_I_ms, 'Y_I_ss':Y_I_ss,'Y_H':Y_H,'Y_R':Y_R,'N_tot':N_tot}
    
        #initial condition
        u = {'t':0, 'S': [N_c,N_t,N_a-I_seed,N_s], 'E':[0]*ages,'I_p':[0,0,I_seed,0],
             'I_as':[0]*ages,'I_ps':[0]*ages,'I_ms':[0]*ages,'I_ss':[0]*ages,'H':[0]*ages,'R':[0]*ages,
             'Y_E':[0]*ages,'Y_I_p':[0]*ages,'Y_I_as':[0]*ages,'Y_I_ps':[0]*ages, 'Y_I_ms':[0]*ages, 'Y_I_ss':[0]*ages, 
             'Y_H':[0]*ages,'Y_R':[0]*ages,'N_tot':[N_c,N_t,N_a,N_s]}   
    
        #save initial condition
        for c in result.keys():
            result[c][0] = u[c]
        
        for j in range(1,tf):
            #run one step of the transmission model
            u = seirh(u,parms,t[j],intervention, LD, exit, scale1, scale2,
                     BS_p, BS_as, BS_t, BS_ss,
                     LD_p, LD_as, LD_t, LD_ss, 
                     EX_p, EX_as, EX_t, EX_ss)
            #save the result 
            for c in result.keys():
                result[c][j] = u[c]
                
        return result 
    
    def run_simulation(intervention = False, LD = [[0,0]], 
                       scale1=0,scale2=0,x_test_a=0,x_test_s=0):
        
        """
        Simulation of multiple stochastic runs of the compartmental, age-stratified model.
        INPUT
        intervention: boolean indicating if an intervention measure (e.g. lockdown) is put in place
        LD: list containing the timesteps corresponding to start and end of lockdown
        scale1: scaling factor of the pre-LD transmission rate, fitted during lockdown 
        scale2: scaling factor of the pre-LD transmission rate, fitted after lifting lockdown
        x_test_a: fraction of asymptomatic cases tested and put in isolation
        x_test_s: fraction of symptomatic cases tested and put in isolation
        RETURNS: dict containing the number of individuals for compartments of interest (e.g. incidence in the hospital compartment), for each timestep, for each run
        """
        
        out_Y_H = pd.DataFrame(np.arange(t_stop))
        out_Y_Ias = pd.DataFrame(np.arange(t_stop))
        out_Y_Ips = pd.DataFrame(np.arange(t_stop))    
        out_Y_Ims = pd.DataFrame(np.arange(t_stop))    
        out_Y_Iss = pd.DataFrame(np.arange(t_stop))    
    
        # read matrices 
        
        #pre-lockdown
        BS_h = pd.read_table('./input/matrices/baseline.txt', header = None, sep=' ')
        BS_p, BS_as, BS_t, BS_ss = extract_matrix(BS_h,x_test_a=0,x_test_s=0)
     
        #lockdown
        LD_h = pd.read_table('./input/matrices/LD/LD_region_'+str(code_region)+'.txt', header = None, sep=' ')
        LD_p, LD_as, LD_t, LD_ss = extract_matrix(LD_h,x_test_a=0,x_test_s=0)
        
        #post-lockdown
        EX_h={}
        for week,ttt in enumerate(weeks):
            path_matrix='./input/matrices/exit/region_'+str(code_region)+'_week_'+str(ttt)+'.txt'
            EX_h[week]=pd.read_table(path_matrix, header = None, sep=' ')
    
        one_week=7
        TW = [[0 for col in range(2)] for row in range(len(weeks))]
        for i in range(len(weeks)):
            TW[i][0]=m_11+i*one_week
            TW[i][1]=m_11+(i+1)*one_week
        
        EX_p={}
        EX_as={}
        EX_t={}
        EX_ss={}
        for week,ttt in enumerate(weeks):
            EX_p[week], EX_as[week], EX_t[week], EX_ss[week] = extract_matrix(EX_h[week],x_test_a=x_test_a[week],x_test_s=x_test_s[week])
      
        #for each run
        for n in range(n_runs):
            out = simulate(intervention, LD, TW, scale1,scale2,
                           BS_p, BS_as, BS_t, BS_ss,
                           LD_p, LD_as, LD_t, LD_ss, 
                           EX_p, EX_as, EX_t, EX_ss)
            # extract quantities of interest, e.g. admission to hospital, all age classes
            # save the timeseries in the column of a dataframe         
            out_Y_H[n] = pd.DataFrame(out['Y_H']).sum(axis=1)
            out_Y_Ias[n] = pd.DataFrame(out['Y_I_as']).sum(axis=1)
            out_Y_Ips[n] = pd.DataFrame(out['Y_I_ps']).sum(axis=1)
            out_Y_Ims[n] = pd.DataFrame(out['Y_I_ms']).sum(axis=1)
            out_Y_Iss[n] = pd.DataFrame(out['Y_I_ss']).sum(axis=1)
            
        return {'adm_H':out_Y_H,'new_Ias':out_Y_Ias,'new_Ips':out_Y_Ips,'new_Ims':out_Y_Ims,'new_Iss':out_Y_Iss}
    
    def add_median_CI(DF):
        df = DF.copy()
        df['p1'] = df[[i for i in range(n_runs)]].quantile(0.025, axis=1)
        df['median'] = df[[i for i in range(n_runs)]].median(axis=1)  
        df['p2'] = df[[i for i in range(n_runs)]].quantile(0.975, axis=1)
        return df
    
    data = pd.read_csv(r'./input/hospitalizations_by_region.csv')
    H_adm = data[data.reg==code_region][['date','hosp_obs']]
    H_adm.columns = ['date','obs']
    H_adm = H_adm.reset_index(drop=True)
    
    #DETECTED CASES (w\complete info + missing data)
    
    detected=pd.read_csv('./input/detected_cases.csv')
    detected=detected[detected['region']==code_region]
    detected=detected[detected['week']<=27]
    
    I_seed = 10  # initial number of infected (adults in I_p compartment)
    
    beta=params["beta"][0]
    lag=params["lag"][0]    #number of days before March 1
    delay=params["delay"][0]
    scale1=params["alpha_LD"][0]
    
    #calendar=pd.DataFrame(pd.date_range(dt.date(2020, 3, 1)-dt.timedelta(days=int(lag)), periods=365)) 
    
    # timesteps for lockdown start and end date (March 17 - May 11, 55 days)
    start_ld = lag + 16  
    m_11 = start_ld + 55  
    
    t_stop = len(H_adm) + lag #number of (daily) timesteps
    
    # Read 8 values in [0,1] of weekly detection probability, for sympt and asympt cases.
    # if n=0, initialize with probability = 0.5
    # if n>0, inform with the detection probability computed at timestep n-1
    
    #n = int(input('Insert current iteration number: n= '))
    n=0
    
    if n:
        try:
            test_asymp = pd.read_table('./output/region_{}_input_iteration_{}_asympt.txt'.format(code_region,n-1), header = None, sep=' ')[0].values
            test_sympt = pd.read_table('./output/region_{}_input_iteration_{}_sympt.txt'.format(code_region,n-1), header = None, sep=' ')[0].values
        except FileNotFoundError:
            #print ('FILES NOT FOUND! I am not finding the output files of the previous iteration, so I am assuming n=0.')
            n = 0    
            test_asymp, test_sympt = np.array([0.5]*8), np.array([0.5]*8)
    else:
        test_asymp, test_sympt = np.array([0.5]*8), np.array([0.5]*8)
        
    #n_runs = int(input('Choose number of stochatic runs: ')) #500 stochastic runs were used in the paper
    
    #alpha_exit = float(input('Choose value of alpha_exit: '))  #explore values of the scaling factor 
    
    output = run_simulation(intervention=True,LD=[[start_ld+delay,m_11]],
                         scale1=scale1,scale2=[alpha_exit for i in range(len(weeks))],
                         x_test_a=test_asymp,  # % testing informed from the detection probability
                         x_test_s=test_sympt)  # % testing informed from the detection probability
    median_adm_H = add_median_CI(output['adm_H'])['median']
    p=0
    for t in range(71,len(H_adm['obs'])): # considet hospitalization data from May 11 
        #compute log likelihood
        p += poisson.logpmf(H_adm['obs'].iloc[t], mu=median_adm_H.iloc[t+lag])
    #print('Loglikelihood with alpha_exit = {} :'.format(alpha_exit),p)
    f=-p
    print(f)