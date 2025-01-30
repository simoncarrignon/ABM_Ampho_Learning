import numpy as np
import sys,os

from model.apemcc import CCSimu
from data.ceramic import *
from scipy.stats import ttest_ind_from_stats

from ecopy import mantel
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import confusion_matrix

import random


def manteldist(x,y):
    if x is None:
        return(1000)
    sites=[]
    metrics=np.empty((0,8))
    for w in x.keys() :
        wsid=x[w].wsid #get workshop id
        try: 
            last=x[w].production[len(x[w].production)-1]  #get last production
            sites=sites + [wsid]*len(last) #gie to all production the name of the workshop of the worker
            metrics=np.concatenate( (metrics,last) )
        except: print(len(x[w].production))
    mat=confusion_matrix(sites,LDA(priors=[.2,.2,.2,.2,.2]).fit(metrics,sites).predict(metrics))
    mat[0,0]=mat[1,1]=mat[2,2]=mat[3,3]=mat[4,4]=0
    nil=mat.sum(1)==0 #store the perfect match to avoid nas
    mat[nil,]=[4,4,4,4,4]
    mat=1-(mat.T/mat.sum(1)).T
    for i in range(0,mat.shape[0]-1):
        for j in range(i+1,mat.shape[0]):
            mat[j,i]=mat[i,j]
    mat[0,0]=mat[1,1]=mat[2,2]=mat[3,3]=mat[4,4]=0
    robs=mantel.Mantel(d1=np.asarray(y["dist"]),d2=mat,tail='both',test='pearson')
    #print("simulation mantel test:"+str(robs))
    return (robs)

distfile=sys.argv[1] #the file where distances are stored
resfile=sys.argv[2] #a prefix that will be used as a folder to store the result of the ABC

#Computing the real distances 
dataset = pd.read_csv('data/dataDressel.csv')
dataset= dataset[dataset['type'].isin(['Dressel C','Dressel D','Dressel E'])]
metrics = dataset.iloc[:, 4:12].values
sites = dataset.iloc[:, 12].values

distriv = pd.read_csv(distfile,header=0) #reading rivers set distance
distriv=pd.crosstab(distriv.iloc[:,0],distriv.iloc[:,1],values=distriv.iloc[:,2],aggfunc="sum") #creating a distance matrix using the list of distance
distriv[distriv.isna()]=0 #replacing NA by 0

mat=confusion_matrix(sites,LDA(priors=[.2,.2,.2,.2,.2]).fit(metrics,sites).predict(metrics))

mat[0,0]=mat[1,1]=mat[2,2]=mat[3,3]=mat[4,4]=0
mat=1-(mat.T/mat.sum(1)).T
for i in range(0,mat.shape[0]-1):
    for j in range(i+1,mat.shape[0]):
        mat[j,i]=mat[i,j]
robs=mantel.Mantel(d1=np.asarray(distriv),d2=mat,tail='both',test='pearson',nperm=119).r_obs
print(robs)

data={"robs":robs,"dist":distriv}
if not os.path.isfile(resfile) :
   with open(resfile, "a") as myfile:
        myfile.write("r_obs,p_val,alpha,mu,tstep,nw,diff\n")

for alpha in np.geomspace(.0001,4,99):
    for r in range(0,99) :
        mu=0.05
        nw=20
        tstep=200
        exp=CCSimu(nw,tstep,"test",-1,mu,alpha,"file",mu_str=allsds*2,rate_depo=tstep-1,outputfile=False,log=False,dist_file=distfile)
        res=exp.run()
        mt=manteldist(res,data)
        with open(resfile, "a") as myfile:
            myfile.write(str(mt.r_obs)+","+str(mt.pval)+","+str(alpha)+","+str(mu)+","+str(tstep)+","+str(nw)+","+str(abs(.51-mt.r_obs))+"\n")
