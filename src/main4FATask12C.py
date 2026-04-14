# -*- coding: utf-8 -*-
"""
Main Script for Fault Analysis
"""

import FaultAnalysis_46705 as fa    # import Fault Analysis functions
import LoadNetworkData4FA as lnd4fa # load the network data to global variables
filename = "src\\TestSystem4FA.txt" #"./TestSystem4FA.txt"
lnd4fa.LoadNetworkData4FA(filename) # makes Zbus0 available as lndfa.Zbus0 etc.


# Task 12: Impact of Pre-Fault Voltage
FaultBus = 4 # Or any bus specified in earlier tasks
FaultType = 2 # Example: 3-phase balanced fault (change as needed)
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