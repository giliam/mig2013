#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import random as rnd
import math
from constantes import *  

def hann_window_bis  (signal):
	k = 0
	l = len(signal)
	j = 0
	liste = []
	while (k <l/(ecart_fenetre*RATE) and j<((2*l)-(ecart_fenetre*RATE))):
		L = []
		for i in range(int(temps_fenetre*RATE)+1):
			L.append(signal[k*int(ecart_fenetre*RATE)+i]* \
            0.5 * (1 - np.cos(2 * (np.pi) * (float(i) / (RATE * temps_fenetre)))))
			j += 1
		liste.append(L)
		k += 1
	return liste
		
def hann_window(signal):
	l = len(signal)
	k = 0
	liste = []
	while (k < l / (ecart_fenetre * RATE)):
		L = []
		for i in range(int(temps_fenetre * RATE) + 1):
			try:
				L.append(signal[k * int(ecart_fenetre * RATE) + i] * 0.5 \
                *(1 - np.cos(2 * np.pi * float(i) / (RATE * temps_fenetre))))
			except IndexError:
				break 
		liste.append(L)
		k+=1
	return liste	

if __name__ == "__main__":
    #test de verification 	
	z = [250.*i/100000 for i in range (88200)]
	
	print(len(hann_window(z)[15]))
