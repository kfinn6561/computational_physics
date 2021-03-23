'''
Created on 4 Oct 2014

@author: Kieran Finn
'''
import numpy as np
import pylab as p
from runge_kutta import plotable

GMh=1. #the numerical value of GM/h^2
zo=np.array([0,1])
omo=np.array([1,-1])

def newton_orbit(x,y):
    return GMh*zo+omo*y[::-1]


eps=0.2#eccentricity


namestring='orbits_epsilon=%g' %eps
phi,u=plotable(newton_orbit,0,2*np.pi,0.01,[GMh*(1+eps),0],order=4)

r=1/u

ax=p.subplot(111,polar=True)
ax.plot(phi,r)
p.savefig(namestring+'.png')
p.show()

print 'done'