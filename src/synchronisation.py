# -*- coding: utf-8 -*-

from numpy import zeros
import scipy.io.wavfile
from constantes import *
from operator import add

""" coeff_lissage est un entier paramétrant l'intensité du lissage indispensable pour éviter de commencer trop tôt à cause du bruit (à déterminer)
    t_min est l'intervalle de temps de sécurité (à déterminer)
    coeff_coupe est l'intensité de la coupe (à déterminer expérimentalement)
"""
 
def synchro(amplitudes,coeff_lissage,t_min,coeff_coupe):
    N=len(amplitudes)
    N_lissage = (int(N/coeff_lissage))
    amplitude_lisse = zeros(N_lissage)
    maxi = 0
    mini = 0
    COEFF = t_min*RATE/coeff_lissage/1000
    for i in range(N_lissage):
        amplitude_lisse[i] = reduce(add, [amplitudes[i * coeff_lissage + j] for j in range(coeff_lissage)], 0)/coeff_lissage
        if(i == 0):
            maxi = amplitude_lisse[i]
            mini = maxi
        elif(abs(amplitude_lisse[i]) > abs(maxi)):
            maxi = amplitude_lisse[i]
        elif(abs(amplitude_lisse[i]) < abs(mini)):
            mini = amplitude_lisse[i]
        
    valeur_seuil = coeff_coupe*(abs(maxi)-abs(mini))
    
    i_min = 0
    i_max = N_lissage - 1
    Depasse = False
    i_dernierHaut = 0
    for i in range(N_lissage):
        if(abs(amplitude_lisse[i]) > valeur_seuil):
            i_dernierHaut = i
        if(not Depasse):
            if(abs(amplitude_lisse[i]) > valeur_seuil):
                Depasse = True
                i_min = i
        else:
            if(abs(amplitude_lisse[i]) < valeur_seuil and (i - i_dernierHaut) > COEFF):
                i_max = i
                break
        
    """for i in range(N_lissage):
        if amplitude_lisse[i] > valeur_seuil and i-t_min*RATE/coeff_lissage/1000 >= 0:
            i_min = i
        elif amplitude_lisse[i] > valeur_seuil and i-t_min*RATE/coeff_lissage/1000 < 0:
            print "L'enregistrement a commence trop tard"
            # return ""
            
    for i in range(N_lissage-1, -1, -1):
        if amplitude_lisse[i] > valeur_seuil and i+t_min*RATE/coeff_lissage/1000 < N_lissage:
            i_max = i
        elif amplitude_lisse[i] > valeur_seuil and i+t_min*RATE/coeff_lissage/1000 > N_lissage:
            print "L'enregistrement a fini trop tot"
            # return """

    if(i_min < COEFF):
        print "L'enregistrement a commence trop tard"
    if(i_max > N_lissage - COEFF):
        print "L'enregistrement a fini trop tot"

    print i_min
    print i_max
    print N

    taille = (i_max-i_min)*coeff_lissage
    print "taille = ", taille
    amplitudes_coupe = zeros(taille)
    for i in range(taille):
        amplitudes_coupe[i] = amplitudes[i+i_min*coeff_lissage]
        
    return amplitudes_coupe
    
ampli = scipy.io.wavfile.read("0.wav")
ampli2 = synchro(ampli[1],COEFF_LISSAGE,T_MIN,COEFF_COUPE)
print "taille2", len(ampli2)
print ampli[1]
print ampli2
print ampli[0]
scipy.io.wavfile.write("0e.wav", ampli[0], ampli2)
