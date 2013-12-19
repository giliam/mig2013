#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from numpy import zeros
from numpy import int16
import scipy.io.wavfile
from core.utils.constantes import *
from operator import add
import math as m

""" coeff_lissage est un entier parametrant l'intensite du lissage indispensable pour eviter de commencer trop tôt a cause du bruit (a determiner)
    t_min est l'intervalle de temps de securite (a determiner)
    coeff_coupe est l'intensite de la coupe (a determiner experimentalement)
"""
 
def synchro(amplitudes,coeff_lissage,t_min,coeff_coupe):
    N = len(amplitudes)
    N_lissage = int(N / coeff_lissage)
    amplitude_lisse = zeros(N_lissage)
    maxi = 0
    mini = 0
    COEFF = t_min * RATE / coeff_lissage / 1000
    for i in range(N_lissage):
        amplitude_lisse[i] = reduce(add, [m.exp(abs(amplitudes[i * coeff_lissage + j]/100)) for j in range(coeff_lissage)], 0) / coeff_lissage
        if(i == 0):
            maxi = amplitude_lisse[i]
            mini = maxi
        elif(amplitude_lisse[i] > maxi):
            maxi = amplitude_lisse[i]
        elif(amplitude_lisse[i] < mini):
            mini = amplitude_lisse[i]

    print "maxi", maxi
    print "mini", mini
        
    valeur_seuil = coeff_coupe * (maxi - mini)
    print "valeur_seuil", valeur_seuil

    compt = 0
    for i in range(N_lissage):
        if(amplitude_lisse[i] > valeur_seuil):
            compt += 1

    print "compt ", compt * coeff_lissage
    
    i_min = 0
    i_max = N_lissage - 1
    i_minTrouve = False
    i_maxTrouve = False
    
    for i in range(N_lissage):
        if((not i_minTrouve) and amplitude_lisse[i] > valeur_seuil):
            i_minTrouve = True
            i_min = i
            print "i_min", i_min
        if((not i_maxTrouve) and amplitude_lisse[N_lissage - i - 1] > valeur_seuil):
            i_max = N_lissage - i - 1
            i_maxTrouve = True
            print "i_max", i_max
        if(i_minTrouve and i_maxTrouve):
            print "fin pour i = ", i
            break
    
    if(i_min < COEFF):
        print "L'enregistrement a commence trop tard"
    if(i_max > N_lissage - COEFF):
        print "L'enregistrement a fini trop tot"

    print i_min * coeff_lissage
    print i_max * coeff_lissage
    print N

    taille = (i_max - i_min) * coeff_lissage
    print "taille = ", taille
    amplitudes_coupe = zeros(taille)
    for i in range(taille):
        amplitudes_coupe[i] = amplitudes[i + i_min * coeff_lissage]
        
    return amplitudes_coupe

if __name__ == '__main__':    
    ampli = scipy.io.wavfile.read("0.wav")
    ampli2 = synchro(ampli[1], COEFF_LISSAGE, T_MIN, COEFF_COUPE)
    scipy.io.wavfile.write("0e.wav", ampli[0], int16(ampli2))
