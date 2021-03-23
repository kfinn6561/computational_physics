'''
Created on 4 Oct 2014

@author: Kieran Finn
'''
import pylab as p
import numpy as np
from useful import *
from runge_kutta import *

eps=getfloat('Choose eccentricity', Range=[0,1])
namestring='relativity_epsilon=%g' %eps

'''scientific constants. put all =1. for testing'''
G=1.
M=1.
c=1.

zo=np.array([0,1])
omo=np.array([1,-1])

index2order={0:1,1:2,2:4}

def GR_orbit(x,y,hh):#need to include h as an input to the function will call using a lambda
    yt=y[::-1]
    return omo*yt+(G*M/(hh**2))*zo+(3.*G*M/(c**2))*zo*(yt**2)

def h(l):
    return G*M/(np.sqrt(l)*c)

def y0(l):
    return np.array([(G*M/(h(l)**2))*(1+eps),0],float)

l0=1e-10
l1=1
dl=2#starting, finishing and multiplicative lambdas

step_size=0.002


x0=0.
l=float(l0)


XX=[]
YY=[]

while l<l1*dl:
    print l
    XX.append(l)
    hh=h(l)
    GR=lambda x,y: GR_orbit(x,y,hh)
    x1,y1=pass_y(GR,x0,y0(l),step_size,0.,4,1)
    YY.append(find_y(GR,x1,y1,step_size,0.,4,1))
    l*=dl

YY=np.abs(np.array(YY)-2*np.pi)

outfile=open(namestring+'.txt','w')
outfile.write('Deviations in angle with epsilon=%g\n' %eps)
outfile.write('lambda\tdelta phi\n')    
for i in range(len(XX)):
    outfile.write('%.4g\t\t%.4g\n' %(XX[i],YY[i]))
outfile.close()
XX=np.array(XX)

p.plot(XX,YY,'s')
p.plot(XX,6*np.pi*XX)
p.loglog()
p.xlabel('lambda')
p.ylabel('delta phi')
p.legend(['data','6*pi*lambda'],loc='lower right')
p.title(namestring)
p.savefig(namestring+'.png')
p.show()

print 'done'
