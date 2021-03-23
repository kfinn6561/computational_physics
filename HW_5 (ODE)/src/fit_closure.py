'''
Created on 5 Oct 2014

@author: Kieran Finn
'''
import pylab as p
import numpy as np



name='epsilon=0.85_position'

fname='closure_'+name+'.txt'
f=open(fname,'r')
r=f.readlines()
f.close()

h=[]
y=[]

for line in r[2:]:
    words=line.split()
    numbers=[]
    for word in words:
        numbers.append(float(word))
    h.append(numbers[0])
    y.append(numbers[1:])
h=np.array(h)
y=np.abs(np.array(y))

coefs=np.polyfit(np.log(h),np.log(y),1)
m=np.outer(np.ones(len(h)),coefs[0])
c=np.outer(np.ones(len(h)),np.exp(coefs[1]))
x=np.outer(h,np.ones(len(y[0])))#converts to a 2d array which can be used for plotting

y_fit=c*(x**m)
y=y.T

p.plot(h,y[0],'x',h,y[1],'^',h,y[2],'s')
p.plot(h,y_fit)
p.loglog()
p.legend(['Euler','RK2','RK4','x^%.2g' %coefs[0][0],'x^%.2g' %coefs[0][1],'x^%.2g' %coefs[0][2]],loc='lower right')
p.xlabel('step size')
p.ylabel('deviation from closure')
p.title(name)
p.savefig(name+'_fits.png')

p.show()

