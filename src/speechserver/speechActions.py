#!/usr/bin env python2
# -*- coding: utf-8 -*-

"""Ici se joue la décision dans les actions à effectuer à partir de la requêtes
du client

actions possibles : add_word_record, list_word_records, rm_word_record, 
                    recognize_spoken_word"""

import scipy.io.wavfile
import sys
sys.path.append("../../")
sys.path.append("../../src")
from main import *
from db import Db
import numpy as np
dbWaves = Db("../../db/",False)
dbWaves.addFile("hmmList.txt",{})
dbWaves.addFile("clientDbList.txt",{})


def requestHandling(clientDbId, action, data):
	if not action in ["add_word","list_word_records","rm_word_record","recognize_spoken_word","listen_recording"]:
		return "Unavailable action"
	

	if action == "add_word": #Pas encore possible de stocker un HMM, à voir plus tard
		try:
			hmmList = dbWaves.getFile("hmmList.txt")
			if len(hmmList) == 0:
				nextId = 0
			else:
				nextId = max(hmmList.keys())+1
			word = data["word"]
			content = data["audiofile"]
			hmm = ampToHMMFromList(content)
			hmmList[nextId] = (word,nextId)
			db.addFile("hmmList.txt",hmmList)
			db.addFile("hmm/" + str(nextId) + ".txt",hmm)
			clientDbsList = dbWaves.getFile("clientDbList.txt")
			if word in clientDbsList[clientDbId]:
				return "Word already in clientDb"
			else:
				clientDbsList[clientDbId][word] = "hmm/" + str(nextId) + ".txt"
				dbWaves.add("clientDbList.txt", clientDbsList)

		except KeyError:
			return "File not found"

	elif action == "recognize_spoken_word":
		try:
	        audioBlob = data["audioBlob"]
            audioType = data["audioType"]
            if audioType == "ogg":
                audioBlob = convert_ogg_blob_to_wave_blob(audioBlob)
			respWord, log = handlingOneWord(audioBlob, dbWaves, 1, 1, 0, clientDb)
			return {'respWord': respWord}
		except KeyError:
			return "File not found"
		
	elif action == "list_word_records": #renvoie un tableau de mots enregistrés
		tab = np.zeros(len(clientDb))
		i = 0
		try:
			for k, elt in enumerate(clientDb):
				tab[i] = elt
				i += 1
			return tab
		except KeyError:
			return "File not found"
	
	elif action == "rm_word_record":
		try:
			word = data["word"]
			del clientDb[word]
		except KeyError:
			return "File not found"
	
	elif action == "listen_recording":
		try:
			return data["audiofile"]
		except KeyError:
			return "file not found" 
