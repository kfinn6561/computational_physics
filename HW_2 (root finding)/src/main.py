'''
Created on Sep 10, 2014

@author: Kieran
'''
import numpy as np

double=True

if double:
    three=3.
    two=2.
    one=1.
    dstring='double'
else:
    three=np.float32(3)
    one=np.float32(1)
    two=np.float32(2)#this is needed for singles to stay as singles, there might be a better way to do this
    dstring='single'

# input f and its derivative (might want to improve to calculate derivative numerically or symbolically)
f=lambda x: x**two-two
fp=lambda x:two*x
fstring='x^2-2' #a string to use as a header in the output
xstar=np.sqrt(2)

bracket=[1,2]

guess=(bracket[0]+bracket[1])/2

outfile=open('%s_%s.txt' %(fstring,dstring),'w')


def Newton(g,gp,x,iterations, verbose=True,double=True):
    f=lambda y:y-g(y)/gp(y)
    if double:
        x=float(x)
    else:
        x=np.float32(x)
    out=[x]
    for i in range(iterations):
        x=f(x)
        out.append(x)
        
    if verbose:
        return out
    else:
        return out[-1]
    
def bisection(g,x0,x1, iterations,verbose=True,double=True):
    '''currently no test to check that you actually start with a bracket, might want to include'''
    if double:
        x0=float(x0)
        x1=float(x1)
    else:
        x0=np.float32(x0)
        x1=np.float32(x1)
    low=[x0]
    high=[x1]
    switch=np.sign(g(x0)) #this remembers if the function goes - to + or vice versa
    for i in range(iterations):
        x=(x0+x1)/two
        if g(x)*switch>0:
            x0=x
        else:
            x1=x
        low.append(x0)
        high.append(x1)
    if verbose:
        return [low,high]
    else:
        return (low[-1]+high[-1])/two
    
def regula_falsi(g,x0,x1, iterations,verbose=True,double=True):
    if double:
        x0=float(x0)
        x1=float(x1)
    else:
        x0=np.float32(x0)
        x1=np.float32(x1)
    low=[x0]
    high=[x1]
    y0=g(x0)
    y1=g(x1)
    switch=np.sign(y0)
    for i in range(iterations):
        x=(x0*y1-x1*y0)/(y1-y0)#may want to rewrite so more numerically stable
        y=g(x)
        if y*switch>0:
            x0=x
            y0=y
        else:
            x1=x
            y1=y
        low.append(x0)
        high.append(x1)
    if verbose:
        return [low,high]
    else:
        return  (x0*y1-x1*y0)/(y1-y0)


   
def secant(g,x0,x1, iterations,verbose=True,double=True):
    if double:
        x0=float(x0)
        x1=float(x1)
    else:
        x0=np.float32(x0)
        x1=np.float32(x1)
    out=[x0,x1]
    y0=g(x0)
    y1=g(x1)
    for i in range(iterations):
        x0=x1
        y0=y1
        x1=(x0*y1-x1*y0)/(y1-y0)#may want to rewrite so more numerically stable
        y1=g(x1)
        out.append(x1)
    if verbose:
        return out
    else:
        return  out[-1] 
    
'''start main program'''
   
outfile.write('Rootfinding methods for the equation %s=0\n' %fstring)
outfile.write('using %s precision\n\n' %dstring)

   
outfile.write('Newtons method\n')
outfile.write('iteration\troot\t\terror\n')

Nroots=Newton(f,fp,guess,10,double=double)

for i in range(len(Nroots)):
    outfile.write('%d\t\t%.10f\t%.6e\n' %(i,Nroots[i],np.abs(Nroots[i]-xstar)))


outfile.write('\n\nBisection Method\n')
outfile.write('iteration\tlower bound\tupper bound\terror\n')

broots=bisection(f,bracket[0],bracket[1],30,double=double)

for i in range(len(broots[0])):
    outfile.write('%d\t\t%.10f\t%.10f\t%.6e\n' %(i,broots[0][i],broots[1][i],np.abs((broots[1][i]+broots[0][i])/2-xstar)))
 
    
outfile.write('\n\nRegula Falsi Method\n')
outfile.write('iteration\tlower bound\tupper bound\terror\n')

rfroots=bisection(f,bracket[0],bracket[1],30,double=double)

for i in range(len(rfroots[0])):
    outfile.write('%d\t\t%.10f\t%.10f\t%.6e\n' %(i,rfroots[0][i],rfroots[1][i],np.abs((rfroots[1][i]+rfroots[0][i])/2-xstar)))
   
   
outfile.write('\n\nSecant method\n')
outfile.write('iteration\troot\t\terror\n')

sroots=Newton(f,fp,guess,20,double=double)

for i in range(len(sroots)):
    outfile.write('%d\t\t%.10f\t%.6e\n' %(i,sroots[i],np.abs(sroots[i]-xstar)))
   
outfile.close()
print 'done'
