
'''
Created on 14 Jan 2013

@author: Kieran Finn
'''
import sys
import time
from tempfile import mkdtemp
import os.path as path
import pickle
import shelve
import shutil
from copy import copy
        
class pickle_defaultdict(): #rewriting ofcollections.defaultdict in such a way that can be pickled
    def __init__(self,default):
        self.default=default
        self.d={}
        
    def __getitem__(self,key):
        if not self.d.has_key(key):
            self.d[key]=copy(self.default)
        return self.d[key]
    
    def __len__(self):
        return len(self.d)
    
    def __setitem__(self,i,j):
        self.d[i]=j
    
    def keys(self):
        return self.d.keys()
            
def set_item(d,i,j,item):
    temp=d[i]
    temp[j]=item
    d[i]=temp

def overprint(s):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(s)

def pload(fname):
    f=open(fname,'rb')
    try:
        out=pickle.load(f)
    except:
        f.close()
        f=open(fname,'r')
        out=pickle.load(f)
    f.close()
    return out

def pdump(obj,fname):
    f=open(fname,'wb')
    pickle.dump(obj,f)
    f.close()
    
def add_comma(number): #makes a large number more readable by adding a comma every three digits
    out=''
    i=1
    number=str(number)
    while i<=len(number):
        out=number[-i]+out
        if i%3==0 and i!=len(number):
            out=','+out
        i+=1
    return out

def date_string():
    s=time.ctime()
    wday,month,day,t,year=s.split()
    t=t.split(':')
    t=t[0]+'_'+t[1]
    return day+'_'+month+'_'+year+'_'+t

def hms(time): #converts a number in seconds into a string of the form HH:MM:SS
    hours=int(time/3600)
    time-=hours*3600
    minutes=int(time/60)
    seconds=int(time-minutes*60)
    out= '%d:%02d:%02d' %(hours,minutes,seconds)
    return out

def old_progress_bar(current,total):#doesn't display any numbers
    screen_length=80.0
    n=int(screen_length*float(current)/total)
    overprint('#'*n)
    

def progress_bar(current,total):
    screen_length=80.0
    middle=int(screen_length/2)
    timestr=' %s/%s ' %(add_comma(current+1),add_comma(total))
    timelen=len(timestr)
    start=middle-timelen/2
    end=start+timelen
    n=int(screen_length*float(current)/total)
    if n<=start:
        out='#'*n+' '*(start-n)+timestr
    elif n<=end:
        out='#'*start+timestr
    else:
        out='#'*start+timestr+'#'*(n-end)
    overprint(out)

     
