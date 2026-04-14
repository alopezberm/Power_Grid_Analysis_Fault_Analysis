# -*- coding: utf-8 -*-
"""
Main Script for Fault Analysis
"""

import FaultAnalysis_46705 as fa    # import Fault Analysis functions
import LoadNetworkData4FA as lnd4fa # load the network data to global variables

#Import this one when does task 13 Restiance scenario
#import LoadNetworkData4FATask13 as lnd4fa # load the network data with grounding modifications to global variables

#filename = "src\\A_High_Loading_Operating_Point.txt" #"./TestSystem4FA.txt"
filename = "src\\TestSystem4FA.txt"

#filename = "src\\A_High_Loading_Operating_Point_solidground1.txt" # for task 13 scenario 1
#filename = "src\\A_High_Loading_Operating_Point_Resistance_Grounding2.txt" # for task 13 scenario 2
#filename = "src\\A_High_Loading_Operating_Point _Reactance_Grounding3.txt" # for task 13 scenario 3
#filename = "src\\A_High_Loading_Operating_Point_ygygytransformer4.txt" # for task 13 scenario 4
#filename = "src\\A_High_Loading_Operating_Point_deltadeltatransformer5.txt" # for task 13 scenario 5


lnd4fa.LoadNetworkData4FA(filename) # makes Zbus0 available as lndfa.Zbus0 etc.

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