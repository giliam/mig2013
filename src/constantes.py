# -*- coding: utf-8 -*-
""" Constantes globales """

import pyaudio

# pour le recorder:
CHUNK = 1024 # nombre de bits enregistrés par boucle
FORMAT = pyaudio.paInt16
CHANNELS = 1 # On est en mono
RATE = 44100 #Fréquence

# Synchro:
COEFF_LISSAGE = 3 # à déterminer empiriquement
T_MIN = 50 # blanc minimum avant le son
COEFF_COUPE = 0.25 # en pourcent