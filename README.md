# Repository for Paper: "Modeling Cultural Evolution Processes in Dressel 20 Amphora Production during the Roman Empire"

This repository contains data and scripts used in the manuscript title, "Modelling cultural evolution processes in Dressel 20 amphora production during the Roman Empire" by María Coto-Sarmiento and Simon Carrignon (2025) to be published  in the Journal of Archaeological Science as part of the Special Issue “Novel Approaches to Past Transportation Networks”.

The repository is organised into the following main directories:
- model: contain the core of the model, in python (cf section#model)
- data: contain the original dataset
- script: contain script used to run and anlyse the simulation (cf section#analysis)

---

This paper is based on two principal components: 

1. The agent based model, which is written in python and describe a simplified geography where workshop at different places can social interact. 
2. The exploration of the simulation; that combine simple basj script to carry multiple simulation and some R scripts to visualise and anlysise the results.


The model itself cna be explored more than it has been done in the paper, 

## 🚀 Dataset

The original data are from Coto et al 2020. They include: measurement of the pot and least cost path between all settlement, using rivers. 

## 🚀 Execute the Model

To run the simulation on a Linux machine, ensure the following packages are installed:

```bash
python3 -m venv .
git clone https://github.com/Auerilas/ecopy.git
python3 -m pip install -e ecopy
./bin/pip3 install Cython
./bin/python3 -m pip install -e ecopy
./bin/pip3 install scikit-learn
```

Once the packages are installed, the simulation can be run as follows:

```bash
./bin/python3 exploreMantelAlpha.py 'data/riverDistances.csv' 't'
```

## 🚀 Re-run Analysis 

To run the simulation on a Linux machine, ensure the following packages are installed:

```bash
python3 -m venv .
git clone https://github.com/Auerilas/ecopy.git
python3 -m pip install -e ecopy
./bin/pip3 install Cython
./bin/python3 -m pip install -e ecopy
./bin/pip3 install scikit-learn
```

Once the packages are installed, the simulation can be run as follows:

```bash
./bin/python3 exploreMantelAlpha.py 'data/riverDistances.csv' 't'
```




##  File Structure

### 🗂️ `./model/`

Core Python file containing the definition of the class used in the model.

### 🗂️ `./data/`

Data files (CSVs) and a Python helper for loading the data used in the model. These are utilized to generate constraints on amphora shapes (covariance matrix and min/max dimension), establish the initial mean of each measurement, and calculate the observed R-squared Mantel test correlation factor.

### 🗂️ `./scripts/`

Various useful scripts.

