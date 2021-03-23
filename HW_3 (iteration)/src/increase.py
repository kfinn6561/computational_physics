'''
Created on 23 Sep 2014

increases the value of a between two given values, creating a movie which will allow for the spotting of bifurcations

@author: Kieran Finn
'''
from functions import *
import pylab as p
import numpy as np
import os
import sys
import shutil

default_iterations=100
frame_duration=0.3

a=0. #need to initiate a
f= lambda x: a*x*(1.-x) #this will update when I change a

a0=getfloat('Starting a value')
a1=getfloat('Finishing a value', Range=[a0,np.inf])
da=getfloat('Step in a',Range=[0,a1-a0])

dirname='%g_%g_%g' %(a0,a1,da)

if os.path.exists(dirname):
    if raw_input('this directory already exists, do you want to delete it and start again? ') in ['yes','Yes','y','Y','1']:
        shutil.rmtree(dirname)
    else:
        sys.exit()
os.mkdir(dirname)

x0=getfloat('Choose a value for x0',Range=[0,1])

suppressed_iterations=int(getfloat('How many iterations to remove transience'))

iterations=getfloat('how many iterations should be plotted? (enter 0 for default of %d)' %default_iterations)
if int(iterations)==0:
    iterations=default_iterations

a=a0
i=0

while True:
    print 'a=%g' %a
    x=iterate(f,x0,suppressed_iterations)#remove transience
    toplot=iterate(f,x,iterations,verbose=1)#iterate to get plotted variables
    p.clf()
    p.plot(toplot)
    p.title('a=%g' %a)
    p.xlabel('iteration')
    p.ylabel('value')
    p.xlim([0,len(toplot)-1])
    p.ylim([0,1])
    p.savefig(dirname+'/%04d.jpg' %i)
    if a>=a1:
        break
    i+=1
    a+=da
    
os.chdir(dirname)
os.system('ffmpeg -r %d -i %s.jpg -vcodec libx264 -y %s.mp4 -qscale 0' %(int(1.0/frame_duration),'%04d',dirname))#create video
    
os.chdir('..')#copy video to main directory and delete files
shutil.copyfile('%s/%s.mp4' %(dirname, dirname),'%s.mp4' %dirname)
shutil.rmtree(dirname)

    
print 'done'
    
    
