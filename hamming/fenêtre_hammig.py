import numpy as np
freq = 44100
ecart_fenetre = 0.015
temps_fenetre = 0.030

def hamming_window (signal):
	k =0
	l =len(signal)
	j =0
	
	while (k <l/(ecart_fenetre*freq) and j<((2*l)-(ecart_fenetre*0.015)):
		for i in range(temps_fenetre*freq):
			signal[k+i]*=(0.5-0.46*np.cos(2*np.pi*(i/(freq))/temps_fenetre))
			j += 1
			if (j == L):
				break
		k+=1
		
		
def hamming_window(bis (signal):
	k =0

	
	while (k <l/(ecart_fenetre*freq)):
		for i in range(temps_fenetre*freq):
			try:
				signal[k+i]*=(0.5-0.46*np.cos(2*np.pi*(i/(freq))/temps_fenetre))
			else: 
				break
		k+=1
		
				