'''
Created on 19 Sep 2014

asks user for values of a and x0 and iterates the function f(x)=ax(1-x) a given number of times, producing a plot and
a txt output. There is an option to suppress some iterations to remove transience.

@author: Kieran Finn
'''
import pylab as p
from functions import *


default_iterations=100


a=getfloat('choose a value for a')
x0=getfloat('choose a value for x0',[0,1])

fname='a=%g_x0=%g' %(a,x0)
outfile=open(fname+'.txt','w')

f= lambda x: a*x*(1.-x)

suppressed_iterations=int(getfloat('How many iterations to remove transience'))


iterations=getfloat('how many iterations should be plotted? (enter 0 for default of %d)' %default_iterations)
if int(iterations)==0:
    iterations=default_iterations

x=iterate(f,x0,suppressed_iterations)#remove transience
toplot=iterate(f,x,iterations,verbose=1)#iterate to get plotted variables

#output
outfile.write('Output for logistic map f(x)=ax(1-x) with a=%g and x0=%g\n' %(a,x0))
if suppressed_iterations !=0:
    outfile.write('Supressing the first %d iterations\n' %suppressed_iterations)
outfile.write('\n\niteration\tvalue\n')
for i in range(len(toplot)):
    outfile.write('%d\t\t%f\n' %(i+suppressed_iterations,toplot[i]))
outfile.close()

#plotting
p.plot(toplot)
p.title(fname)
p.xlabel('iteration')
p.ylabel('value')
p.savefig(fname+'.png')
p.show()

print 'done'
