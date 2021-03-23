'''
Created on 29 Sep 2014

@author: Kieran Finn
'''
import pylab as p
import numpy as np

input_file='bifurcations_from_1_to_32768.txt'


ns=[]
bfpoints=[]
f=open(input_file,'r')
for line in f:
    r=line.split()
    m=int(r[3].split('-')[0])
    ns.append(np.log2(m))
    bfpoints.append(float(r[8]))
f.close()

deltas=[]
for i in bfpoints:#find the errors from the asymptotic value (taken to be the final point)
    deltas.append(bfpoints[-1]-i)
deltas=np.array(deltas)
ns=np.array(ns)

lgdeltas=np.log(deltas)

p.plot(ns,lgdeltas,'ro')

m,c=np.polyfit(ns[:5],lgdeltas[:5],1)
p.plot(ns,m*ns+c)

p.xlabel('log_2(bifurcation order)')
p.ylabel('ln(a_inf-a)')
p.title('(a-a_inf)=%.4f(%.6f^-n)' %(np.exp(c),np.exp(-m)))
p.savefig('Feigenbaum.png')
p.show()

print 'done'