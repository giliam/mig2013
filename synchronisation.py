# -*- coding: utf-8 -*-
from numpy import zeros
'''coeff_lissage est un entier paramétrant l'intensité du lissage indispensable pour éviter de commencer trop tôt à cause du bruit
   '''
 
def synchro (amplitudes,coeff_lissage,t_min):
	N=len(amplitude_max)
	N_lissage = (int(N/coeff_lissage))
	amplitude_lisse = zeros(N_lissage)
	i = 0
	while i < N_lissage:
		amplitude_lisse[i] = reduce(add,[amplitudes[i*coeff_lissage+j] for j in range(coeff_lissage)],0)/coeff_lissage
		i += 1
	valeur_seuil = (max(amplitude_lisse)-min(amplitude_lisse))/2
	
	i_min = 0
	i_max = 0
	i = 0
	while i < N_lissage:
		if amplitude_lisse[i] > valeur_seuil and i-t_min*Fe/coeff_lissage >= 0
			i_min = i-i-t_min*Fe/coeff_lissage
		else if  amplitude_lisse[i] > valeur_seuil and i-t_min*Fe/coeff_lissage < 0
			print "L'enregistrement a commencé trop tard"
			return ""
	
	while i < N_lissage:
		if amplitude_lisse[i] > valeur_seuil and i-t_min*Fe/coeff_lissage >= 0
			i_min = i-i-t_min*Fe/coeff_lissage
		else if  amplitude_lisse[i] > valeur_seuil and i-t_min*Fe/coeff_lissage < 0
			print "L'enregistrement a commencé trop tard"
			return ""
		
	amplitudes_coupe = zeros(i_max-i_min)
	for i in range(i_max-i_min):
		amplitudes_coupe[i] = amplitudes[i+i_min]
		
	if i_min/Fe < t_min or (N-i_max)/Fe < t_min
		
	
	return amplitudes_coupe
		
