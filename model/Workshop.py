#import random 
from numpy import random 

#Definition of the Agent which are workshop in our case:
class Workshop(object):
    dist=0
    wsid=""
    wkid=-1
    productionparam={}
    prod_rate=-1
    mutation_power=4
    world_lim={}
    production={}
    cov_mat=[]
    means=[]


    #This function allow us to create a new workshop 
    def __init__(self, wsid, dist,productionparam,prod_rate,world_lim,log=True,wkid=-1):
        self.productionparam=productionparam
        self.world_lim=world_lim
        self.wsid=wsid
        if(wkid>-1):self.wkid=wkid
        self.production=[] #store the production step by step
        self.prod_rate=prod_rate
        self.means=productionparam['means']
        self.cov_mat=productionparam['cov_mat']
        self.prod_rate=prod_rate
        self.dist=dist
        self.perfectcopy=1
        self.log=log
        #for measure in self.productionparam:
        #    self.production[measure]=list()
        if self.log: print('New worker '+str(wkid)+" in workshop "+self.wsid+" at : "+str(self.dist)+" km")

    #fonction to use  str() in order to print a workshop as a string (in this case doesnt work with this code)
    #def __str__(self):
        #return('Workshop '+self.id+" at distance: "+str(self.dist)+"\n\t they produce amphora with exterior_diam mean="+str(self.productionparam["exterior_diam"]["mean"])+", sd="+str(self.productionparam["exterior_diam"]["sd"]))
    
    #produce: show a production of amphora given the parameter of the function measure we use (in this case doesnt work with this code)
    #def produce(self,amount):
        #for i in range(1,amount,1):
            #amphsize= random.gauss(self.productionparam["exterior_diam"]["mean"],self.productionparam["exterior_diam"]["sd"])

    #writeProduce: write in a file the amphora produced given the parameter of the workshop 
    #if amount>0 it will limit the number of amphora written in the output file (
    #t: the time of production (used to saave when it was produced, useless if only l
    def produce(self,t,res_file,amount=0):
        if amount == 0:
            amount=self.prod_rate
        res=random.multivariate_normal(self.productionparam["means"],self.productionparam["cov_mat"],amount)
        self.production.append(res)
        if(res_file!=""):
            for i in range(amount):
                amph=str(t)+","+self.wsid+","+str(self.dist)+",amphora_"+ str(self.wkid) + "."+ str(i)+","
                amph=amph+",".join(map(str,res[i]))
                res_file.write(amph+"\n")
        return(res)


    #mutate: randomly change the parameter of production
    def mutate(self,mu_str):
        percent=0

        for measure in self.productionparam['means'].keys():
            #up=-1 #increase or decrease the value
            #if(random.randint(2) == 1):up=1 #randomly  increase or decrease the size
            cur=self.productionparam['means'][measure]  #current measure
            ms=random.normal(0,mu_str[measure],1) #strentgh for this corresponding measure
            if(percent): #two mode of mutation, decrease/increase by a relative percentage of the measurement or using an absolute increment 
                new = cur + cur * ms 
            else:
                new = cur +  ms 

            #print("add"+str(new)+"to "+measure)
            while new > (self.world_lim["max"][measure]) or new < (self.world_lim["min"][measure]):
                if new > (self.world_lim["max"][measure]):
                    up=-1
                else :
                    up = 1 
                ms=random.normal(0,mu_str[measure],1)
                if(percent):
                    new = cur + cur * ms * up
                else:
                    new = cur + ms
            self.productionparam["means"][measure]=new


    def copy(self,ws2):
        if(self.perfectcopy):
            self.productionparam = ws2.productionparam.copy()
            self.productionparam["means"] = ws2.productionparam["means"].copy()
        else:
            self.measure = self.imperfectcopy()

    ##imperfect copy
    def imperfectcopy(self):
        for measure in self.productionparam["means"].key(): #loop if we cannot assume learnign is perfect
            up=-1
            if(random.randint(0,1)):up=1
            self.productionparam["means"][measure] = ws2.productionparam[measure]["mean"] #+  self.productionparam[measure]["mean"]*self.mutation_power  *up
            self.productionparam[measure]["cov_mat"] = ws2.productionparam[measure]["cov_mat"]
            while self.productionparam["means"][measure] > self.world_lim["max"][measure] or self.productionparam["mean"][measure] < self.world_lim["min"][measure]:
                if self.productionparam["mean"][measure] > self.world_lim["max"][measure]:
                    up=-1
                else :
                    up = 1 
                self.productionparam["mean"][measure] = self.productionparam["mean"][measure] + self.productionparam["mean"][measure]* self.mutation_power  *up
            #self.productionparam[measure]["sd"] = ws2.productionparam[measure]["sd"]+  self.productionparam[measure]["sd"]*.0001 *up  + random.random()*self.productionparam["exterior_diam"]["sd"]-self.productionparam["exterior_diam"]["sd"]

#########################
#########################
#########################
#########################


