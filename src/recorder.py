# -*- coding: utf-8 -*-

""" Réalise l'enregistrement d'un certain nombre d'échantillons audio déterminé par l'utilisateur.
		Nécessite PYAUDIO pour fonctionner : http://www.lfd.uci.edu/~gohlke/pythonlibs/ """
		
import os
import pyaudio
import wave
from constantes import *

def recorder(db):
	""" Procède à l'enregistrement """ 

	nb_mots = raw_input("Combien d'enregistrement par mots ? ")
	nb_mots = int(nb_mots)

	while True:
		mot = raw_input("Entrez le mot a enregistrer : ")
		temps = raw_input("Entrez le nombre de secondes pour l'enregistrement : ")
		temps = float(temps)
		for i in range(nb_mots):
			raw_input("Appuyez sur une touche pour commencer l'enregistrement : ")
			p = pyaudio.PyAudio()

			stream = p.open(format=FORMAT,
							channels=CHANNELS,
							rate=RATE,
							input=True,
							frames_per_buffer=CHUNK)

			print "Enregistrement[", i, "]:"

			frames = []

			for j in range(0, int(RATE / CHUNK * temps)): 
				data = stream.read(CHUNK)
				frames.append(data)
			
			print "Fin - Enregistrement[", i, "]:"

			stream.stop_stream()
			stream.close()
			p.terminate()
			name = mot + "/" + str(i) + ".wav"
			db.addWave(name,CHANNELS,p.get_sample_size(FORMAT),RATE,frames,p)
			
			print "Fin du mot ", i
