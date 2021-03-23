'''
Created on 6 Dec 2014

@author: Kieran Finn
'''
from metropolis_functions import metro
import numpy as np
from functions import pdump,pload
import pylab as p

iterations=10000#this will be multiplied by L^2
transience=100#this will be multiplied by L^2
Ls=[4,8,16,32,64,128,215,512]
Ls=[4,8,16,32,64]

maxit=10000000#maximum number of iterations without running into memory error

beta=0.5*np.log(1+np.sqrt(2))
start='hot'

fname='susceptibility'


chis=[]
for L in Ls:
    V=L**2
    current_iterations=iterations*V
    iteration0=current_iterations%maxit
    N=(current_iterations-iteration0)/maxit
    current_transience=transience*V
    chi=0.
    if iteration0<=current_transience:
        toadd=current_transience-iteration0
        perN=toadd/N+1
        iteration0+=perN*N
        bigit=maxit-perN
    else:
        bigit=maxit
        
    _,M,spins=metro(beta,L,start,iteration0,partial=True)
    M=np.array(M[current_transience::])
    chi+=np.sum(M**2)
    
    for i in range(N):
        print '%d of %d' %(i+1,N)
        _,M,spins=metro(beta,L,'continue',bigit,spins0=spins,partial=True)
        M=np.array(M)
        chi+=np.sum(M**2)
    
    
    chi=chi/(V*(current_iterations-current_transience))
    chis.append(chi)

pdump([Ls,chis],fname+'.dat')

#Ls,chis=pload(fname+'.dat')

Ls=np.array(Ls)

gamma,a=np.polyfit(np.log(Ls),np.log(chis),1)

p.plot(Ls,chis,'ro')
p.plot(Ls,np.exp(a)*(Ls**gamma))
p.loglog()
p.xlabel('L')
p.ylabel('chi')
p.title('susceptibility at the critical point critical exponant is %.4g' %gamma)
p.savefig(fname+'.png')
p.show()
    