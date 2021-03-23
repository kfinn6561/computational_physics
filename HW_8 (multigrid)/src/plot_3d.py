'''
Created on 11 Nov 2014

@author: Kieran Finn
'''
from functions import pload,progress_bar
import numpy as np
import pylab as p
from mpl_toolkits.mplot3d import axes3d#used for 3d plotting
import os
import shutil
import sys


fname='multigrid_data'
datname=fname+'.dat'
dirname='multigrid_3d'


X,Y,phi_exact,data=pload(datname)#read data from file
N,_=phi_exact.shape
thin=1
if N>100:
    thin=2
if N>500:
    thin=10
if N>1000:
    thin=20



try:
    d=np.append(np.array(data).flatten(),phi_exact.flatten())#all values of phi, used to set the min and max values for the plots
except:
    d=phi_exact.flatten()
min_z=min(d)
max_z=max(d)
min_z-=0.1*np.abs(min_z)
max_z+=0.1*np.abs(max_z)#leaves a bit of padding space

frame=0

if os.path.exists(dirname):
    if raw_input('this directory already exists, do you want to delete it and start again? ') in ['yes','Yes','y','Y','1']:
        shutil.rmtree(dirname)
    else:
        sys.exit()
os.mkdir(dirname)


def plot(phi):
    global frame
    fig=p.figure()
    ax=fig.add_subplot(111,projection='3d')
    ax.plot_wireframe(X[::thin,::thin],Y[::thin,::thin],phi[::thin,::thin],color='blue')
    #ax.plot_wireframe(X[::thin,::thin],Y[::thin,::thin],phi_exact[::thin,::thin],color='green')
    p.title('iteration %03d' %frame)
    ax.set_xlim((X[(0,0)],X[(-1,-1)]))
    ax.set_ylim((Y[(0,0)],Y[(-1,-1)]))
    ax.set_zlim((min_z,max_z))
    p.savefig(dirname+'/%04d.jpg' %frame)
    p.close()
    frame+=1
 
N=len(data)    
for i in range(N):
    progress_bar(i,N)
    plot(data[i])
    
frame_duration=0.3
os.chdir(dirname)
os.system('ffmpeg -r %d -i %s.jpg -vcodec libx264 -y %s.mp4 -qscale 0' %(int(1.0/frame_duration),'%04d',fname))#create video
    
os.chdir('..')#copy video to main directory and delete files
shutil.copyfile('%s/%s.mp4' %(dirname, fname),'%s.mp4' %fname)
shutil.rmtree(dirname)

print 'done'