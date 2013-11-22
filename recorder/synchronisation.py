# -*- coding: utf-8 -*-
from numpy import zeros
''' coeff_lissage est un entier paramétrant l'intensité du lissage indispensable pour éviter de commencer trop tôt à cause du bruit (à déterminer)
	t_min est l'intervalle de temps de sécurité (à déterminer)
	coeff_coupe est l'intensité de la coupe (à déterminer expérimentalement)
'''
 
def synchro (amplitudes,coeff_lissage,t_min,coeff_coupe):
	N=len(amplitude_max)
	N_lissage = (int(N/coeff_lissage))
	amplitude_lisse = zeros(N_lissage)
	i = 0
	while i < N_lissage:
		amplitude_lisse[i] = reduce(add,[amplitudes[i*coeff_lissage+j] for j in range(coeff_lissage)],0)/coeff_lissage
		i += 1
	valeur_seuil = coeff_coupe*(max(amplitude_lisse)-min(amplitude_lisse))/2
	
	i_min = 0
	i_max = 0
	i = 0
	while i < N_lissage:
		if amplitude_lisse[i] > valeur_seuil and i-t_min*RATE/coeff_lissage >= 0:
			i_min = i-t_min*RATE/coeff_lissage
		elif  amplitude_lisse[i] > valeur_seuil and i-t_min*RATE/coeff_lissage < 0:
			print "L'enregistrement a commence trop tard"
			return ""
	i = N_lissage-1
	while i > -1:
		if amplitude_lisse[i] > valeur_seuil and i+t_min*RATE/coeff_lissage < N_lissage:
			i_max = i+t_min*RATE/coeff_lissage
		elif  amplitude_lisse[i] > valeur_seuil and i+t_min*RATE/coeff_lissage > N_lissage:
			print "L'enregistrement a fini trop tot"
			return ""
			
	amplitudes_coupe = zeros(i_max-i_min)
	for i in range((i_max*-i_min)*coeff_lissage):
		amplitudes_coupe[i] = amplitudes[i+i_min*coeff_lissage]
		
	return amplitudes_coupe