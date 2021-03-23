'''
Created on 6 Dec 2014

@author: Kieran Finn
'''
import os
import numpy as np

betas=[0.,0.01,0.1,0.2,0.3,0.4,0.44,0.5*np.log(1+np.sqrt(2)),0.5,1.,10.]
Ls=[4,8,16,32,64,128,215,512]
starts=['hot','cold']

for beta in betas:
    for L in Ls:
        for start in starts:
            os.system('python metropolis.py %g %s %d' %(beta,start,L))
            
print 'done'