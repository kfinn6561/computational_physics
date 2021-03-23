'''
Created on 2 Nov 2014

@author: Kieran Finn
'''
import numpy as np
import pylab as p
from mpl_toolkits.mplot3d import axes3d#used for 3d plotting
from relaxation_algorithms import *
from functions import progress_bar
import os
import shutil
import sys

max_z=9.
min_z=-4.#for plots


def phi_test(x,y):#the real analytic solution, used to create the BCs and RHS of Poisson eqn
    return 3.*x+2.*y+4.*np.sin(3.*x)*np.cos(y)

def gradphi_test(x,y):#the RHS of Poisson equation
    return -40.*np.sin(3.*x)*np.cos(y)
'''
def phi_test(x,y):#the real analytic solution, used to create the BCs and RHS of Poisson eqn
    return 0

def gradphi_test(x,y):#the RHS of Poisson equation
    return 0
'''

iterations=130
dirname='temp'
frame=0

if os.path.exists(dirname):
    if raw_input('this directory already exists, do you want to delete it and start again? ') in ['yes','Yes','y','Y','1']:
        shutil.rmtree(dirname)
    else:
        sys.exit()
os.mkdir(dirname)

def plot(X,Y,phi,phi_exact):
    global frame
    fig=p.figure()
    ax=fig.add_subplot(111,projection='3d')
    ax.plot_wireframe(X,Y,phi,color='blue')
    ax.plot_wireframe(X,Y,phi_exact,color='green')
    p.title('iteration %03d' %frame)
    ax.set_xlim((X[(0,0)],X[(-1,-1)]))
    ax.set_ylim((Y[(0,0)],Y[(-1,-1)]))
    ax.set_zlim((min_z,max_z))
    p.savefig(dirname+'/%04d.jpg' %frame)
    p.close()
    frame+=1

def norm(phi,f,l):
    lx,ly=l
    out=(1./lx**2)*(phi[:-2,1:-1]+phi[2:,1:-1]-2*phi[1:-1,1:-1])+(1./ly**2)*(phi[1:-1,:-2]+phi[1:-1,2:]-2*phi[1:-1,1:-1])-f[1:-1,1:-1]
    out=np.abs(out)
    Nx,Ny=out.shape
    out=np.sum(out)
    out=out/(Nx*Ny)
    return out

'''initialise. To generalise to more dimensions may want to make L, l etc a vector'''

L=1.#total length of the side
Lx=L
Ly=L

l=0.01#step size
lx=l
ly=l

Nx=int(Lx/lx)
lx=Lx/Nx#may need to adjust l, because we need it to be an integer fraction of L

Ny=int(Ly/ly)
ly=Ly/Ny

l=np.array([lx,ly])#useful to have an array of the steps

Nx+=1
Ny+=1#need to include both endpoints

fname='Nx=%d_Ny=%d' %(Nx-1,Ny-1)
outfile=open(fname+'.txt','w')
outfile.write('Successive iterations of the Poisson equation using stepsizes of %g\n' %l[0])
outfile.write('\n\n Iteration\tError\n')

errors=[]
X=np.zeros((Nx,Ny))#creates an X,Y grid that will be used for plotting. Probably an easier way to do this
Y=np.zeros((Nx,Ny))
phi_exact=np.zeros((Nx,Ny))
gradphi_grid=np.zeros((Nx,Ny))
for i in range(Nx):
    for j in range(Ny):
        x,y=(i,j)*l
        X[(i,j)]=x
        Y[(i,j)]=y
        phi_exact[(i,j)]=phi_test(x, y)
        gradphi_grid[(i,j)]=gradphi_test(x, y)

phi=np.zeros((Nx,Ny))#initialise phi to all zeros
#phi=phi+2.#debug
for i in range(Nx):#initialise boundary data
    phi[(i,0)]=phi_test(i*lx,0.)
    phi[(i,-1)]=phi_test(i*lx,Ly)
for i in range(Ny):
    phi[(0,i)]=phi_test(0.,i*ly)
    phi[(-1,i)]=phi_test(Lx,i*ly)
    

    
iteration=0

while True:
    progress_bar(iteration,iterations)
    plot(X,Y,phi,phi_exact)
    error=norm(phi,gradphi_grid,l)
    errors.append(error)
    outfile.write('%d\t\t%.5g\n' %(iteration, error))
    iteration+=1
    if iteration>iterations:
        break
    phi=GS(phi,gradphi_grid,l)
    
outfile.close()

p.figure()
p.plot(errors)
p.xlabel('iteration')
p.ylabel('error')
p.title('%dX%d grid' %(Nx,Ny))
p.semilogy()
p.savefig(fname+'.png')

frame_duration=0.3
os.chdir(dirname)
os.system('ffmpeg -r %d -i %s.jpg -vcodec libx264 -y %s.mp4 -qscale 0' %(int(1.0/frame_duration),'%04d',fname))#create video
    
os.chdir('..')#copy video to main directory and delete files
shutil.copyfile('%s/%s.mp4' %(dirname, fname),'%s.mp4' %fname)
shutil.rmtree(dirname)
print 'done'
