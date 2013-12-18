#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Réalise l'enregistrement d'un certain nombre d'échantillons audio déterminé par l'utilisateur.
		Nécessite PYAUDIO pour fonctionner : http://www.lfd.uci.edu/~gohlke/pythonlibs/ """
import os
import pyaudio
import wave
from core.utils.constantes import *
import random
import hashlib


def recorder(db,dirName="",nbRecording=-1,askForWord=True,seconds=-1,nbWords=1,fileName="",confirm=True):
	""" Procède à l'enregistrement """ 

	if nbRecording < 0:
		nbRecording = raw_input("Combien d'enregistrement par mots ? ")
		nbRecording = int(nbRecording)
	n = ""
	for k in range(nbWords):
		if askForWord:
			mot = raw_input("Entrez le mot a enregistrer : ")
		else:
			mot = ""
			
		if seconds < 0:
			seconds = raw_input("Entrez le nombre de secondes pour l'enregistrement : ")
		seconds = float(seconds) + 1
		
		for i in range(nbRecording):
			if confirm:
				raw_input("Appuyez sur une touche pour commencer l'enregistrement : ")
			p = pyaudio.PyAudio()

			stream = p.open(format=FORMAT,
				channels=CHANNELS,
				rate=RATE,
				input=True,
				frames_per_buffer=CHUNK)

			#print "Enregistrement[", i, "]:"

			frames = []

			for j in range(0, int(RATE / CHUNK * seconds)): 
				data = stream.read(CHUNK)
				frames.append(data)
			
			#print "Fin - Enregistrement[", i, "]:"

			stream.stop_stream()
			stream.close()
			p.terminate()
			if dirName != "":
				random.seed()
				if fileName == "":
					fileName = hashlib.sha224(str(random.randint(0,1e10))).hexdigest()
				name = dirName + "/" + fileName + ".wav"
			else:
				n = str(i)
				name = mot + "/" + n + ".wav"
			db.addWave(name,CHANNELS,p.get_sample_size(FORMAT), RATE, frames,p)
			#print "Fin du mot ", i
	return fileName
