'''
Created on 4 Oct 2014

@author: Kieran Finn
'''
import pylab as p
import numpy as np
from useful import *
from runge_kutta import evaluate

GMh=1. #the numerical value of GM/h^2
zo=np.array([0,1])
omo=np.array([1,-1])

index2order={0:1,1:2,2:4}

def newton_orbit(x,y):
    return GMh*zo+omo*y[::-1]

eps=getfloat('Choose eccentricity', Range=[0,1])
namestring='closure_epsilon=%g' %eps

h0=getfloat('Choose smallest step size', Range=(0,np.inf))
h1=getfloat('Choose largest step size', Range=(h0,np.inf))
dh=getfloat('Choose multiplicative factor', Range=(1,np.inf))

x0=0
y0=[GMh*(1+eps),0]

y0=np.array(y0,float)
h=float(h0)

x=[]
y=[[],[],[]]
yp=[[],[],[]]

while h<h1*dh:
    print h
    x.append(h)
    for i in range(3):
        u,v=evaluate(newton_orbit,x0,2*np.pi,h,y0,index2order[i])
        y[i].append(1./u-1./y0[0])#structure of RK inputs is f, x0,x1,dx,y0,order
        yp[i].append(v)
        '''this is structured so that what's plotted is r(2pi)-r(0) (=1/u(2pi)-1/u(0))'''
    h*=dh

outfile=open(namestring+'_position.txt','w')
outfile.write('deviations of position from closure with epsilon=%g\n' %eps)
outfile.write('step size\tEuler\tRK2\tRK4\n')    
for i in range(len(x)):
    outfile.write('%.4g\t\t%.4g\t%.4g\t%.4g\n' %(x[i],y[0][i],y[1][i],y[2][i]))
outfile.close()

outfile=open(namestring+'_velocity.txt','w')
outfile.write('deviations of velocity from closure with epsilon=%g\n' %eps)
outfile.write('step size\tEuler\tRK2\tRK4\n')    
for i in range(len(x)):
    outfile.write('%.4g\t\t%.4g\t%.4g\t%.4g\n' %(x[i],yp[0][i],yp[1][i],yp[2][i]))
outfile.close()

y=np.abs(np.array(y))
p.plot(x,y[0],'x',x,y[1],'^',x,y[2],'s')
p.loglog()
p.xlabel('step size')
p.ylabel('position deviation from closure')
p.title(namestring+':position')
p.legend(['euler','rk2','rk4'],loc='lower right')
p.savefig(namestring+'_position.png')

p.figure()
yp=np.abs(np.array(yp))
p.plot(x,yp[0],'x',x,yp[1],'^',x,yp[2],'s')
p.loglog()
p.xlabel('step size')
p.ylabel('velocity deviation from closure')
p.title(namestring+': velocity')
p.legend(['euler','rk2','rk4'],loc='lower right')
p.savefig(namestring+'_velocity.png')
p.show()

print 'done'
