'''
Created on 4 Dec 2014

@author: Kieran Finn
'''
import pylab as p
from functions import pload,progress_bar
import os
import shutil
import sys

fname='metropolis_16_0.1_cold'
dirname=fname
skip=10#don't want to plot every frame

if os.path.exists(dirname):
    if raw_input('this directory already exists, do you want to delete it and start again? ') in ['yes','Yes','y','Y','1']:
        shutil.rmtree(dirname)
    else:
        sys.exit()
os.mkdir(dirname)

energies,magnetisations,spins0,changes,meta_data=pload(fname+'.dat')
iterations=meta_data[3]

iterations=20000#comment this out for full video but would take too long

frame=0
spins=spins0
for i in range(0,iterations):
    if i%skip==0:
        progress_bar(i,iterations)
        p.clf()
        p.imshow(spins,interpolation='none',vmin=-1,vmax=1)
        p.title('t=%d'%i)
        p.savefig(dirname+'/%04d.jpg'%frame)
        frame+=1
    if changes[i]:
        x,y=changes[i]
        spins[x,y]*=-1
p.clf()
p.imshow(spins,interpolation='none',vmin=-1,vmax=1)
p.title('t=%d'%i)
p.savefig(dirname+'/%04d.jpg'%frame)     
frame_duration=0.01
os.chdir(dirname)
os.system('ffmpeg -r %d -i %s.jpg -vcodec libx264 -y %s.mp4 -qscale 0' %(int(1.0/frame_duration),'%04d',fname))#create video
    
os.chdir('..')#copy video to main directory and delete files
shutil.copyfile('%s/%s.mp4' %(dirname, fname),'%s.mp4' %fname)
shutil.rmtree(dirname)

print 'done'
    
    