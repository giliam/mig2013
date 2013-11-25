# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 16:55:24 2013

@author: MIG
"""

import math
import numpy as np

def is2Power(N):
    return N == np.power(2,int(math.log(N,2)))
def get2Power(N):
    return int(np.power(2,int(math.log(N,2))+1))
def zPad(sig):
    N = len(sig)
    return sig + [0 for i in range(get2Power(N)-N)]
def reduc(M,N):
    d = pgcd(M,N)
    return M/d,N/d
def pgcd(a,b):
    r = a%b
    if r==0: return b
    else: return pgcd(b,r)
