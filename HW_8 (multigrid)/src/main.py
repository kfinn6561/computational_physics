'''
Created on Nov 11, 2014

@author: Kieran
'''
import pylab as p
import numpy as np
from copy import copy
import multigrid_5 as MG
from functions import pdump


def phi_test(x,y):#the real analytic solution, used to create the BCs and RHS of Poisson eqn
    return 4.*np.sin(6.*np.pi*x)*np.cos(2.*np.pi*y)

def gradphi_test(x,y):#the RHS of Poisson equation
    return -160.*np.pi*np.pi*np.sin(6.*np.pi*x)*np.cos(2.*np.pi*y)

'''

sigma=0.005
def phi_test(x,y):#the real analytic solution, used to create the BCs and RHS of Poisson eqn
    return np.exp(-((x-0.5)**2+(y-0.5)**2)/(2*sigma))

def gradphi_test(x,y):#the RHS of Poisson equation
    return (-2./sigma+(x-0.5)**2/(sigma**2)+(y-0.5)**2/(sigma**2))*np.exp(-((x-0.5)**2+(y-0.5)**2)/(2*sigma))


def phi_test(x,y):#the real analytic solution, used to create the BCs and RHS of Poisson eqn
    return 0.*x

def gradphi_test(x,y):#the RHS of Poisson equation
    return 0.*x
'''


iterations=50
N=2**4#number of grid points
gamma=0
m1=3#pre smoothings
m2=4#post smoothings

gammadict={1:'V',2:'W',0:'GS'}

fname='multigrid_%d_%s' %(N,gammadict[gamma])
#fname='multigrid_data'


def error(phi,f):
    eps=(MG.apply_A(phi)-f)
    eps=eps.flatten()
    eps=np.abs(eps)
    N=len(eps)
    eps=np.sum(eps)
    return eps/N


L=1.#length of grid
l=L/float(N)
data=[]

'''initialise'''
phi=np.zeros((N,N))
phi=np.random.rand(N,N)
phi=phi-np.sum(phi)/len(phi.flatten())


x=np.arange(N)*l+l/2
y=np.arange(N)*l+l/2#change this line if asymetric grid needed
X,Y=np.meshgrid(x,y)
f=gradphi_test(X,Y)
phi_exact=phi_test(X,Y)
f=f/(L**2)#renormalise f so that the box size is 1.

'''
def error(phi,f):
    N=len(phi.flatten())
    phi_bar=np.sum(phi)/N
    eps=phi-phi_bar-phi_exact
    eps=np.abs(eps)
    eps=eps.flatten()
    eps=np.sum(eps)
    return eps/N
'''

print 'iteration\terror'
iteration=0
errors=[]
while True:
    #data.append(phi)
    eps=error(phi,f)
    print '%d\t\t%.5g' %(iteration,eps)
    errors.append(eps)
    iteration+=1
    if iteration>iterations:
        break
    phi=MG.main(phi,f,gamma,m1,m2)

pdump([X,Y,phi_exact,data],fname+'.dat')

p.plot(errors)
p.semilogy()
p.title('Multigrid with N=%d' %N)
p.xlabel('iteration')
p.ylabel('error')
p.savefig(fname+'.jpg')
p.show()

print 'done'