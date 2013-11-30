import numpy as np
import math

FE = 44100 #frequence d'echantillonage

def mel(f):
    return 2595*math.log(1+f/700.)/math.log(10)

def triangularFilter(tab,FE):
	pasOutput = mel(FE/2.)/12.
	pasFFT = FE/(2.*len(tab))
	outputTab = [0 for i in range(24)]
	for n in range(24):
		debut = n/2 * pasOutput + (n%2)*pasOutput/2.
		fin = n/2*pasOutput + (n%2)*pasOutput/2.+pasOutput
		for k in range(len(tab)):
			f = k*pasFFT
			if(mel(f) > debut and mel(f)<fin):
				outputTab[n] += abs(tab[k])
			else:
				break
	for n in range(24):
		outputTab[n] = math.log(outputTab[n])
	return outputTab

