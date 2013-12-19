# -*- coding: utf-8 -*-
""" Constantes globales """

import pyaudio

# pour le recorder:
CHUNK = 1024 # nombre de bits enregistres par boucle
FORMAT = pyaudio.paInt16
CHANNELS = 1 # On est en mono
RATE = 44100 #Frequence

# Synchro:
COEFF_LISSAGE = 5 # a determiner empiriquement
T_MIN = 50 # blanc minimum avant le son
COEFF_COUPE = 0.0000001 # en pourcent

# fenetre hann : 

ecart_fenetre = 0.01301587
temps_fenetre = 0.023219954648526

#Creation MFCC

TAILLE_FINALE_MFCC = 13

NB_ITERATIONS = 10
