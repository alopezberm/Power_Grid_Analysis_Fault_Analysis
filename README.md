# DTU 46705 Power Grid Analysis - Assignment 2: Fault Analysis ⚡

This repository contains the Python implementation and project structure for **Assignment 2** of the 46705 Power Grid Analysis course at the Technical University of Denmark (DTU), developed by **Group 15**.

## 🎯 Project Objectives

The purpose of this assignment is to develop a Python-based program capable of systematically calculating fault currents and bus voltages for different fault types and locations in a transmission system.

The main objectives (based on the course guidelines) include:
- Applying the theory of symmetrical components to model generators, transformers, and transmission lines under fault conditions.
- Constructing positive, negative, and zero sequence networks.
- Computing subtransient fault currents for 3-phase balanced faults, Single Line-to-Ground (SLG) faults, Line-to-Line (LL) faults, and Double Line-to-Ground (DLG) faults.
- Analyzing and validating the impact of faults by comparing numerical results with manual analytical calculations (Part A).

## 📂 Repository Structure

```text
46705_Assignment2_FaultAnalysis/
│
├── data/
│   └── TestSystem4FA.txt         # Text file containing the network topology and data
│
├── src/
│   ├── main4FA.py                # Main script to run the fault analysis
│   ├── FaultAnalysis_46705.py    # Core functions to implement (sequence networks & fault currents)
│   ├── LoadNetworkData4FA.py     # Loads the network data into global variables
│   └── ReadNetworkData.py        # Auxiliary functions to parse the .txt file
│
├── report/
│   ├── figures/                  # Images, plots, and diagrams used in the report
│   └── A2_Group_15_46705.pdf     # The final report PDF for DTU-LEARN submission
│
├── .gitignore                    # To ignore __pycache__, virtual environments, etc.
└── README.md                     # Project documentation
