
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 14:36:29 2013

@author: Croig
"""

import util

import numpy as np
import matplotlib.pyplot as plt

""" Utiliser "fftListes" et lui envoyer la liste des echantillons. """

def fftListe(echs):
    n = len(echs)
    rep = [[] for k in range(n)]
    if n%2 == 1:
        for k in range(n/2):
            print "Echantillons ",2*k," et ",2*k+1," en cours..."
            rep[2*k],rep[2*k+1] = fft(echs[2*k],echs[2*k+1])
            
    else:
        for k in range(n/2-1):
            print "Echantillons ",2*k," et ",2*k+1," en cours..."
            rep[2*k],rep[2*k+1] = fft(echs[2*k],echs[2*k+1])
        rep[n-1] = fft(echs[n-2])
    rep[n-1] = fft(echs[n-1])

def fft(sig, sig2=[], mid=True, lin=True, freqMax=12000):
    """param sig : signal a traiter
param sig2=[] : signal secondaire à calculer en parallele. Donne un
                tuple avec les deux spectres.
param mid=True : renvoyer la moitie du tableau (parite du spectre)
param lin=True : methode d'interpolation lineaire
param freqMax=12000 : frequence maximale representee dans le tableau"""
    N = len(sig)
    M = len(sig2)
    if (M==0 or (M!=0 and M==N)):
        if sig2==[]:
            C = fftCT(sig,lin)
            if mid:
                return C[len(C)/2:]
            else:
                return C
        else:
            C = fftCT([sig[k]+sig2[k]*1j for k in range(N)],lin)
            C1 = [(C[k]+C[N-k].conjugate())/2 for k in range(1,N)]
            C2 = [(C[k]-C[N-k].conjugate())/(2j) for k in range(1,N)]
            if mid: return C1[len(C1)/2:],C2[len(C2)/2:]
            else: return C1,C2
    else:
        print "Deux echantillons de meme taille needed !"
        return [],[]

def fftCT(sig,lin):
    N = len(sig)
    if util.is2Power(N):
        return fftCTRec(sig)
    else:
        print "zPad needed"
        return fftCTRec(util.zPad(sig))

def fftCTRec(sig):
    N = len(sig)
    if N <= 1:
        return sig
    else:
        even = fftCTRec(sig[0::2])
        odd = fftCTRec(sig[1::2])
        return [even[k] + np.exp(-2j*np.pi*k/N)*odd[k] for k in range(N/2)] + \
               [even[k] - np.exp(-2j*np.pi*k/N)*odd[k] for k in range(N/2)]

               
freq1,freq2 = 220,440
freqEch = 44100
s1 = [np.sin(2*np.pi*freq1*t/freqEch) for t in range(1024)]
s2 = [np.sin(2*np.pi*freq2*t/freqEch) for t in range(1024)]
C1,C2 = fft(s1,s2)
plt.plot([abs(C1[k]) for k in range(len(C1))])
