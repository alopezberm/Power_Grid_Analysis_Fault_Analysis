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