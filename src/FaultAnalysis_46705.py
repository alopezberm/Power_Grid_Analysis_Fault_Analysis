"""
46705 - Power Grid Analysis
This file contains the definitions of the functions needed to
carry out Fault Analysis calculations in python.
"""

import numpy as np

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
        ''' Insert your code'''
    elif fault_type == 1:
        ''' Insert your code'''
    elif fault_type == 2:
        ''' Insert your code'''
    elif fault_type == 3:
        ''' Insert your code'''
    else:
        print('Unknown Fault Type')
    return Iseq

# 1.2 the Calculate_Sequence_Fault_Voltages() function
def Calculate_Sequence_Fault_Voltages(Zbus0,Zbus1,Zbus2,bus_to_ind,fault_bus,Vf,Iseq):
    ''' Insert your code'''
    return Vseq_mat

# 1.3. the Convert_Sequence2Phase_Currents() function
def Convert_Sequence2Phase_Currents(Iseq):
    ''' Insert your code'''
    return Iph

# 1.4 the Convert_Sequence2Phase_Voltages() function
def Convert_Sequence2Phase_Voltages(Vseq_mat):
    ''' Insert your code'''
    return Vph_mat

# ####################################################
# #  Displaying the results in the terminal window   #
# ####################################################
# 2. the DisplayFaultAnalysisResults() function
def DisplayFaultAnalysisResults(Iph,Vph_mat,fault_bus,fault_type,Zf,Vf):
    print('==============================================================')
    print('|                  Fault Analysis Results                    |')
    print('==============================================================')

    ''' Insert your code'''
    
    print('==============================================================')  
    return