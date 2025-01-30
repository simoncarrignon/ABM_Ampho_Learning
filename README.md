#  Repo for paper "Modelling Cultural Evolution Processes in Dressel 20 Amphora Production during the Roman Empire"


To run the simulation on a linux machine, a few packages needs to be installed: 

```bash
python3 -m venv .
git clone https://github.com/Auerilas/ecopy.git
python3 -m pip install -e ecopy
./bin/pip3 install Cython
./bin/python3 -m pip install -e ecopy
./bin/pip3 install scikit-learn
```

simulation can be run then:

```bash
./bin/python3 exploreMantelAlpha.py 'data/riverDistances.csv' 't'
```
