import numpy as np
import scipy.io.wavfile
import math as m
from numpy import int8

def quantification(fileName):
    ampli = scipy.io.wavfile.read( "db/waves/" + fileName )
    freq = ampli[0]
    ampli = ampli[1]
    N=len(ampli)
    ampMax = -1
    ampMin = 1
    newAmp = np.zeros(N)
    
    for i in range(N):
        if ampMax < ampli[i]:
            ampMax = ampli[i]
        if ampMin > ampli[i]:
            ampMin = ampli[i]
    ampAbs = 2* (ampMax + m.fabs(ampMin))
    print ampAbs
    
    for i in range(N):
        if ampli[i] > 0:
            newAmp[i] = ampli[i] * 255 / ampAbs
        else:
            newAmp[i] = ampli[i] * 255 / ampAbs
            
    scipy.io.wavfile.write( "db/waves/mod/" + fileName , freq, int8(newAmp))


