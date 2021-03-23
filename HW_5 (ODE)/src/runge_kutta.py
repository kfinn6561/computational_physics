'''
Created on 4 Oct 2014

@author: Kieran Finn
'''
import numpy as np


def Euler(f, x, y, h): #y may be a vector, make sure f is set up for that
    return y+h*f(x,y)

def RK2step(f,x, y, h):
    k1=h*f(x,y)
    k2=h*f(x+h,y+k1)
    return y+0.5*(k1+k2)

def RK4step(f,x,y,h):
    k1=h*f(x,y)
    k2=h*f(x+0.5*h,y+0.5*k1)
    k3=h*f(x+0.5*h,y+0.5*k2)
    k4=h*f(x+h,y+k3)
    return y+(1./6.)*(k1+2*k2+2*k3+k4)


iterators={1:Euler,2:RK2step,4:RK4step}#update this if higher order methods are programmed


def fixed_step(f,x0,x1,h,y0, order=1, verbose=0):
    try:
        iterator=iterators[order]
    except KeyError:
        print 'ERROR: order %g Runge Kutta method does not exist or has not been programmed'
        return False
    
    try:
        if (x1-x0)/h<0:
            print 'ERROR: the steps are going in the wrong direction'
            return False
    except ZeroDivisionError:
        print "ERROR: step size is zero"
        return False
    
    x=float(x0)
    y=np.array(y0,np.float)
    
    '''verbose has 6 levels: 0-1, do not print, 2-3, print, 4-5, print and stop after each iteration.
    Even (0,2,4) return just the answer, odd return all iterations in a list'''
    verbose=int(verbose)
    output=(verbose%2==1)#true for even, false for odd
    printing=(verbose>=2)#true if printing is required
    stopping=(verbose>=4)#true if stopping is required
    
    
    if output:
        out=np.array([np.insert(y,0,x)])
    
    while x<=x1:
        if printing:
            print x,y
        y=iterator(f,x,y,h)
        x+=h
        if output:
            out=np.append(out,[np.insert(y,0,x)],0)
        if stopping:
            raw_input('>')
        
    if output:
        return out
    else:
        return (x,y)
        
        
def plotable(f,x0,x1,h,y0, order):
    out=fixed_step(f,x0,x1,h,y0,order,verbose=1)
    out=out.T
    x=out[0]
    y=out[1]
    return (x,y)

def evaluate(f,x0,x1,h,y0, order):
    '''since the finishing value may not be an exact number of steps away, this performs one additional step to bring you to x1'''
    x,y=fixed_step(f,x0,x1,h,y0, order,verbose=0)
    h=x1-x#the size of the additional step to be made
    iterator=iterators[order]
    return iterator(f,x,y,h)
    

    
def find_y(f,x0,y0,h,y1, order, index):#finds x st y[index](x)=y1    
    try:
        iterator=iterators[order]
    except KeyError:
        print 'ERROR: order %g Runge Kutta method does not exist or has not been programmed'
        return False
    
    y=y0
    x=x0
    
    y_keep=[y[index]-y1]
    for i in range(2):#creates a list of 3 y values which will be used to find an accurate value of x(y=y1) 
        y=iterator(f,x,y,h)
        x+=h
        y_keep.append(y[index]-y1)
        
    switch=np.sign(y[index]-y1)#determines if the function is going -to + or vice versa
    
    while switch*(y[index]-y1)>0:
        y=iterator(f,x,y,h)
        x+=h
        y_keep.append(y[index]-y1)
        del y_keep[0]
        
    x_keep=[x-2*h,x-h,x]
    a,b,c=np.polyfit(x_keep,y_keep,2)
    
    return (0.-b-switch*np.sqrt(b**2-4*a*c))/(2*a)

def pass_y(f,x0,y0,h,y1, order, index, min_iter=3):#keeps iterating until y passes through the value y1  
    '''min_+iter allows you to start just to one side of the root (e.g. roundoff)'''
    try:
        iterator=iterators[order]
    except KeyError:
        print 'ERROR: order %g Runge Kutta method does not exist or has not been programmed'
        return False
    
    x,y=fixed_step(f,x0,x0+min_iter*h,h,y0,order,verbose=0)
        
    switch=np.sign(y[index]-y1)#determines if the function is going -to + or vice versa
    
    while switch*(y[index]-y1)>0:
        y=iterator(f,x,y,h)
        x+=h
        
    return (x,y)