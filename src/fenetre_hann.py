import numpy as np
import random as rnd
import math
from constantes import *  

def hann_window_bis  (signal):
	k =0
	l =len(signal)
	j =0
	while (k <l/(ecart_fenetre*RATE) and j<((2*l)-(ecart_fenetre*RATE))):
		for i in range(int(temps_fenetre*RATE)):
			signal[k*int(ecart_fenetre*RATE)+i]*= 0.5-0.5*np.cos(2*(np.pi)*(float(i)/(RATE*temps_fenetre)))
			j += 1
			if (j == l):
				break
		k+=1
	return signal		
		
def hann_window(signal):
	l =len(signal)
	k =0
	while (k <l/(ecart_fenetre*RATE)):
		for i in range(int(temps_fenetre*RATE)):
			try:
				signal[k*int(ecart_fenetre*RATE)+i]*= 0.5-0.5*np.cos(2*(np.pi)*(float(i)/(RATE*temps_fenetre)))
			except IndexError:
				break 
		k+=1
	return signal			

if __name__ == "__main__":
#test de verification 	
	z = [250*i/100000 for i in range (88200)]
	
	print(hann_window(z)==hann_window_bis(z))
