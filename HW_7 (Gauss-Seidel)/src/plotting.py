'''
Created on 5 Nov 2014

@author: Kieran Finn
'''
import pylab as p
import numpy as np
from functions import pload

def theory(N,w):
    mu=np.cos(np.pi/N)
    b=2.*(w-1.)-mu**2*w**2
    c=(w-1.)**2
    if b**2-4*c<0:
        return w-1
    else:
        return (-b+np.sqrt(b**2-4*c))/2.#do I want plus or minus?


def get_theory(N):
    return np.vectorize(lambda x:theory(N,x))

fname='plotting_data.dat'

data,ws=pload(fname)
ws=np.array(ws)

X=[]
Y=[]#for the rho vs N plot

Ns=np.sort(data.keys())

for N in Ns:
    X.append(N)
    i=data[N].index(min(data[N]))
    Y.append(ws[i])#collects the data for the final plot
    
    p.figure()
    p.plot(ws,data[N],'x')
    f=get_theory(N)
    p.plot(ws,f(ws))
    p.xlim(1,2)
    p.ylim(0,1.1)
    p.xlabel('w')
    p.ylabel('rho')
    p.title('N=%d' %N)
    p.savefig('convergence_N=%d.png' %N)
    
X=np.array(X)
Y=np.array(Y)

p.figure()
p.plot(X,Y,'x')
p.plot(X,2.-2*np.pi/X)
p.ylim(1,2)
p.xlabel('N')
p.ylabel('w_opt')
p.title('optimal w')
p.savefig('optimal_w.png')

p.show()
print 'done'

