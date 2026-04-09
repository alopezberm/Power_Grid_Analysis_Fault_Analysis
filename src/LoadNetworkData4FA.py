# -*- coding: utf-8 -*-
import numpy as np
import ReadNetworkData as rd4fa

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
        Z_se = 1j*X; Y_se = 1/Z_se
        
        #Update the bus admittance matrix
        Ybus[ind_fr,ind_fr]+= ''' Insert your code'''
        Ybus[ind_to,ind_to]+= ''' Insert your code'''
        Ybus[ind_fr,ind_to]+= ''' Insert your code'''
        Ybus[ind_to,ind_fr]+= ''' Insert your code'''
        #negative sequence
        Z2 = ''' Insert your code'''
        Y2 = ''' Insert your code'''
        Ybus2[ind_fr,ind_fr]+=''' Insert your code'''
        Ybus2[ind_to,ind_to]+= ''' Insert your code''' 
        Ybus2[ind_fr,ind_to]+= ''' Insert your code'''
        Ybus2[ind_to,ind_fr]+= ''' Insert your code'''
        #zero sequence
        Z0 = ''' Insert your code''' 
        Y0 = ''' Insert your code'''
        Ybus0[ind_fr,ind_fr]+= ''' Insert your code'''
        Ybus0[ind_to,ind_to]+= ''' Insert your code'''
        Ybus0[ind_fr,ind_to]+= ''' Insert your code'''
        Ybus0[ind_to,ind_fr]+= ''' Insert your code'''

    # Add the transformer model to Ybus
    #bus_fr, bus_to, id_, R,X,n,ang1,fr_co, to_co, X2, X0 
    for line in tran_data:
        bus_fr, bus_to, id_, R,X,n,ang1, MVA_rate,fr_co, to_co, X2, X0 = line #unpack
        ind_fr = bus_to_ind[bus_fr]  # get the matrix index corresponding to the bus    
        ind_to = bus_to_ind[bus_to]  # same here

        
        #positive sequence
        Zeq = 1j*X; Yeq = 1/Zeq
        Yps_mat = np.zeros((2,2),dtype=complex)
        Yps_mat[0,0] = ''' Insert your code'''  
        Yps_mat[0,1] = ''' Insert your code'''
        Yps_mat[1,0] = ''' Insert your code'''          
        Yps_mat[1,1] = ''' Insert your code'''
        ind_ = np.array([ind_fr,ind_to])
        Ybus[np.ix_(ind_,ind_)] += Yps_mat
        
        #negative sequence
        Z2 = 1j*X2; Y2 = 1/Z2
        Yps_mat = np.zeros((2,2),dtype=complex)
        Yps_mat[0,0] = ''' Insert your code''' 
        Yps_mat[0,1] = ''' Insert your code'''
        Yps_mat[1,0] = ''' Insert your code'''           
        Yps_mat[1,1] =''' Insert your code'''
        ind_ = np.array([ind_fr,ind_to])
        Ybus2[np.ix_(ind_,ind_)] += Yps_mat
        
        #Zero sequence
        Z0 = 1j*X0; Y0 = 1/Z0
        Yps_mat = np.zeros((2,2),dtype=complex)
        if fr_co == 2 and to_co == 2:
            Yps_mat[0,0] = ''' Insert your code'''
            Yps_mat[0,1] = ''' Insert your code'''
            Yps_mat[1,0] = ''' Insert your code''' 
            Yps_mat[1,1] = ''' Insert your code'''
        elif fr_co == 2 and to_co == 3:
            Yps_mat[0,0] = ''' Insert your code'''
        elif fr_co == 3 and to_co == 2:
            Yps_mat[1,1] = ''' Insert your code'''       
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
        Ybus[ind_bus,ind_bus]+= ''' Insert your code'''
        #negative sequence
        Z2 = 1j*X2*mva_base/MVA_size; 
        Y2 = 1/Z2
        Ybus2[ind_bus,ind_bus]+= ''' Insert your code'''
        #zero sequence
        Z0 = 1j*X0*mva_base/MVA_size 
        if ground:
            Z0 += ''' Insert your code'''
        Y0 = 1/Z0
        Ybus0[ind_bus,ind_bus]+= Y0
   
    Zbus0 = np.linalg.inv(Ybus0)
    Zbus1 = np.linalg.inv(Ybus)
    Zbus2 = np.linalg.inv(Ybus2)
    
    return
    