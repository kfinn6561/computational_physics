'''
Created on 2 Nov 2014

@author: Kieran Finn
'''
import numpy as np
from copy import copy
from collections import defaultdict

up=np.array([0,1])
down=np.array([0,-1])
left=np.array([1,0])
right=np.array([-1,0])

spirals=defaultdict(lambda :np.array([False]))
def get_spiral(X,Y):
    global spirals
    XY=[X,Y]
    if spirals[(X,Y)].any():
        return spirals[(X,Y)]
    x=np.array([-1,0])
    out=[]
    directs=[left,up,right,down]
    d=0
    while XY[0]+XY[1]>0:
        for i in range(XY[d%2]):
            x+=directs[d]
            out.append(copy(x))
        d+=1
        d=d%4
        XY[d%2]-=1
    out=np.array(out)
    spirals[(X,Y)]=copy(out)
    return out

lexicog=defaultdict(lambda :np.array([False]))
def get_lexicog(X,Y):
    global lexicog
    if spirals[(X,Y)].any():
        return lexicog[(X,Y)]
    out=[]
    for i in range(X):
        for j in range(Y):
            out.append([i,j])
    out=np.array(out)
    lexicog[(X,Y)]=copy(out)
    return out


def SOR(w,phi,f,l):
    '''w is the weight, f is the function on the RHS of the poisson equation, l is the distance between lattice sites
    phi must be a matrix so that you can easily see the neighbours. Includes boundary data as edges'''
    X,Y=phi.shape
    order=get_spiral(X-2,Y-2)+1#I'm using a spiral ordering whereby we start on the boundary and spiral inwards. In this way I hope the boundary data will propogate inwards quickly'
    #order=get_lexicog(X-2,Y-2)+1
    lx,ly=l
    for i in order:
        phi[tuple(i)]=(1-w)*phi[tuple(i)]+(w/(2.*(lx**2+ly**2)))*(ly**2*(phi[tuple(i+left)]+phi[tuple(i+right)])+lx**2*(phi[tuple(i+up)]+phi[tuple(i+down)])-(lx**2)*(ly**2)*f[tuple(i)])
    return phi

def GS(phi,f,l):#Gauss-Seidel is a special case of SOR with w=1
    return SOR(1.,phi,f,l)



















def SOR_RB(w,phi,f,l):# a more efficient version of SOR using red_black ordering
    lx,ly=l
    lx=lx**2
    ly=ly**2
    #red
    phi[1:-1:2,1:-1:2]=(1.-w)*phi[1:-1:2,1:-1:2]+(w/(2.*(lx+ly)))*((phi[:-2:2,1:-1:2]+phi[2::2,1:-1:2])*ly+(phi[1:-1:2,:-2:2]+phi[1:-1:2,2::2])*lx-lx*ly*f[1:-1:2,1:-1:2])
    phi[2:-1:2,2:-1:2]=(1.-w)*phi[2:-1:2,2:-1:2]+(w/(2.*(lx+ly)))*((phi[1:-2:2,2:-1:2]+phi[3::2,2:-1:2])*ly+(phi[2:-1:2,1:-2:2]+phi[2:-1:2,3::2])*lx-lx*ly*f[2:-1:2,2:-1:2])
    
    #black
    phi[2:-1:2,1:-1:2]=(1.-w)*phi[2:-1:2,1:-1:2]+(w/(2.*(lx+ly)))*((phi[1:-2:2,1:-1:2]+phi[3::2,1:-1:2])*ly+(phi[2:-1:2,:-2:2]+phi[2:-1:2,2::2])*lx-lx*ly*f[2:-1:2,1:-1:2])
    phi[1:-1:2,2:-1:2]=(1.-w)*phi[1:-1:2,2:-1:2]+(w/(2.*(lx+ly)))*((phi[:-2:2,2:-1:2]+phi[2::2,2:-1:2])*ly+(phi[1:-1:2,1:-2:2]+phi[1:-1:2,3::2])*lx-lx*ly*f[1:-1:2,2:-1:2])
    return phi

def GS_RB(phi,f,l):#Gauss-Seidel is a special case of SOR with w=1
    return SOR_RB(1.,phi,f,l)
        