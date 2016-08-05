#!/usr/bin/env python
#updates: class implementation, common function
#Program designed by Adrian Wong
import sys, time


def timeCal(arg):  #time calculation
    cdef long end_time = time.time()
    cdef float timeElapse = end_time - arg
    return timeElapse

def signedInt(arg):
    #MOD(NUM+2^15,2^16)-2^15
    cdef int num = ((<int> arg + 2 ** 15) % (2 ** 16)) - 2 ** 15
    #signedInt = str(signedInt)
    return num

def shiftTemp(arg):
    cdef int num = int(arg)
    cdef float temp = num * (10 ** -1)
    #temp = str(temp)
    return <char> temp

def shiftCurrent(arg):
    #MOD(NUM+2^15,2^16)-2^15
    cdef int num = int(arg)
    cdef int n = (((num + 2 ** 15) % (2 ** 16)) - 2 ** 15) * (10 ** -1)
    #signedInt = str(signedInt)
    return n

def keyScan(mode,passTime,button,pressKey,key):
    cdef int b = <int> button
    cdef int m = <int> mode
    cdef int t = <int> passTime
    if mode == 1:
        if b == 0 and t > 10: #set passTime to large number to bypass time check
            #do something
            return True
    elif mode == 2:
        if pressKey == key:
            return True
    else:
        return False