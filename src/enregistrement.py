# -*- coding: utf-8 -*-

import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"
RECORD_SECONDS = 1

nb_mots = raw_input("Combien d'enregistrement par mots?")
nb_mots = int(nb_mots)

while True:
	mot = raw_input("Entrer le mot à enregistrer")
	for i in range(nb_mots):
		p = pyaudio.PyAudio()

		stream = p.open(format=FORMAT,
						channels=CHANNELS,
						rate=RATE,
						input=True,
						frames_per_buffer=CHUNK)

		print "Enregistrement[", i, "]:"

		frames = []

		for j in range(0, int(RATE / CHUNK * RECORD_SECONDS)): 
			data = stream.read(CHUNK)
			frames.append(data)
		
		print "Fin - Enregistrement[", i, "]:"

		stream.stop_stream()
		stream.close()
		p.terminate()
		
		name = mot + "/" + str(i) + ".wav"

		wf = wave.open(name, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()
		
		print "fin du mot ", i
		raw_input("appuyer sur une touche pour le prochain mot")