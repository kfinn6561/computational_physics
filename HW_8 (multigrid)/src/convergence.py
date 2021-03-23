'''
Created on 11 Nov 2014

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

pre_iterations=2#get into the asymptotic region
iterations=10

Ns=[2**4,2**5,2**6,2**7,2**8,2**9,2**10,2**11]#number of grid points
gamma=0
m1=2#pre smoothings
m2=2#post smoothings

fname='multigrid_data.dat'
L=1.#length of grid
data=[]

toplot=[[] for i in range(len(Ns))]

gammadict={1:'V',2:'W',0:'GS'}


def error(phi,phi_exact):
    N=len(phi.flatten())
    phi_bar=np.sum(phi)/N
    eps=phi-phi_bar-phi_exact
    eps=np.abs(eps)
    eps=eps.flatten()
    eps=np.sum(eps)
    return eps/N
'''

def error(phi,f):
    eps=(MG.apply_A(phi)-f)
    eps=eps.flatten()
    eps=np.abs(eps)
    N=len(eps)
    eps=np.sum(eps)
    return eps/N
'''

for I in range(len(Ns)):
    N=Ns[I]
    print '\n\nN=%d'%N
    l=L/float(N)
    
    '''initialise'''
    phi=np.zeros((N,N))
    x=np.arange(N)*l
    y=np.arange(N)*l#change this line if asymetric grid needed
    X,Y=np.meshgrid(x,y)
    f=gradphi_test(X,Y)
    phi_exact=phi_test(X,Y)
    f=f/(L**2)#renormalise f so that the box size is 1.
    
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
        toplot[I].append(new)
        if old:
            out+=new/old
    data.append(out/iterations)
    
pdump([Ns,data],'critical_slowing_down_%s.dat' %gammadict[gamma])

p.plot(Ns,data)
p.semilogx()
p.title('Critical slowing down in %s cycle' %gammadict[gamma])
p.xlabel('grid size')
p.ylabel('rho')
p.ylim(0,1)
p.savefig('critical_slowing_down_%s.jpg' %gammadict[gamma])

p.figure()
y=np.array(toplot).T
p.plot(y)
p.title('convergence of result for different Ns')
p.xlabel('iteration')
p.ylabel('error')
p.legend([str(N) for N in Ns])
p.savefig('convergence%s.jpg' %gammadict[gamma])
p.show()

print '\ndone'