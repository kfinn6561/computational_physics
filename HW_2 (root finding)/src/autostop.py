'''
Created on Sep 10, 2014

@author: Kieran
'''
import numpy as np

# input f and its derivative (might want to improve to calculate derivative numerically or symbolically)
f=lambda x: np.exp(x)
fp=lambda x:np.exp(x)
fstring='e^x' #a string to use as a header in the output
xstar=0.

bracket=[-1,np.pi]
xacc=1e-10

guess=(bracket[0]+bracket[1])/2

outfile=open('%s_autostop.txt' %fstring,'w')


def Newton(g,gp,x,xacc, verbose=True,maxit=200):
    f=lambda y:y-g(y)/gp(y)
    x=float(x)
    x0=x-3*xacc
    out=[x]
    count=0
    while np.abs(x-x0)>xacc and count<maxit:
        x0=x
        x=f(x)
        out.append(x)
        count+=1
        
    if verbose:
        return out
    else:
        return out[-1]
    
def bisection(g,x0,x1, xacc,verbose=True,maxit=200):
    '''currently no test to check that you actually start with a bracket, might want to include'''
    x0=float(x0)
    x1=float(x1)
    low=[x0]
    high=[x1]
    count=0
    switch=np.sign(g(x0)) #this remembers if the function goes - to + or vice versa
    while np.abs(x0-x1)>xacc and count<maxit:
        count+=1
        x=(x0+x1)/2
        if g(x)*switch>0:
            x0=x
        else:
            x1=x
        low.append(x0)
        high.append(x1)
    if verbose:
        return [low,high]
    else:
        return (low[-1]+high[-1])/2
    
def regula_falsi(g,x0,x1, xacc,verbose=True,maxit=200):
    x0=float(x0)
    x1=float(x1)
    low=[x0]
    high=[x1]
    y0=g(x0)
    y1=g(x1)
    switch=np.sign(y0)
    count=0
    while np.abs(x0-x1)>xacc and count<maxit:
        count+=1
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


   
def secant(g,x0,x1, xacc,verbose=True,maxit=200):
    x0=float(x0)
    x1=float(x1)
    out=[x0,x1]
    y0=g(x0)
    y1=g(x1)
    count=0
    while np.abs(x0-x1)>xacc and count<maxit:
        count+=1
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

   
outfile.write('Newtons method\n')
outfile.write('iteration\troot\t\terror\n')

Nroots=Newton(f,fp,guess,xacc)

for i in range(len(Nroots)):
    outfile.write('%d\t\t%.10f\t%.6e\n' %(i,Nroots[i],np.abs(Nroots[i]-xstar)))


outfile.write('\n\nBisection Method\n')
outfile.write('iteration\tlower bound\tupper bound\terror\n')

broots=bisection(f,bracket[0],bracket[1],xacc)

for i in range(len(broots[0])):
    outfile.write('%d\t\t%.10f\t%.10f\t%.6e\n' %(i,broots[0][i],broots[1][i],np.abs((broots[1][i]+broots[0][i])/2-xstar)))
 
    
outfile.write('\n\nRegula Falsi Method\n')
outfile.write('iteration\tlower bound\tupper bound\terror\n')

rfroots=bisection(f,bracket[0],bracket[1],xacc)

for i in range(len(rfroots[0])):
    outfile.write('%d\t\t%.10f\t%.10f\t%.6e\n' %(i,rfroots[0][i],rfroots[1][i],np.abs((rfroots[1][i]+rfroots[0][i])/2-xstar)))
   
   
outfile.write('\n\nSecant method\n')
outfile.write('iteration\troot\t\terror\n')

sroots=Newton(f,fp,guess,xacc)

for i in range(len(sroots)):
    outfile.write('%d\t\t%.10f\t%.6e\n' %(i,sroots[i],np.abs(sroots[i]-xstar)))
   
outfile.close()
print 'done'
