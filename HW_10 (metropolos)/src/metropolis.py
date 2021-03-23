'''
Created on Dec 4, 2014

@author: Kieran
'''
import sys
from functions import pdump
from metropolis_functions import metro

beta=0.2 #temperature of the system
L=16 #LxL grid
start='hot'
iterations=10000000
verbose=False

try:
    beta=float(sys.argv[1])
    start=sys.argv[2]
    L=int(sys.argv[3])#may want some error correction
    iterations=int(sys.argv[4])
except IndexError:
    pass

fname='metropolis_%d_%g_%s' %(L,beta,start)
meta_data=[beta,L,start,iterations]

energies,magnetisations,spins0,changes=metro(beta,L,start,iterations)

    
pdump([energies,magnetisations,spins0,changes,meta_data],fname+'.dat')

if verbose:
    '''write to human readable form'''
    f=open(fname+'.txt','w')
    f.write('Metropolis algorithm with beta=%g and %s start on a %dx%d grid\n' %(beta,start,L,L))
    f.write('t\tE\tM\n')
    for i in range(len(energies)):
        f.write('%d\t%.4g\t%g\n' %(i,energies[i],magnetisations[i]))
    f.close()

    
