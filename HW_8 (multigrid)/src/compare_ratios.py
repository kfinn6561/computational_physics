'''
Created on 15 Nov 2014

@author: Kieran Finn
'''
import pylab as p
import numpy as np
from copy import copy
import multigrid_5 as MG
from functions import progress_bar,pdump

def phi_test(x,y):#the real analytic solution, used to create the BCs and RHS of Poisson eqn
    return 4.*np.sin(6.*np.pi*x)*np.cos(2.*np.pi*y)

def gradphi_test(x,y):#the RHS of Poisson equation
    return -160.*np.pi*np.pi*np.sin(6.*np.pi*x)*np.cos(2.*np.pi*y)


N=2**8
pre_iterations=2#get into the asymptotic region
iterations=10

ms=range(1,21)#sum of m1 and m2
ratios=[(3,1),(2,1),(1,1),(1,2),(1,3)]
gamma=1

fname='multigrid_data.dat'
L=1.#length of grid
data=[]

gammadict={1:'V',2:'W',0:'GS'}

'''
def error(phi,f):
    eps=(MG.apply_A(phi)-f)
    eps=eps.flatten()
    eps=np.abs(eps)
    N=len(eps)
    eps=np.sum(eps)
    return eps/N
'''

def error(phi,phi_exact):
    N=len(phi.flatten())
    phi_bar=np.sum(phi)/N
    eps=phi-phi_bar-phi_exact
    eps=np.abs(eps)
    eps=eps.flatten()
    eps=np.sum(eps)
    return eps/N

l=L/float(N)
    
'''initialise'''
phi0=np.zeros((N,N))
x=np.arange(N)*l
y=np.arange(N)*l#change this line if asymetric grid needed
X,Y=np.meshgrid(x,y)
f=gradphi_test(X,Y)
phi_exact=phi_test(X,Y)
f=f/(L**2)#renormalise f so that the box size is 1.


for M in ms:
    temp_data=[]
    for ratio in ratios:
        phi=copy(phi0)
        r1,r2=ratio
        m1=int(np.round((float(r1)/(r1+r2))*M))
        m2=M-m1   
        print '\n\n'
        print 'm1=%d, m2=%d' %(m1,m2)
        
        for i in range(pre_iterations):
            phi=MG.main(phi,f,gamma,m1,m2)
            
        old=False
        new=False
        out=0.
        for i in range(iterations+1):
            progress_bar(i,iterations+1)
            phi=MG.main(phi,f,gamma,m1,m2)
            old=new
            new=error(phi,phi_exact)
            if old:
                out+=new/old
        temp_data.append(out/iterations)
    data.append(temp_data)
    
pdump([ms,ratios,data],'compare_ratio_%d' %N)

p.plot(ms,data)
p.title('Comparison of convergence for different ratios of m1 and m2. N=%d' %N)
p.xlabel('m1+m2')
p.ylabel('rho')
p.legend([str(r) for r in ratios],loc='lower right')
p.ylim(0,1)
p.savefig('compare_ratio_%d.jpg' %N)

p.show()

print '\ndone'