'''
Created on 4 Dec 2014

@author: Kieran Finn
'''
import pylab as p
import numpy as np
from functions import pload

fname='metropolis_16_0.1_cold'

E,M,spins0,changes,meta_data=pload(fname+'.dat')
beta,L,start,iterations=meta_data

M2=np.array(M)**2

p.plot(E)
p.xlabel('time')
p.ylabel('E')
p.title('Energies beta=%g, L=%d, %s' %(beta,L,start))
p.savefig('energy_%d_%g_%s.png' %(L,beta,start))

p.figure()
p.plot(M)
p.xlabel('time')
p.ylabel('M')
p.title('Magnetisation beta=%g, L=%d, %s' %(beta,L,start))
p.savefig('magnetisation_%d_%g_%s.png' %(L,beta,start))

p.figure()
p.plot(M2)
p.xlabel('time')
p.ylabel('M^2')
p.title('Magnetisation^2 beta=%g, L=%d, %s' %(beta,L,start))
p.savefig('M2_%d_%g_%s.png' %(L,beta,start))

p.show()