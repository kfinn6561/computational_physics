'''
Created on 6 Dec 2014

@author: Kieran Finn
'''
import pylab as p
from autocorrelate_functions import tau
import numpy as np
from functions import pdump,pload
from metropolis_functions import metro


betas=[0.,0.01,0.1,0.2,0.3,0.4,0.44,0.5*np.log(1+np.sqrt(2)),0.5,1.,10.]
Ls=[4,8,16,32,64,128,215]
starts=['hot','cold']
iterations=6000000
transience=1000#number to delete from beginning
window=100

def plot(data,name):
    N=len(data)
    data=np.array(data)
    f,ax=p.subplots(N,sharex=True,figsize=(8.5,11),dpi=100)
    for i in range(N):
        ax[i].plot(betas,data[i].T)
        ax[i].semilogx()
        ax[i].set_ylabel('L=%d' %Ls[i])
    p.suptitle('Correlation times for %s' %name)
    p.xlabel('beta')
    f.text(0.06, 0.5, 'tau', ha='center', va='center', rotation='vertical')
    p.savefig('correlations_%s.pdf' %name)
 
tE=[]
tM=[]
tM2=[]
for L in Ls:
    temp_E=[]
    temp_M=[]
    temp_M2=[]
    for start in starts:
        start_E=[]
        start_M=[]
        start_M2=[]
        for beta in betas:
            E,M,_,_=metro(beta,L,start,iterations)
            
            #Actually quicker to calculate from scratch than to load the data from file
            #print 'beta=%g and %s start on a %dx%d grid' %(beta,start,L,L)
            #E,M,_,_,_=pload('metropolis_%d_%g_%s.dat' %(L,beta,start))
            
            E=E[transience::]
            M=M[transience::]
            E=np.array(E)
            M=np.array(M)
            M2=M**2
            start_E.append(tau(E,window*L))
            start_M.append(tau(M,window*L))
            start_M2.append(tau(M2,window*L))
        temp_E.append(start_E)
        temp_M.append(start_M)
        temp_M2.append(start_M2)
    tE.append(temp_E)
    tM.append(temp_M)
    tM2.append(temp_M2)
    
'''
tE,tM,tM2=pload('taus.dat')
'''
        
pdump([tE,tM,tM2],'taus.dat')
plot(tE,'Energy')
plot(tM,'Magnetisation')
plot(tM2,'M^2')
p.show()
            
            