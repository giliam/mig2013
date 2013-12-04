#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from numpy import int16
import scipy.io.wavfile
from operator import add


def sync(amplitudes):
    tOut = 50
    N = len(amplitudes)
    coeff_lissage = 5
    max = 0
    for i in range(N):
        if abs(amplitudes[i]) > max:
            max = abs(amplitudes[i])

    #print("Max is {}".format(max))

    valeurSeuil = 50
    #print("Seuil is {}".format(valeurSeuil))

    maxDiff = 300
    maxRemove = 800
    #print("MaxDiff is {}".format(maxDiff))

    iMin = -1
    iMin2 = -1
    iMax = -1
    iMax2 = -1
    inIt = False
    lastHit = -1

    for i in range(N):
        if iMin == -1 and amplitudes[i] > valeurSeuil:
            iMin = i
            lastHit = i
            inIt = True
        if iMin != -1:
            if i - iMin > maxRemove: # Won't remove more than maxRemove
                break
            elif inIt == True and amplitudes[i] > valeurSeuil:
                lastHit = i
            elif inIt == True and amplitudes[i] < valeurSeuil and i - lastHit >= maxDiff:
                inIt = False
            elif inIt == False and amplitudes[i] > valeurSeuil:
                iMin2 = i
                break

    inIt = False
    lastHit = -1

    for i in range(N-1, -1, -1):
        if iMax == -1 and amplitudes[i] > valeurSeuil:
            iMax = i
            lastHit = i
            inIt = True
        if iMax != -1:
            if iMax - i > maxRemove: # Won't remove more than maxRemove
                break
            elif inIt == True and amplitudes[i] > valeurSeuil:
                lastHit = i
            elif inIt == True and amplitudes[i] < valeurSeuil and lastHit - i >= maxDiff:
                inIt = False
            elif inIt == False and amplitudes[i] > valeurSeuil:
                iMax2 = i
                break

    #print("iMin is {}".format(iMin))
    #print("iMin2 is {}".format(iMin2))
    #print("iMax is {}".format(iMax))
    #print("iMax2 is {}".format(iMax2))
    #print("")

    if iMin2 != -1 and iMin2-iMin > tOut:
        iMin2 -= tOut
    if iMax2 != -1 and iMax-iMax2 > tOut:
        iMax2 += tOut

    if iMin > tOut:
        iMin -= tOut
    if N-1 - iMax > tOut:
        iMax += tOut


    amplitudes_coupe = [0. for i in range(iMax-iMin+1)]
    for i in range(iMax-iMin+1):
        amplitudes_coupe[i] = amplitudes[iMin + i]

    if iMin2 != -1 or iMax2 != - 1:
        if iMin2 == -1:
            iMin2 = iMin
        if iMax2 == -1:
            iMax2 = iMax

        if iMin2 - iMin <= maxRemove and iMax - iMax2 <= maxRemove:
            return amplitudes_coupe
        amplitudes_coupe2 = [0. for i in range(iMax2-iMin2+1)]
        for i in range(iMax2-iMin2+1):
            amplitudes_coupe2[i] = amplitudes[iMin2 + i]

        return sync(amplitudes_coupe2)
    else:
        return amplitudes_coupe
def syncFile(path, name):
    ampli = scipy.io.wavfile.read(path + name)
    ampli2 = sync(ampli[1])
    scipy.io.wavfile.write(path + "sync_" + name, ampli[0], int16(ampli2))
if __name__ == "__main__":
    syncFile("0")
    syncFile("1")
    syncFile("2")
