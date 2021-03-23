'''
Created on 7 Oct 2014

@author: Kieran Finn
'''
import pylab as p
import numpy as np
from useful import *
from runge_kutta import *

'''unless specified all units are SI. i.e. m, kg, s'''

G=6.673e-11#Newton's constant
M=1.98855e30#mass of the sun
c=2.99792458e8#speed of light

eps=0.2056#eccentricity of orbit

v_min=58.98*1e3 #minimum speed
perihelion=46.00*1e6*1e3#perihelion distance
m=0.3301e24 #mass of mercury

l=v_min*perihelion#the specific orbital angular momentum. since, at perihelion dr/dt=0.
L=l*m#total angular momentum

lam=(G*M/(l*c))**2
GMl=G*M/(l**2)

period=87.969#in days
century=365.25*100.#days in a century

zo=np.array([0,1])
omo=np.array([1,-1])


def dimless_GR_orbit(x,y):
    yt=y[::-1]
    return omo*yt+zo+3.*lam*zo*(yt**2)

def rad_to_sec(theta):
    deg=theta*180./np.pi
    sec=deg*3600.
    return sec

step_size=0.002


x0=0.
y0=np.array([1./(perihelion*GMl),0],float)


x1,y1=pass_y(dimless_GR_orbit,x0,y0,step_size,0.,4,1)
dx=find_y(dimless_GR_orbit,x1,y1,step_size,0.,4,1)-2*np.pi#angle lost per orbit

out=dx*century/period#*number of orbits in a century

out=rad_to_sec(out)#convert to arcseconds

print out

phi,u=plotable(dimless_GR_orbit,0,2*np.pi,step_size,y0,order=4)

r=1/u

ax=p.subplot(111,polar=True)
ax.plot(phi,r)
p.show()

print 'done'
