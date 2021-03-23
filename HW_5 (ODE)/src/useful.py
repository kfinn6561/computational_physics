
'''
Created on 14 Jan 2013

@author: Kieran Finn
'''
import sys
import pickle


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
                if type(Range)==tuple:#open interval
                    if out>Range[0] and out<Range[1]:
                        return out
                else:#closed interval
                    if out>=Range[0] and out<=Range[1]:
                        return out
                print 'ERROR: value not in range'
        except ValueError:
            print 'ERROR: not a valid number'

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
'''
def progress_bar(current,total):
    screen_length=80.0
    n=int(screen_length*float(current)/total)
    overprint('#'*n)
    
'''
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