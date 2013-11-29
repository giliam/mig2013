#!/usr/bin/env python2
# -*- coding: utf-8 -*-

""" Réalise l'enregistrement d'un certain nombre d'échantillons audio déterminé par l'utilisateur.
		Nécessite PYAUDIO pour fonctionner : http://www.lfd.uci.edu/~gohlke/pythonlibs/ """
		
import os
import pyaudio
import wave
from constantes import *
import random
import hashlib


def recorder(db,dirName="",nbRecording=-1,askForWord=True):
	""" Procède à l'enregistrement """ 

	if nbRecording < 0:
		nbRecording = raw_input("Combien d'enregistrement par mots ? ")
		nbRecording = int(nbRecording)
	n = ""
	while True:
		if askForWord:
			mot = raw_input("Entrez le mot a enregistrer : ")
		else:
			mot = ""
			
		temps = raw_input("Entrez le nombre de secondes pour l'enregistrement : ")
		temps = float(temps)
		for i in range(nbRecording):
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
			if dirName != "":
				random.seed()
				n = hashlib.sha224(str(random.randint(0,1e10))).hexdigest()
				name = dirName + "/" + n + ".wav"
			else:
				n = str(i)
				name = mot + "/" + n + ".wav"
			db.addWave(name,CHANNELS,p.get_sample_size(FORMAT), RATE, frames,p)
			
			print "Fin du mot ", i
	return n
