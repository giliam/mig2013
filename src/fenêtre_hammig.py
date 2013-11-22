import numpy as np
import random as rnd
import math
freq = 44100
ecart_fenetre = 1./441.
temps_fenetre = 0.030

def hamming_window (signal):
	k =0
	l =len(signal)
	j =0
	while (k <l/(ecart_fenetre*freq) and j<((2*l)-(ecart_fenetre*freq))):
		for i in range(int(temps_fenetre*freq)):
			signal[k*int(ecart_fenetre*freq)+i]*=(0.5-0.5*np.cos(2*np.pi*(i/(freq))/temps_fenetre))
			j += 1
			if (j == l):
				break
		k+=1
	return signal		
		
def hamming_window_bis (signal):
	l =len(signal)
	k =0
	while (k <l/(ecart_fenetre*freq)):
		for i in range(int(temps_fenetre*freq)):
			try:
				signal[k*int(ecart_fenetre*freq)+i]*=(0.5-0.5*np.cos(2*np.pi*(i/(freq))/temps_fenetre))
			except IndexError:
				break 
		k+=1
		
	return signal			
	
z = []
for i in range(88200): 
	z.append(250*i/100000)
	
print(hamming_window(z) == hamming_window_bis(z))
