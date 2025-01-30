#!/usr/bin/python

#A simple evolutionary model to study the evolution of workshop amphora production
#

import random
import math
import csv
import numpy as np
from numpy.random import choice
from model.Workshop import Workshop #import the agent class
from data.ceramic import *
import sys,os

#Definition of a simulation
class CCSimu(object):
    #"sd",12.3795766686627,8.5207422211249,9.83854926282588,11.6498468434151,13.2438062309636

    n_ws=-1 ##if no number of workshop given we us 5
    max_time= 10000
    outfile= "output"
    model= -1

    #Some usual default parameters:
    #p_mu=.001 ##mutation probability 1 other 1000 .1 percent
    #b_dist=1 #weight of the distance


    realws={"villaseca","belen","malpica","delicias","parlamento"}
    p_mu=.001
    b_dist=-1 #bias toward distance: when b_dist == -1 <=> no bias <=> transmission depends only of  (horizontal transmission).  b_dist == 2 <=> ultra biased <=> even small distance make  copy
    world=list()
    world_list=dict()
    world_lim=list()
    world_mat=dict()
    prodfile=""
    init=""
    rate_depo=1000 #the rate at which workshops will write their deposit in the outputfile
    initm={"cov_mat":cov_mat,"means":globalmeans}

    def __init__(self,n_ws,max_time,pref,model,p_mu,b_dist,init,dist_list={},outputfile=True,mu_str=[],log=True,prod_rate=10,rate_depo=1000,dist_file=""):
        self.dist_file=dist_file
        #print(str(n_ws)+","+str(max_time)+","+str(p_mu)+","+str(b_dist))
        self.n_ws=n_ws
        self.max_time=max_time
        self.pref=pref #us eto classify differetn type of simulation
        self.model=model #what tipe of model should be in HT HTD VT or -1 if no model
        self.p_mu=p_mu
        self.mu_str=mu_str #a dictionary given for each measure the amplitude of mutation
        self.b_dist=b_dist
        self.init=init
        self.log=log
        self.ouputfile=outputfile
        self.prod_rate=prod_rate
        self.rate_depo=rate_depo
        self.initm={"cov_mat":cov_mat,"means":globalmeans}
        #if(len(mu_str) < 1) self.mu_str={

        if self.log :print('Initialization of the world')

        self.world = dict() #initialisation of the world
        self.world_dist=dict() #dictionnaire to store the distance of the cities two by two
        self.world_mat=dict() #dictionnaire to store the full matrice of distance

        #self.world_lim={"exterior_diam":{"min":130,"max":200},"protruding_rim":{"min":5,"max":40}, "rim_w":{"min":25,"max": 48}, "rim_w_2":{"min": 15,"max": 44}}
        self.world_lim={"min":worldmin,"max":worldmax}
        if self.init=="file":
            for i in self.realws:
                self.world_mat[i]=dict()
                for j in self.realws:
                    if i != j :
                        self.world_mat[i][j]=0
            if(len(dist_list) >0):
                self.world_dist = dist_list
            else:
                if self.log : print("initialize the workshop using the file 'data/distmetrics.csv'")
                if self.log : print("warning:argument"+" number of workshop"+" will be ignored")
                if self.dist_file=="" : self.dist_file='data/riverDistances.csv'
                with open(self.dist_file,'r') as distfile:
                      distances = csv.reader(distfile, delimiter=',')
                      next(distances) #skip header
                      for row in distances:
                          self.world_dist[row[0]]=float(row[2]) #print(row)
                          self.world_dist[row[0]+row[1]]=float(row[2]) #print(row)
                          self.world_dist[row[1]+row[0]]=float(row[2]) #print(row)
                          self.world_mat[row[1]][row[0]]=float(row[2]) #print(row)
                          self.world_mat[row[0]][row[1]]=float(row[2]) #print(row)
                          self.world_mat[row[0]][row[0]]=1
                          self.world_mat[row[1]][row[1]]=1
                      #worldlist[distances[1]] = {distances[2],distances[3]}
                distfile.close()
                if self.log : print(distfile)

              #(1) mean of mean btw ws (2)sd of mean btw ws (3)min (4)max
              #measurement:             (1)                 (2)     (3) (4)
              #exterior_diam           166.667395         4.9998310 130 200
              #inside_diam              93.631245         1.3069177  70 140
              #rim_h                    35.387083         0.8810068  25  48
              #rim_w                    36.686752         1.9171952  25  48
              #shape_w                   9.646956         0.6530906   5  14
              #rim_inside_h             28.373472         1.1329995  20  39
              #rim_w_2                  31.054947         1.2328019  15  44
              #protruding_rim           18.273888         3.2735080   5  40
             #exterior_diam    inside_diam          rim_h          rim_w        shape_w  rim_inside_h        rim_w_2 protruding_rim
             #     11.126504       9.250002       3.004174       3.494843       1.080722       2.976005       4.216725       4.790658
            #the mean standard deviation for every measurment
            self.maxdist=max(self.world_dist.values())
            self.mindist=min(self.world_dist.values())
            for ws in  self.realws:
                dist=10 #this is not use in that case as the "distance" are given by the dictionnary world_dict
                if(self.n_ws<0):
                    wkid=-1
                    wsid=ws
                else:
                    wkid=0
                    wsid=ws+"_0"
                new_ws= Workshop(ws,dist,self.initm.copy(),self.prod_rate,self.world_lim,log=self.log,wkid=wkid)
                self.world[wsid]=new_ws
        elif self.init=="art":
            if self.log : print("initialize"+str(self.n_ws)+" workshop randomly")
            for ws in range(self.n_ws):
                dist=ws
                wsid='ws_'+str(ws)
                new_ws= Workshop(wsid,dist,self.initm.copy(),10,self.world_lim,log=self.log)
                self.world[wsid]=new_ws
            self.maxdist=self.n_ws
            self.mindist=0
        if(self.ouputfile):
            outfilename=self.pref+"_"+"N"+str(self.n_ws)+".csv"
            self.prodfile = open(outfilename, "w")
            header = "time,workshop,dist,amphora,"+",".join(self.initm['means'].keys())+"\n"
            self.prodfile.write(header)
        else:
            self.prodfile=""

        if(self.n_ws > 0):
            oldkeys=self.world.copy()
            for i in  oldkeys.keys(): #copy n_ws time the workersb
                for j in range(self.n_ws):
                    wsid=self.world[i].wsid
                    wid=str(wsid)+"_"+str(j+1)
                    new_ws= Workshop(wsid,dist,self.initm,self.prod_rate,self.world_lim,log=self.log,wkid=j)
                    self.world[wid]=new_ws
        self.n_ws=len(self.world)
        #print("total number of worke:"+str(self.n_ws))

    #given a absolute distance, return a relative distance
    #def getrelativedist_array(self,dis,alpha):
    #    dis=np.array(dis)
    #    probas=pow(dis,-alpha)/sum(pow(dis,-alpha))
    #    return(probas)

    def getrelativedist(self,dis,alpha):
        probas={k : np.float64(math.exp(-alpha*v)) for k,v in dis.items()}
        tot=np.float64(sum(probas.values()))
        probs={k : np.float64(v)/tot for k,v in probas.items()}
        #if(sum(probs.values())!=1):
        #    print(probas)
        #    print(probs)
        #    print(sum(probs.values()))
        return(probs)

    #strenght of the bias toward distance.
    def beta_d(self,dist):
        #if(epsilon>1):
               #if(self.b_dist> 0):
        #    return( -pow(d,100 ** self.b_dist))
        #else: #(self.b_dist=< 0):
        #    return( -(1-pow(d,100 ** self.b_dist)))
        return(1-pow(1-dist,100 ** self.b_dist))
    ##proxi to setup copy using 3 different bias
    def threemod(self,dist):
        proba=0
        if(  self.model == "HT"):
            proba= 1   #no effect of distance between the workshop ie everybody copy everybody with same proba of 1/100
        elif self.model== "HTD":
            proba= dist < random.random()*self.b_dist  #should be true when two workshop are close to eachother
        elif self.model == "VT":
            proba= 0
        return(proba)

    def getcopy(self,dis,alpha):
        d=self.getrelativedist(dis,alpha)
        keys,probas=zip(*d.items())
        probs=np.array(probas)
        #print(probs)
        try:
            copy=np.random.choice(keys,1,p=probs)
        except:
            #print("===============================")
            #print(dis)
            #print(alpha)
            #print(probs)
            #print(sum(probs))
            #print(sum(np.isnan(probs)))
            #print("===============================")
            if(sum(np.isnan(probs))>0):
                probs[np.isnan(probs)]=0
                probs[~np.isnan(probs)]=1/sum(np.isnan(probs))
            #else:
            #    probs[~np.isnan(probs)]=0
            #    probs[np.isnan(probs)]=1
            copy=np.random.choice(keys,1,p=probs)
            #sys.exit()
        #print("gonna copy:"+str(copy[0]))
        return(self.world[copy[0]])


    def run(self): ##main function of the class Experiment => run a simulation

        relative=True #relative distance to normalize the distance between 0 and 1 where 0 is the distance
        ##begining of the simulation
        if self.log : print(" simulation copy mechanism: "+str(self.model)+",b_dist="+str(self.b_dist)+",time="+str(self.max_time)+",p_mu="+str(self.p_mu))
        for t in range(0,self.max_time,1): 
            if self.log : print("step number"+str(t))
            for i in self.world.keys() :
                print(i)
                ws=self.world[i]
                if( self.rate_depo == 0 ):
                    ws.produce(t,self.prodfile)
                elif( t%self.rate_depo ==0): 
                    ws.produce(t,self.prodfile)
                if( random.random()< self.p_mu):
                    ws.mutate(self.mu_str)
                else:
                    distances=dict()
                    for j in self.world.keys(): #going through all potential neighbours
                        if(i != j):
                            nb=self.world[j]
                            distances[j]=self.world_mat[ws.wsid][nb.wsid] #we use the distance between workshop tofind distance between individual. Very suboptimal.
                            #distances=self.world_mat[ws.wsid]
                    #print("ws:"+ws.id)
                    ws2=self.getcopy(distances,self.b_dist)
                    #if(ws.wsid != ws2.wsid):
                        #print("over ws copy")
                    #print(ws.wsid + "(" + str(ws.wkid) + ") copy from "+ws2.wsid+ "(" + str(ws2.wkid) + ")")
                    ws.copy(ws2)
        if(self.prodfile!=""):
            self.prodfile.close()
        if self.log : print("simulation done.")
        return(self.world)

