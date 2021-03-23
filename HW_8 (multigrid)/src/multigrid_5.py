'''
Created on 11 Nov 2014

@author: Kieran Finn
'''
import numpy as np
from copy import copy
'''the multigrid method for the 5 point stencil and piecewise constant interpolation'''



'''this all has box size L=1., which will be accounted for by a redefinition of f'''
def SOR(w,phi,f):#Red black ordering SOR algorithm using the 5 point stencil and periodic BCs
    N,_=phi.shape    
    l=1./float(N)
    phi_l=np.roll(phi, 1, 0)#left neighbour
    phi_r=np.roll(phi,-1,0)#right neighbour
    phi_u=np.roll(phi,1,1)#up neighbour
    phi_d=np.roll(phi,-1,1)#down neighbour
    neighbours=phi_l+phi_r+phi_d+phi_u#sum of the neighbours
    gs=(1./4.)*(neighbours-(l**2)*f)#the gaus seidel algorithm would implement just this for all sites
    #red
    phi[::2,::2]=(1.-w)*phi[::2,::2]+w*gs[::2,::2]
    phi[1::2,1::2]=(1.-w)*phi[1::2,1::2]+w*gs[1::2,1::2]
    
    #black
    phi[::2,1::2]=(1.-w)*phi[::2,1::2]+w*gs[::2,1::2]
    phi[1::2,::2]=(1.-w)*phi[1::2,::2]+w*gs[1::2,::2]
    return phi

def GS(phi,f):#Gauss-Seidel is a special case of SOR with w=1
    return SOR(1.,phi,f)

def smooth(phi,f,N):#simply applies GS N times
    for i in range(N):
        phi=GS(phi,f)
    return phi
    
def restrict(phi):#uses the stencil ((1,1),(1,1))
    '''this may cause errors if x,y are not even'''
    phi_d=np.roll(phi, -1, 0)#left neighbour
    phi_r=np.roll(phi,-1,1)#up neighbour
    phi_rd=np.roll(np.roll(phi,-1,1),-1,0)#corner
    out=(1./8.)*(phi+phi_r+phi_d+phi_rd)[::2,::2]
    out=copy(out)#ensures we get a new array not just a view to the fine grid
    return out
    
def prolong(phi):#uses the stencil((1,1),(1,1))
    x,y=phi.shape
    out=np.zeros((2*x,2*y))
    out[::2,::2]=phi
    out[1::2,::2]=phi
    out[::2,1::2]=phi
    out[1::2,1::2]=phi
    out=copy(out)
    return out

def apply_A(phi):#applies the 5 point stencil to the matrix phi, box size is L=1.
    N,_=phi.shape
    l=1./float(N)
    phi_u=np.roll(phi, 1, 0)#left neighbour
    phi_d=np.roll(phi,-1,0)#right neighbour
    phi_l=np.roll(phi,1,1)#up neighbour
    phi_r=np.roll(phi,-1,1)#down neighbour
    return (1./(l**2))*(phi_l+phi_r+phi_u+phi_d-4*phi)

def main(phi,f,gamma,m1,m2):#f must already be normalised so that the box is L=1
    #print 'pre smoothing'
    phi=smooth(phi,f,m1)#pre-smoothing
    if min(phi.shape)>2:#not yet on the coarsest grid
        d=f-apply_A(phi)
        d=restrict(d)
        #print 'restricting to %dX%d grid' %d.shape
        psi=np.zeros_like(d)
        for i in range(gamma):
            psi=main(psi,d,gamma,m1,m2)
        #print 'prolonging back to the %dX%d grid' %phi.shape
        phi=phi+prolong(psi)
    #print 'post smoothing'
    phi=smooth(phi,f,m2)
    return copy(phi)