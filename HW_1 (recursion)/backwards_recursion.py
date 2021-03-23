'''
Created on 6 Sep 2014

@author: Kieran Finn
'''
import numpy as np
from scipy.integrate import quad

five=np.float32(5)
one=np.float32(1)

One=np.longdouble(1)
Five=np.longdouble(5)

def I_exact(n):
    return quad(lambda x: x**n/(x+5.),0,1)[0]

I_sing=np.zeros(21,dtype=np.float32)
I_doub=np.zeros(21)  
I_quad=np.zeros(21,dtype=np.longdouble)

I_sing[20]=np.float32(0)
I_doub[20]=0.
I_quad[20]=np.longdouble(0)

f=open('backward_recursion.txt','w')

f.write('n\tsingle\t\tdouble\t\tquadruple\texact\n')   
for n in range(20,0,-1):
    I_sing[n-1]=one/(five*np.float32(n))-(one/five)*I_sing[n]
    I_doub[n-1]=1./(5.*float(n))-(1./5.)*I_doub[n]
    I_quad[n-1]=One/(Five*np.longdouble(n))-(One/Five)*I_quad[n]

for i in range(21):
    f.write('%d\t%.6f\t%.6f\t%.6f\t%.6f\n' %(i,I_sing[i],I_doub[i],I_quad[i],I_exact(i)))
    
f.close()
print 'done'