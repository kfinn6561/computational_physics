'''
Created on 15 Nov 2014

@author: Kieran Finn
'''
import pylab as p
import numpy as np
from copy import copy
import multigrid_5 as MG
from functions import progress_bar,pdump,barchart
from time import clock

def phi_test(x,y):#the real analytic solution, used to create the BCs and RHS of Poisson eqn
    return 4.*np.sin(6.*np.pi*x)*np.cos(2.*np.pi*y)

def gradphi_test(x,y):#the RHS of Poisson equation
    return -160.*np.pi*np.pi*np.sin(6.*np.pi*x)*np.cos(2.*np.pi*y)


N=2**8
pre_iterations=2#get into the asymptotic region
iterations=10

ms=range(1,21)#sum of m1 and m2
gammas=[0,1,2]

L=1.#length of grid
data=[]

gammadict={1:'V cycle',2:'W cycle',0:'GS'}
timedict={g:0. for g in gammadict.values()}

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
    m1=M/2
    m2=M-m1
    print '\n\n'
    print 'm1=%d, m2=%d' %(m1,m2)
    temp_data=[]
    for gamma in gammas:
        print '\n'
        print 'gamma=%d\n'%gamma
        
        phi=copy(phi0)
        start=clock()
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
        timedict[gammadict[gamma]]+=clock()-start
        temp_data.append(out/iterations)
    data.append(temp_data)
    
pdump([ms,gammas,data],'compare_m_%d' %N)

p.plot(ms,data)
p.title('Comparison of convergence for different values of m1 and m2. N=%d' %N)
p.xlabel('m1+m2')
p.ylabel('rho')
p.legend([gammadict[g] for g in gammas], loc='lower right')
p.ylim(0,1)
p.savefig('compare_m_%d.jpg' %N)

N_tot=float((iterations+pre_iterations)*len(ms))

for g in gammadict.values():
    timedict[g]/=N_tot
p.figure()
barchart(timedict)
p.ylabel('average time per iteration/s')
p.title('cpu time for each method')
p.savefig('timing_%d.jpg' %N)


p.show()

print '\ndone'