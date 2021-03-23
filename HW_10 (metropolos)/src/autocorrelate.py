'''
Created on 5 Dec 2014

@author: Kieran Finn
'''
import pylab as p
import numpy as np
from functions import pload,get_float,progress_bar
from autocorrelate_functions import Cff
from metropolis_functions import metro

fname='16_0.2_hot'
skip=int(get_float('Select number of initial iterations to drop',[0,np.inf]))

beta=0.2
L=16
start='hot'
iterations=10000000

#E,M,spins0,changes,meta_data=pload('metropolis_'+fname+'.dat')
E,M,spins0,changes=metro(beta,L,start,iterations)

M2=np.array(M)**2


E=E[skip::]
M=M[skip::]

window=700
    
def plot(data,name):
    print '\nCalculating correlations for %s' %name
    data=np.array(data)
    mean=np.mean(data)#only need to calculate the mean once
    data=data-mean
    Cff0=Cff(data,0)
    Cs=[Cff0]
    x=[0]
    for i in range(1,window):
        progress_bar(i,window)
        Cs.append(Cff(data,i))
        x.append(i)
    Cs=np.concatenate((Cs[:0:-1],Cs))#Cff(-u)=Cff(u)
    x=np.array(x)
    x=np.concatenate((-x[:0:-1],x))
    tau=np.sum(Cs)/(2*Cff0)
    p.figure()
    p.plot(x,Cs)
    p.title('%s for beta=%g, L=%d and %s start.\n Mean is %.3g, tau is %.3g' %(name,beta,L,start,mean,tau))
    p.xlabel('u')
    p.ylabel('Cff(u)')
    p.savefig('autocorrelate_%s_%s.png' %(name,fname))
    
    
'''main program'''
plot(E,'Energy')
plot(M,'Magnetisation')
plot(M2,'M^2')

p.show()

    