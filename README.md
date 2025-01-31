# Repository for Paper: "Modeling Cultural Evolution Processes in Dressel 20 Amphora Production during the Roman Empire"

## Content

### 🗂️ `./model/`

Core Python file containing the definition of the class used in the model.

### 🗂️ `./data/`

Data files (CSVs) and a Python helper for loading the data used in the model. These are utilized to generate constraints on amphora shapes (covariance matrix and min/max dimension), establish the initial mean of each measurement, and calculate the observed R-squared Mantel test correlation factor.

### 🗂️ `./scripts/`

Various useful scripts.

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

