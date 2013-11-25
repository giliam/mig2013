#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created on Thu Nov 21 14:36:29 2013

@author: Croig
"""

import util

import numpy as np
import matplotlib.pyplot as plt


def fft(sig, sig2=[], meth="CT", mid=True, lin=True, freqMax=12000):
    """param sig : signal a traiter
        param sig2=[] : !!! EN CHANTIER !!! : signal secondaire à calculer en parallele
        param meth="CT" : methode de calcul de la FFT
            CT : Cooley-Tukey (classique, par defaut)
        param mid=True : renvoyer la moitie du tableau (parite du spectre)
        param lin=True : methode d'interpolation lineaire
        param freqMax=12000 : frequence maximale representee dans le tableau"""
    N = len(sig)
    M = len(sig2)
    if meth == "CT":
        if sig2==[]:
            C = fftCT(sig,lin)
        else:
            C = fftCT([sig[k] + sig2[k] * 1j for k in range(N)],lin)
    if sig2 == []:
        if mid: return C[len(C)/2:]
        else: return C
    else:
        C1 = [(C[k] + C[N-k].conjugate())/2 for k in range(N)]
        C2 = [(C[k] - C[N-k].conjugate())/(2j) for k in range(N)]
        if mid: return C1[len(C1)/2:],C2[len(C2)/2:]
        else: return C1,C2

def fftCT(sig,lin):
    N = len(sig)
    if util.is2Power(N):
        return fftCTRec(sig)
    else:
        return fftCTRec(util.zPad(sig))

def fftCTRec(sig):
    N = len(sig)
    if N <= 1:
        return sig
    else:
        even = fftCTRec(sig[0::2])
        odd = fftCTRec(sig[1::2])
        return [even[k] + np.exp(-2j * np.pi * k/N) * odd[k] for k in range(N/2)] + \
               [even[k] - np.exp(-2j * np.pi * k/N) * odd[k] for k in range(N/2)]
               

     

