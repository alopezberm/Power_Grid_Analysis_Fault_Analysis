"""
    ======================================================================================
    46705 Power Grid Analysis - DTU
    Assignment 2: Fault Analysis
    Group: 15

    DESCRIPTION:
    This master script performs a comprehensive fault analysis for a multi-bus 
    transmission system using the Z-bus impedance matrix method. It covers:
    - Sequence Network Construction: Building positive, negative, and zero-sequence 
      admittance (Y-bus) and impedance (Z-bus) matrices.
    - Fault Calculations: Implementation of analytical models for Symmetrical 
      (3-Phase) and Asymmetrical (SLG, LL, DLG) faults.
    - Transformer & Grounding Analysis: Modeling the impact of various transformer 
      winding connections and generator neutral grounding configurations.
    - Parametric Studies: Sensitivity analysis regarding fault impedance (Zf) and 
      pre-fault voltage levels (Vf) on short-circuit current magnitudes.
    ======================================================================================
"""

import numpy as np
import re
import csv
import FaultAnalysis_46705 as fa
import LoadNetworkData4FA as lnd4fa
import ReadNetworkData as rd4fa

# 1. the FaultAnalysis() function
def FaultAnalysis(Zbus0,Zbus1,Zbus2,bus_to_ind,fault_bus,fault_type,Zf,Vf):
   
    # calculate sequence fault currents
    Iseq = Calculate_Sequence_Fault_Currents(Zbus0,Zbus1,Zbus2,bus_to_ind,fault_bus,fault_type,Zf,Vf)
    # calculate sequence fault voltages
    Vseq_mat = Calculate_Sequence_Fault_Voltages(Zbus0,Zbus1,Zbus2,bus_to_ind,fault_bus,Vf,Iseq)
    # convert sequence currents to phase (fault) currents
    Iph = Convert_Sequence2Phase_Currents(Iseq)
    # convert sequence voltages to phase line-to-ground (fault) voltages
    Vph_mat = Convert_Sequence2Phase_Voltages(Vseq_mat)    
    return Iph, Vph_mat

# 1.1. the Calculate_Sequence_Fault_Currents() function
def Calculate_Sequence_Fault_Currents(Zbus0,Zbus1,Zbus2,bus_to_ind,fault_bus,fault_type,Zf,Vf):
#  fault_type: 0 = 3-phase balanced fault; 1 = Single Line-to-Ground fault;
#              2 = Line-to-Line fault;     3 = Double Line-to-Ground fault.    
    # Iseq current array: 
    # Iseq[0] = zero-sequence; Iseq[1] = positive-sequence; Iseq[2] = negative-sequence
    Iseq = np.zeros(3,dtype=complex)
    fb = bus_to_ind[fault_bus]
    if fault_type == 0:
        # 3-Phase balanced fault: Only positive sequence network is involved
        Iseq[1] = Vf / (Zbus1[fb, fb] + Zf)
    elif fault_type == 1:
        # Single Line-to-Ground (SLG): Sequence networks connected in series
        Iseq[0] = Vf / (Zbus0[fb, fb] + Zbus1[fb, fb] + Zbus2[fb, fb] + 3*Zf)
        Iseq[1] = Iseq[0]
        Iseq[2] = Iseq[0]        
    elif fault_type == 2:
        # Line-to-Line (LL): Positive and Negative networks connected in parallel (Zero sequence is 0)
        Iseq[1] = Vf / (Zbus1[fb, fb] + Zbus2[fb, fb] + Zf)
        Iseq[2] = -Iseq[1]
    elif fault_type == 3:
        # Double Line-to-Ground (DLG): All three sequence networks connected in parallel
        Z0_eq = Zbus0[fb, fb] + 3*Zf
        Iseq[1] = Vf / (Zbus1[fb, fb] + (Zbus2[fb, fb] * Z0_eq) / (Zbus2[fb, fb] + Z0_eq))
        Iseq[2] = -Iseq[1] * Z0_eq / (Zbus2[fb, fb] + Z0_eq)
        Iseq[0] = -Iseq[1] * Zbus2[fb, fb] / (Zbus2[fb, fb] + Z0_eq)
    else:
        print('Unknown Fault Type')
    return Iseq

# 1.2 the Calculate_Sequence_Fault_Voltages() function
def Calculate_Sequence_Fault_Voltages(Zbus0,Zbus1,Zbus2,bus_to_ind,fault_bus,Vf,Iseq):
    N = len(Zbus1) # Number of buses
    Vseq_mat = np.zeros((N, 3), dtype=complex)
    fb = bus_to_ind[fault_bus]
    
    # Calculate voltages for all buses using the Zbus matrices and injected fault currents
    # Vseq_mat[:, 0] = Zero sequence, Vseq_mat[:, 1] = Positive sequence, Vseq_mat[:, 2] = Negative sequence
    Vseq_mat[:, 0] = -Zbus0[:, fb] * Iseq[0]
    Vseq_mat[:, 1] = Vf - Zbus1[:, fb] * Iseq[1]
    Vseq_mat[:, 2] = -Zbus2[:, fb] * Iseq[2]
    return Vseq_mat

# 1.3. the Convert_Sequence2Phase_Currents() function
def Convert_Sequence2Phase_Currents(Iseq):
    # Fortescue Transformation Matrix (A)
    a = np.exp(1j * 2 * np.pi / 3)
    A_mat = np.array([[1, 1, 1], 
                      [1, a**2, a], 
                      [1, a, a**2]])
    # Convert sequence currents to phase currents: Iph = A * Iseq
    Iph = np.dot(A_mat, Iseq)
    return Iph

# 1.4 the Convert_Sequence2Phase_Voltages() function
def Convert_Sequence2Phase_Voltages(Vseq_mat):
    N = len(Vseq_mat)
    Vph_mat = np.zeros((N, 3), dtype=complex)
    
    # Fortescue Transformation Matrix (A)
    a = np.exp(1j * 2 * np.pi / 3)
    A_mat = np.array([[1, 1, 1], 
                      [1, a**2, a], 
                      [1, a, a**2]])
                      
    # Apply transformation to every bus: Vph = A * Vseq
    for i in range(N):
        Vph_mat[i] = np.dot(A_mat, Vseq_mat[i])
    return Vph_mat

# ####################################################
# #  Displaying the results in the terminal window   #
# ####################################################
# 2. the DisplayFaultAnalysisResults() function
def DisplayFaultAnalysisResults(Iph,Vph_mat,fault_bus,fault_type,Zf,Vf):
    print('='*88)
    print('|' + 'Fault Analysis Results'.center(86) + '|')
    print('='*88)

    fault_names = {0: '3-phase balanced fault', 1: 'Single Line-to-Ground fault', 2: 'Line-to-Line fault', 3: 'Double Line-to-Ground fault'}
    
    print('|' + f' Fault Type         :  {fault_names.get(fault_type, "Unknown")}'.ljust(86) + '|')
    print('|' + f' Faulted Bus        :  {fault_bus}'.ljust(86) + '|')
    print('|' + f' Fault Impedance    :  {Zf} pu'.ljust(86) + '|')
    print('|' + f' Prefault Voltage   :  {Vf} pu'.ljust(86) + '|')
    print('='*88)
    
    print('|' + ' --> FAULT CURRENTS (Phase a, b, c) at the fault location:'.ljust(86) + '|')
    phases = ['a', 'b', 'c']
    for i in range(3):
        mag = np.abs(Iph[i])
        ang = np.angle(Iph[i], deg=True)
        print('|' + f'     I_{phases[i]} = {mag:10.4f} pu   < {ang:7.2f} deg'.ljust(86) + '|')
        
    print('|' + '-'*86 + '|')
    print('|' + ' --> BUS VOLTAGES (Phase a, b, c) for all nodes:'.ljust(86) + '|')
    s_header = '  Bus Index |     Va (mag < deg)     |     Vb (mag < deg)     |     Vc (mag < deg)'
    print('|' + s_header.ljust(86) + '|')
    for idx, v_ph in enumerate(Vph_mat):
        v_mags = np.abs(v_ph)
        v_angs = np.angle(v_ph, deg=True)
        s_row = f'      {idx+1:<6d}|  {v_mags[0]:6.4f} < {v_angs[0]:7.2f} deg  |  {v_mags[1]:6.4f} < {v_angs[1]:7.2f} deg  |  {v_mags[2]:6.4f} < {v_angs[2]:7.2f} deg'
        print('|' + s_row.ljust(86) + '|')
    
    print('='*88)
    return

# ###################### LoadNetworkData4FA ##############################

    

def LoadNetworkData4FA(filename):
    global Ybus,Sbus,V0,buscode,pq_index,pv_index,Y_fr,Y_to,br_f,br_t,br_Y,S_LD,bus_kv, \
           ind_to_bus,bus_to_ind,MVA_base,bus_labels,Ybus0,Ybus2,Zbus0,Zbus1,Zbus2          
    #read in the data from the file...
    bus_data,load_data,gen_data,line_data,tran_data,mva_base,bus_to_ind,ind_to_bus = \
    rd4fa.read_network_data_from_file(filename)

    ############################################################################################## 
    # Construct the Ybus (positive-sequence), Ybus0 (zero-sequence), and Ybus2 (negative-sequence)
    # matrices from elements in the line_data and trans_data
    # Keep/modify code from the Python power flow program as needed
    ##########################################################################
    MVA_base = mva_base   
    N = len(bus_data) # Number of buses
    Ybus = np.zeros((N,N),dtype=complex)
    Ybus2 = np.zeros((N,N),dtype=complex)
    Ybus0 = np.zeros((N,N),dtype=complex)
    
    # Add line admittances to the Ybus
    for line in line_data:
        bus_fr, bus_to, id_, R, X, B, MVA_rate, X2, X0 = line #unpack
        ind_fr = bus_to_ind[bus_fr]    
        ind_to = bus_to_ind[bus_to] 

        #Update the bus admittance matrix
        Z_se = R + 1j*X; Y_se = 1/Z_se 
        Ybus[ind_fr,ind_fr]+= Y_se 
        Ybus[ind_to,ind_to]+= Y_se
        Ybus[ind_fr,ind_to]+= -Y_se
        Ybus[ind_to,ind_fr]+= -Y_se
        #negative sequence
        Z2 = R + 1j*X2; Y2 = 1/Z2
        Ybus2[ind_fr,ind_fr]+= Y2
        Ybus2[ind_to,ind_to]+= Y2
        Ybus2[ind_fr,ind_to]+= -Y2
        Ybus2[ind_to,ind_fr]+= -Y2
        #zero sequence
        # NOTE: Since the provided input file format lacks an R0 column, 
        # R0 is calculated based on the specific cable parameters provided in Table 1 
        # (z0_real / z1_real = 0.2 / 0.08 = 2.5).
        Z0 = (R * 2.5) + 1j*X0; Y0 = 1/Z0
        Ybus0[ind_fr,ind_fr]+= Y0
        Ybus0[ind_to,ind_to]+= Y0
        Ybus0[ind_fr,ind_to]+= -Y0
        Ybus0[ind_to,ind_fr]+= -Y0

    # Add the transformer model to Ybus
    #bus_fr, bus_to, id_, R,X,n,ang1,fr_co, to_co, X2, X0 
    for line in tran_data:
        bus_fr, bus_to, id_, R,X,n,ang1, MVA_rate,fr_co, to_co, X2, X0 = line #unpack
        ind_fr = bus_to_ind[bus_fr]  # get the matrix index corresponding to the bus    
        ind_to = bus_to_ind[bus_to]  # same here

        
        #positive sequence
        Zeq = 1j*X; Yeq = 1/Zeq
        Yps_mat = np.zeros((2,2),dtype=complex)
        Yps_mat[0,0] = Yeq   
        Yps_mat[0,1] = -Yeq
        Yps_mat[1,0] = -Yeq          
        Yps_mat[1,1] = Yeq
        ind_ = np.array([ind_fr,ind_to])
        Ybus[np.ix_(ind_,ind_)] += Yps_mat
        
        #negative sequence
        Z2 = 1j*X2; Y2 = 1/Z2
        Yps_mat = np.zeros((2,2),dtype=complex)
        Yps_mat[0,0] = Y2   
        Yps_mat[0,1] = -Y2
        Yps_mat[1,0] = -Y2          
        Yps_mat[1,1] = Y2
        ind_ = np.array([ind_fr,ind_to])
        Ybus2[np.ix_(ind_,ind_)] += Yps_mat
        
        #Zero sequence
        Z0 = 1j*X0; Y0 = 1/Z0
        Yps_mat = np.zeros((2,2),dtype=complex)
        if fr_co == 2 and to_co == 2:
            Yps_mat[0,0] = Y0
            Yps_mat[0,1] = -Y0
            Yps_mat[1,0] = -Y0           
            Yps_mat[1,1] = Y0
        elif fr_co == 2 and to_co == 3:
            Yps_mat[0,0] = Y0
        elif fr_co == 3 and to_co == 2:
            Yps_mat[1,1] = Y0     
        ind_ = np.array([ind_fr,ind_to])
        Ybus0[np.ix_(ind_,ind_)] += Yps_mat
        
       

    # create the Sbus, V and other bus related arrays
    V0 = np.ones(N,dtype=complex) # the inital guess for the bus voltages
    #Get the bus data
    bus_kv = []
    buscode = []
    bus_labels = []
    for line in bus_data:
        b_nr, label, v_init, theta_init, code, kv, v_low, v_high = line
        buscode.append(code)
        bus_labels.append(label)
        bus_kv.append(kv)
    buscode = np.array(buscode)
    bus_kv = np.array(bus_kv)
    
    # Create the Sbus vector (bus injections)
    Sbus = np.zeros(N,dtype=complex)
    S_LD = np.zeros(N,dtype=complex)
        
    for line in load_data:
        bus_nr, PLD, QLD = line
        ind_nr = bus_to_ind[bus_nr]
        SLD_val =(PLD+1j*QLD)/MVA_base
        Sbus[ind_nr] += -SLD_val # load is a negative injection...
        S_LD[ind_nr] +=  SLD_val # Keep track of the loads
        
    for line in gen_data:
        #bus_nr, mva_size, p_gen, X, X2, X0, Xn, ground
        bus_nr, MVA_size, p_gen, p_max, q_max, q_min,  X, X2, X0, Xn, ground = line
        ind_nr = bus_to_ind[bus_nr]
        SLD = (p_gen)/MVA_base
        Sbus[ind_nr] += SLD # gen is a negative injection...
        ind_bus = bus_to_ind[bus_nr]
        #positive sequence
        Z = 1j*X*mva_base/MVA_size; 
        Y = 1/Z        
        #Update the bus admittance matrix
        Ybus[ind_bus,ind_bus]+= Y
        #negative sequence
        Z2 = 1j*X2*mva_base/MVA_size; 
        Y2 = 1/Z2
        Ybus2[ind_bus,ind_bus]+= Y2
        #zero sequence
        Z0 = 1j*X0*mva_base/MVA_size 
        if ground:
            # Multiplied by 3 because the physical neutral current is 3 times the zero-sequence current (In = 3*I0). This is because the zero-sequence current is defined as the current that flows in the neutral conductor, and in a three-phase system, the neutral current is equal to the sum of the currents in the three phases. Therefore, if we have a zero-sequence impedance Z0, the corresponding neutral impedance would be Z0/3, and the admittance would be 3/Z0. However, since we are adding this to the diagonal of Ybus0, we can directly add 3*Y0 to account for this effect.
            Z0 += 3*1j*Xn*mva_base/MVA_size
        Y0 = 1/Z0
        Ybus0[ind_bus,ind_bus]+= Y0
   
    Zbus0 = np.linalg.inv(Ybus0)
    Zbus1 = np.linalg.inv(Ybus)
    Zbus2 = np.linalg.inv(Ybus2)
    
    return


############# ReadNetwrokData #############

"""
The ReadNetworkData helpers parse network input files used by
`LoadNetworkData4FA`. Parsing utilities are defined below; common
dependencies are imported at the top of the file.
"""

def read_network_data_from_file(filename):
    bus_data = []
    load_data = []
    gen_data = []
    line_data = []
    tran_data = []
    mva_base = 0.0
    data_input_type = '' #label keeping track of the type of model data being read
    #Open the network file and process the data
    with open(filename,newline='')as f:
        csv_reader = csv.reader(f)  # read in all of the data
        for line in csv_reader:
            #check if the line is a header line:
            if "//BEGIN " in line[0]: #New section of data starts with //BEGIN
                if 'BEGIN BUS DATA' in line[0]:
                    data_input_type = 'BUS'
                elif 'BEGIN LOAD DATA' in line[0]:
                    data_input_type = 'LOAD'
                elif 'BEGIN GENERATOR DATA' in line[0]:
                    data_input_type = 'GEN'
                elif 'BEGIN LINE DATA' in line[0]:
                    data_input_type = 'LINE'
                elif 'BEGIN TRANSFORMER DATA' in line[0]:
                    data_input_type = 'TRAN'
                elif 'BEGIN MVA SYSTEM' in line[0]:
                    data_input_type = 'MVA'                   
                else:
                    data_input_type = 'UNSPECIFIED'
                
                continue #read next line which contains data

            
            #Check if there is a comment at the end of the line // is in the data (that is comment) and remove that part
            dummy = []
            for k in line:
                if '//' in k: 
                    dummy.append(k.split('//')[0])
                    break
                else:
                    dummy.append(k)
            line = dummy

            if line[0] == '': # If the line was commented out, skip it..             
                continue
            if line[0].isspace(): # If the line has only whitespace, skip it..             
                continue
            
            
            if data_input_type == 'MVA':
                mva_base = parse_mva_data(line)
            elif data_input_type == 'BUS':
                a = parse_bus_data(line)
                bus_data.append(a)
            elif data_input_type == 'LOAD':
                b = parse_load_data(line)
                load_data.append(b)                
            elif data_input_type == 'GEN':
                d = parse_gen_data(line)
                gen_data.append(d)                
                continue
            elif data_input_type == 'LINE':
               c =  parse_transmission_line_data(line)
               line_data.append(c)
            elif data_input_type == 'TRAN':
               f =  parse_transformer_data(line)
               tran_data.append(f)
            else:
                print('DATA TYPE is unspecified!!!!')
                print('Input not treaded:', line)
            
    

    #create mappping objects from bus_nr to matrix indices and vice verse
    bus_to_ind = {} # empty dictionary
    ind_to_bus = {}
    for ind, line in zip(range(len(bus_data)),bus_data): 
        bus_nr = line[0]
        bus_to_ind[bus_nr] = ind
        ind_to_bus[ind] = bus_nr
            
    return bus_data,load_data,gen_data,line_data,tran_data,mva_base, bus_to_ind, ind_to_bus


def parse_transmission_line_data(row_):
    # unpack the values:    
    fr,to,br_id,R,X,B,MVA_rate,X2,X0 = row_[0:9]
    fr = int(fr)    #convert the string to int
    to = int(to)    #convert the string to int
    br_id = re.findall("'([^']*)'",br_id)[0]
    R = float(R) #convert the R str to float
    X = float(X) #convert the X str to float
    B = float(B) #convert the B_half str to float
    X2 = float(X2)
    X0 = float(X0)
    MVA_rate = float(MVA_rate)
    return [fr,to,br_id,R,X,B,MVA_rate,X2,X0] 


def parse_mva_data(row_):
    mva_size = row_[0]
    mva_size = float(mva_size)        #convert string to float
    return mva_size 


def parse_gen_data(row_):
    # unpack the values:
    bus_nr, mva_size, p_gen, p_max, q_max, q_min, X1, X2, X0, Xn, grnd = row_[0:11]
    bus_nr = int(bus_nr)     #convert the srting to int
    mva_size = float(mva_size)        #convert string to float
    p_gen = float(p_gen)        #convert string to float
    p_max = float(p_max)        #convert string to float
    q_max = float(q_max)        #convert string to float
    q_min = float(q_min)        #convert string to float
    X1 = float(X1)
    X2 = float(X2)
    X0 = float(X0)
    Xn = float(Xn)
    grnd = bool(grnd)
    return [bus_nr, mva_size, p_gen, p_max, q_max, q_min, X1, X2, X0, Xn, grnd] 



#//BEGIN BUS DATA,(BUS_NR, LABEL, KV_BASE, BUSCODE)
def parse_bus_data(row_):
    # unpack the values:    
    bus_nr, label, vm_init, theta_init, buscode, kv_base, v_min, v_max = row_[0:8]
    bus_nr = int(bus_nr)    #convert the srting to int
    label = re.findall(r'\b.*\b',label)[0] #regular expression to get the label
    vm_init = float(vm_init)        #convert string to float
    theta_init = float(theta_init)  #convert string to float
    buscode = int(buscode)          #convert the buscode str to int
    kv_base = float(kv_base)        #convert string to float
    v_min = float(v_min)            #convert string to float
    v_max = float(v_max)            #convert string to float
    return [bus_nr, label, vm_init, theta_init, buscode, kv_base, v_min, v_max] 



#//BEGIN LOAD DATA (BUS_NR, P_load MW, Q_load MVAR)  
def parse_load_data(row_):
    # unpack the values:    
    bus_nr, p_ld, q_ld = row_[0:3]
    bus_nr = int(bus_nr)     #convert the srting to int
    p_ld = float(p_ld)        #convert string to float
    q_ld = float(q_ld)        #convert string to float
    return [bus_nr, p_ld, q_ld] 


def parse_transformer_data(row_):
    # unpack the values:
    fr,to,br_id,R,X,n,ang1,MVA_rate,fr_co,to_co,X2,X0 = row_[0:12]
    fr = int(fr)    #convert the srting to int
    to = int(to)    #convert the string to int
    br_id = re.findall("'([^']*)'",br_id)[0]
#    br_id = re.findall(r"'.*'",br_id)[0] #regular expression to find the id str
#    br_id = br_id[1:-1]     #get the id out of the string
    R = float(R) #convert the R str to float
    X = float(X) #convert the X str to float
    n = float(n) #convert the n str to float
    ang1 = float(ang1) #convert the ang1 str to float
    X2 = float(X2)
    X0 = float(X0) #typo in th eoriginal file (X2) instad of (X0)
    MVA_rate=float(MVA_rate)
    fr_co = int(fr_co)    #convert the srting to int
    to_co = int(to_co)    #convert the string to int
    return [fr,to,br_id,R,X,n,ang1,MVA_rate,fr_co,to_co,X2,X0] 

    
################ Main4FA #################

# -*- coding: utf-8 -*-
"""
Main Script for Fault Analysis
"""


#filename = "src\\A_High_Loading_Operating_Point_deltadeltatransformer5.txt" 
filename = "src\\TestSystem4FA.txt"

#filename = "src\\TestSystem4FA_solidground1.txt" # for task 13 scenario 1
#filename = "src\\TestSystem4FA_Resistance_Grounding2.txt" # for task 13 scenario 2
#filename = "src\\TestSystem4FA_Reactance_Grounding3.txt" # for task 13 scenario 3
#filename = "src\\TestSystem4FA_ygygytransformer4.txt" # for task 13 scenario 4
#filename = "src\\TestSystem4FA_deltadeltatransformer5.txt" # for task 13 scenario 5


lnd4fa.LoadNetworkData4FA(filename) # makes Zbus0 available as lndfa.Zbus0 etc.
# Carry out the fault analysis ... 
FaultBus = 4

# FaultType: 0 = 3-phase balanced fault; 1 = Single Line-to-Ground fault;
#            2 = Line-to-Line fault;     3 = Double Line-to-Ground fault.
FaultType = 0
FaultImpedance = 0 # (in pu) 
PrefaultVoltage = 1.000 # (in pu)
# Iph: phase current array (0: phase a; 1: phase b; 2: phase c). 
# Vph_mat: phase line-to-ground voltages (rows: busses; columns: phases a, b, c).
Iph,Vph_mat = fa.FaultAnalysis(lnd4fa.Zbus0,lnd4fa.Zbus1,lnd4fa.Zbus2,lnd4fa.bus_to_ind, 
                                FaultBus,FaultType,FaultImpedance,PrefaultVoltage)
# Display results
fa.DisplayFaultAnalysisResults(Iph,Vph_mat,FaultBus,FaultType,FaultImpedance,PrefaultVoltage)
print('**********End of Fault Analysis**********')


################# Main4FA11C #################

# Main Script for Fault Analysis Part 11C

# Carry out the fault analysis ...
FaultBus = 4
PrefaultVoltage = 1  # (in pu)

# 4 fault types: 0, 1, 2, 3
fault_types = [0, 1, 2, 3] # 0 = 3-phase balanced fault; 1 = Single Line-to-Ground fault; 2 = Line-to-Line fault; 3 = Double Line-to-Ground fault. Adjust as needed for specific analysis.

# 3 different fault impedance values (in pu) - adjust as needed
fault_impedances = [0.00019, 0.02836, 18.9036]

for FaultType in fault_types:
    for FaultImpedance in fault_impedances:
        print(f"\n=== Running Fault Analysis | Bus={FaultBus}, Type={FaultType}, Zf={FaultImpedance} pu ===")
        
        # Iph: phase current array (0: phase a; 1: phase b; 2: phase c). 
        # Vph_mat: phase line-to-ground voltages (rows: busses; columns: phases a, b, c).
        Iph, Vph_mat = fa.FaultAnalysis(
            lnd4fa.Zbus0, lnd4fa.Zbus1, lnd4fa.Zbus2, lnd4fa.bus_to_ind,
            FaultBus, FaultType, FaultImpedance, PrefaultVoltage
        )

        # Display results
        fa.DisplayFaultAnalysisResults(
            Iph, Vph_mat, FaultBus, FaultType, FaultImpedance, PrefaultVoltage
        )

print('**********End of Fault Analysis**********')

################ Main4FA12C #################

# Main Script for Fault Analysis Part 12C

# Task 12: Impact of Pre-Fault Voltage
FaultBus = 4 # Or any bus specified in earlier tasks
FaultType = 0 # Example: 3-phase balanced fault (change as needed)
FaultImpedance = 0.0 # Bolted fault as per Task 12 instructions

# Define the range of pre-fault voltages to study
vf_values = [0.95, 1.00, 1.05]

for Vf in vf_values:
    print(f"\n--- Analyzing for Prefault Voltage: {Vf} pu ---")
    
    # Run the analysis
    Iph, Vph_mat = fa.FaultAnalysis(lnd4fa.Zbus0, lnd4fa.Zbus1, lnd4fa.Zbus2, 
                                    lnd4fa.bus_to_ind, FaultBus, FaultType, 
                                    FaultImpedance, Vf)
    
    # Display results for each case
    fa.DisplayFaultAnalysisResults(Iph, Vph_mat, FaultBus, FaultType, FaultImpedance, Vf)
print('**********End of Fault Analysis**********')