#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 16:55:24 2013

@author: MIG
"""

import math
import numpy as np
from fractions import gcd


def is2Power(N):
    return N == np.power(2, int(math.log(N, 2)))
    
def get2Power(N):
    return int(np.power(2, int(math.log(N, 2)) + 1))
    
def zPad(sig):
    N = len(sig)
    return sig + [0 for i in range(get2Power(N) - N)]
    
def reduc(M,N):
    d = gcd(M, N)
    return M/d, N/d
    
def pgcd(a,b):
    # une fonction fractions.gcd(a, b) est déjà implémentée dans Python
    return gcd(a, b)
