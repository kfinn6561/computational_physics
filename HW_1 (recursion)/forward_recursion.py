'''
Created on 5 Sep 2014

@author: Kieran Finn
'''
import numpy as np
from scipy.integrate import quad

five=np.float32(5)

def I_exact(n):
    return quad(lambda x: x**n/(x+5.),0,1)[0]

I_sing=np.zeros(31,dtype=np.float32)
I_doub=np.zeros(31)  
I_quad=np.zeros(31,dtype=np.longdouble)

I_sing[0]=np.log(np.float32(6)/five)
I_doub[0]=np.log(6./5.)
I_quad[0]=np.log(np.longdouble(6)/np.longdouble(5))

f=open('forward_recursion.txt','w')

f.write('n\tsingle\t\tdouble\t\tquadruple\texact\n')   
for i in range(30):
    f.write('%d\t%.6e\t%.6e\t%.6e\t%.6e\n' %(i,I_sing[i],I_doub[i],I_quad[i],I_exact(i)))
    I_sing[i+1]=np.float32(1)/np.float32(i+1)-five*I_sing[i]
    I_doub[i+1]=1./float(i+1)-5.*I_doub[i]
    I_quad[i+1]=np.longdouble(1)/np.longdouble(i+1)-np.longdouble(5)*I_quad[i]
    
f.write('%d\t%.6e\t%.6e\t%.6e\t%.6e' %(30,I_sing[30],I_doub[30],I_quad[30],I_exact(30)))
f.close()
print 'done'
