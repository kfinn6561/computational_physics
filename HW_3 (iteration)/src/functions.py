'''
Created on 23 Sep 2014

@author: Kieran Finn
'''

def getfloat(message,Range=False):
    ''''a subroutine for allowing the user to choose a value for a parameter.
    Includes error handling to ensure what is entered is a float and allows an allowed range to be specified'''
    while True:
        out=raw_input(message+': ')
        try:
            out=float(out)
            if not Range:
                return out
            else:
                if out>=Range[0] and out<=Range[1]:
                    return out
                else:
                    print 'ERROR: value not in range'
        except ValueError:
            print 'ERROR: not a valid number'

def iterate(f,x,iterations,verbose=0):
    '''verbose has 6 levels: 0-1, do not print, 2-3, print, 4-5, print and stop after each iteration.
    Even (0,2,4) return just the answer, odd return all iterations in a list'''
    verbose=int(verbose)
    output=(verbose%2==1)#true for even, false for odd
    printing=(verbose>=2)#true if printing is required
    stopping=(verbose>=4)#true if stopping is required
    
    iterations=int(iterations)
    
    if output:
        out=[x]
    for i in range(iterations):
        if printing:
            print i,x
        x=f(x)
        if output:
            out.append(x)
        if stopping:
            raw_input('>')
    
    if printing:
        print iterations,x    
    if output:
        return out
    else:
        return x