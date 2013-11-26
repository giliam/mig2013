# -*- coding: utf-8 -*-
""" Constantes globales """

import pyaudio

# pour le recorder:
CHUNK = 1024 # nombre de bits enregistrés par boucle
FORMAT = pyaudio.paInt16
CHANNELS = 1 # On est en mono
RATE = 44100 #Fréquence

# Synchro:
COEFF_LISSAGE = 5 # à déterminer empiriquement
T_MIN = 50 # blanc minimum avant le son
COEFF_COUPE = 0.0000001 # en pourcent

# fenetre hann : 

ecart_fenetre = 0.01301587
temps_fenetre = 0.023219954648526
