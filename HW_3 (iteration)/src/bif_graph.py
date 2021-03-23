'''
Created on 1 Oct 2014

@author: Kieran Finn
'''
from functions import *
import numpy as np
import sys
import pylab as p

input_file='bifurcations_from_1_to_1024.txt'
grid=100
x0=0.4

def getf(a):
    return lambda x: a*x*(1.-x)

def getfp(a):
    return lambda x: a*(1.-2*x)

def get_fp_and_f(f,fp,x,m):
    fs=iterate(f, x, m, verbose=1)#returns a list of f0(x)-fm(x)
    fout=fs[-1]
    fpout=1
    for i in range(len(fs)-1): #fm'(x)=prod f'(fk(x)) (k: 0 - m-1)
        fpout*=fp(fs[i])
    return (fout,fpout)
    
def Newton(a,m,x,xtol=1e-13, ytol=1e-10, verbose=False,maxit=2000):
    f=getf(a)
    fp=getfp(a)
    
    x=float(x)
    out=[x]
    count=0
    while True:
        fm,fpm=get_fp_and_f(f, fp, x, m)
        x0=x
        x=x-(fm-x)/(fpm-1)#the function we're finding the root of is f(x)-x=0
        out.append(x)
        count+=1
        if np.abs(x-x0)<=xtol:
            #success
            break
        if count>maxit:
            #failure
            return False    
    if verbose:
        return out
    else:
        return out[-1]
    
def findroot(a,m,x,iterations=100,maxtimes=10):
    count=0    
    while True:
        x=iterate(getf(a),x,iterations)
        xN=Newton(a,m,x)
        if xN:#the method was successful
            x=xN
            break
        count+=1
        if count>=maxtimes:
            print 'ERROR could not achieve desired accuracy'
            return False
        
    return iterate(getf(a),x,m-1,verbose=1)




ms=[]
bfpoints=[0.]
f=open(input_file,'r')
for line in f:
    r=line.split()
    m=int(r[3].split('-')[0])
    ms.append(m)
    bfpoints.append(float(r[8]))
f.close()

for i in range(len(bfpoints)-1):
    m=ms[i]
    print 'm=%d' %m
    x=np.linspace(bfpoints[i],bfpoints[i+1],grid)
    y=[]
    for a in x:
        y.append(np.sort(findroot(a,m,x0)))
    p.plot(x,y,'b')
    
p.ylim(0,1)
p.xlabel('a')
p.ylabel('fixed points')
p.title('bifurcation diagram')
p.savefig('bifurcation_diagram.pdf')
p.savefig('bifurcation_diagram.png')
p.show()
print 'done'