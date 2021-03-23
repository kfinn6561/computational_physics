'''
Created on 5 Nov 2014

@author: Kieran Finn
'''
'''this algorithm is set up to be specific to a (0,1)x(0,1) domain with the same step size in the x and y direction'''

import numpy as np
import pylab as p
from relaxation_algorithms import *
from collections import defaultdict
from functions import pdump, progress_bar


def phi_test(x,y):#the real analytic solution, used to create the BCs and RHS of Poisson eqn
    return 3.*x+2.*y+4.*np.sin(3.*x)*np.cos(y)

def gradphi_test(x,y):#the RHS of Poisson equation
    return -40.*np.sin(3.*x)*np.cos(y)
'''

def phi_test(x,y):#the real analytic solution, used to create the BCs and RHS of Poisson eqn
    return 2.+3.*x-2.*y+x*y

def gradphi_test(x,y):#the RHS of Poisson equation
    return 0.
'''

def norm(phi,f,l):
    out=(1./l**2)*(phi[:-2,1:-1]+phi[2:,1:-1]+phi[1:-1,:-2]+phi[1:-1,2:]-4*phi[1:-1,1:-1])-f[1:-1,1:-1]
    out=np.abs(out)    
    Nx,Ny=out.shape
    out=np.sum(out)
    out=out/(Nx*Ny)
    return out


Nw=101
L=1.
Ns=[200]#values of N to use
#Ns=[5,10] #for debug
ws=np.linspace(1.,2.,Nw)
transience=2#number of iterations to remove transience multiplied by grid size
measure=20#number of iterations to average over to find convergence rate
pname='plotting_data_200.dat'


data=defaultdict(list)

for N in Ns:
    print '\n\n\n'
    print 'N=%d' %N
    l=L/N
    phi0=np.zeros((N,N))#initialise phi to all zeros
    for i in range(N):#initialise boundary data
        phi0[(i,0)]=phi_test(i*l,0.)
        phi0[(i,-1)]=phi_test(i*l,L)
    for i in range(N):
        phi0[(0,i)]=phi_test(0.,i*l)
        phi0[(-1,i)]=phi_test(L,i*l)
    
    gradphi_grid=np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            x,y=np.array([i,j])*l
            gradphi_grid[(i,j)]=gradphi_test(x, y)
            
    pdump([dict(data),ws],pname) #means some data is till saved if the program crashes
    for w in ws:
        phi=copy(phi0)
        progress_bar(int(np.round((w-1)*Nw)),Nw)
        con1=False
        for i in range(transience*N):#more transience for bigger grid
            phi=SOR(w,phi,gradphi_grid,(l,l))
            
        out=0.
        iteration=0
        while True:
            con0=con1
            con1=norm(phi,gradphi_grid,l)
            if con0:
                out+=con1/con0
            iteration+=1
            if iteration>measure+1:
                break
            phi=SOR(w,phi,gradphi_grid,(l,l))
        out=out/measure
        data[N].append(out)

        
data=dict(data)#turns it into a regular dictionary so that it can be pickled
pdump([data,ws],pname)
print 'done'