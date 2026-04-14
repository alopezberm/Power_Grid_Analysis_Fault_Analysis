# DTU 46705 Power Grid Analysis - Assignment 2: Fault Analysis ⚡

This repository contains the Python implementation and project structure for **Assignment 2** of the 46705 Power Grid Analysis course at the Technical University of Denmark (DTU), developed by **Group 15**.

## 🎯 Project Objectives

The purpose of this assignment is to develop a Python-based program capable of systematically calculating fault currents and bus voltages for different fault types and locations in a transmission system.

The main objectives (based on the course guidelines) include:
* Applying the theory of symmetrical components to model generators, transformers, and transmission lines under fault conditions.
* Constructing positive, negative, and zero sequence networks.
* Computing subtransient fault currents for 3-phase balanced faults, Single Line-to-Ground (SLG) faults, Line-to-Line (LL) faults, and Double Line-to-Ground (DLG) faults.
* Analyzing and validating the impact of faults by comparing numerical results with manual analytical calculations (Part A).

## 📂 Repository Structure

This repository is organized into root documentation and a central `src/` directory containing the logic, simulation routines, and network data.

### 🏠 Project Root
* **`.gitignore`** 
* **`README.md`** 

### ⚙️ Source Code (`src/`)
* **`A2_Group_15_46705.py`** – **The Master Script.** The primary entry point that integrates all modules into a single execution flow for the full assignment.
* **`FaultAnalysis_46705.py`** – Core mathematical library implementing symmetrical component transformations and fault current equations.
* **`LoadNetworkData4FA.py`** – Logic for assembling the $Y_{bus}$ and $Z_{bus}$ matrices for positive, negative, and zero sequence networks.
* **`ReadNetworkData.py`** – Parsing utility to load grid parameters from text files into Python dictionaries/arrays.
* **`main4FA.py`** – Script for general system validation and testing.
* **`main4FATask11C.py`** – Dedicated routine for performing 3-phase symmetrical fault analysis.
* **`main4FATask12C.py`** – Dedicated routine for analyzing the influence of pre-fault voltage on current magnitudes.

### 📊 Network & Test Data (`src/`)
* **`TestSystem4FA.txt`** – The standard base network configuration for the assignment.
* **`A_High_Loading_Operating_Point.txt`** – System state under high-load conditions for pre-fault analysis.
* **`TestSystem4FA_solidground1.txt`** – Network data for solidly grounded neutral study.
* **`TestSystem4FA_Resistance_grounding2.txt`** – Network data for resistance grounding study.
* **`TestSystem4FA_Reactance_Grounding3.txt`** – Network data for reactance grounding study.
* **`TestSystem4FA_ygygytransformer4..txt`** – Configuration for Yg-Yg transformer connection analysis.
* **`TestSystem4FA_deltadeltatransformer5.txt`** – Configuration for Delta-Delta transformer connection analysis.
