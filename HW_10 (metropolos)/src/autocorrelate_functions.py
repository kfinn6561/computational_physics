'''
Created on 6 Dec 2014

@author: Kieran Finn
'''
import numpy as np


def Cff(data,u):#assumes mean has already been subtracted
    if u!=0:
        out=data[:-u:]*data[u::]
    else:
        out=data**2
    return np.mean(out) 

def tau(data,window):
    mean=np.mean(data)
    data=data-mean
    tau=0.
    Cff0=Cff(data,0)
    for i in range(1,window):
        tau+=Cff(data,i)
    return (2*tau+Cff0)/(2*Cff0)
    