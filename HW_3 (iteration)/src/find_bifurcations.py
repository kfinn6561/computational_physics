'''
Created on Sep 23, 2014

finds the value of a where a bifurcation occurs for a given order

@author: Kieran
'''

from functions import *
import numpy as np
import sys

def getf(a):
    return lambda x: a*x*(1.-x)

def getfp(a):
    return lambda x: a*(1.-2*x)

def get_fp_and_f(f,fp,x,m):#returns f^m(x) and f'^m(x)
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
        if np.abs(fm-x)<ytol*x and np.abs(x-x0)<=xtol:
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
        
    f,fp=get_fp_and_f(getf(a),getfp(a),x,m)
    return fp +1#need the plus 1 as we're looking for f'[x]=-1
    
def secant_with_brackets(f,xl,xr,xtol=1e-13):
    xr0=xr
    x0=xl
    y0=f(x0)
    maxit=100
    count=0
    while True:
        print 'current bracket is %.6f-%.6f' %(xl,xr)
        y1=f(xr)
        if y1<0 or np.abs(y1)>2: #|y1|>2 means we are in the oscilatory phase
            break
        count+=1
        if count>maxit:
            print 'ERROR: cannot find a starting bracket'
            sys.exit(1)
        if y1>0:
            print 'both roots lie on the same side, increasing xr'
            if xr==xr0:
                xr*=1.1
                xr0=xr
            else:
                xr=(xr+xr0)/2
        else:            
            print 'couldn\'t find the orbit for this value of a, decreasing xr'
            xr0=xr
            xr=(xl+xr)/2
    
    x1=xr
    
    '''assumes that the function goes from negative to positive with increasing a, which it should do'''
    while xr-xl>xtol:
        print 'current bracket is %.6f-%.6f' %(xl,xr)
        try:
            x=(x0*y1-x1*y0)/(y1-y0)#may want to rewrite so more numerically stable
        except ZeroDivisionError:
            x=xr+1# forces it to do bisection
        if x>xr or x<xl:#outside bracket
            x=(xl+xr)/2#use bisection
        y0=y1
        y1=f(x)
        if y1<0 or np.abs(y1)>2:#update the bracketing interval (|y1|>2 means we are in the unstable oscilatory phase)
            xr=x
        else:
            xl=x
            
        x0=x1
        x1=x
    
    return (xl+xr)/2
        

'''main program'''
   
m=2**int(getfloat('Choose value n so that the period is 2^n',Range=[0,np.inf]))#m=2^n
print 'searching for orbits of period %d\n' %m
a0=getfloat('Choose lower bound for a')
a1=getfloat('Choose upper bound for a')

x0=getfloat('Choose a starting value, x0', Range=[0,1])
print '\n\n'

#import time
#t1=time.clock()
a=secant_with_brackets(lambda a:findroot(a,m,x0),a0,a1)
#t=time.clock()-t1
print'\n\n'

print 'bifurcation point for %d->%d period orbits found at %f' %(m,2*m,a)
#print 'calculation took %f seconds' %t

print 'done'
    