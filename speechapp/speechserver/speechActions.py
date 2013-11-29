#!/usr/bin env python2
# -*- coding: utf-8 -*-

"""Ici se joue la décision dans les actions à effectuer à partir de la requêtes
du client

actions possibles : add_word_record, list_word_records, rm_word_record, 
                    recognize_spoken_word"""
import scipy.io.wavfile
import sys
sys.path.append("../../")
from main import *
import numpy as np

def requestHandling(clientDb, action, data):
	
	if not action in ["add_word","list_word_records","rm_word_record","recognize_spoken_word","listen_recording"]:
		return "Unavailable action"
	
	if action == "add_word": #Pas encore possible de stocker un HMM, à voir plus tard
		try:				
			word = data["word"]
			content = data["audiofile"]
		except KeyError:
			return "File not found"
		
			
			
	elif action == "recognize_spoken_word":
		try:
			dbWaves = Db("db/",False)
			content = data["audiofile"]
			word,log = handlingOneWord(content,dbWaves,1,1,0,clientDb):
			return word
		except KeyError
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
	
	elif action == "listen_recording"
		try:
			return data["audiofile"]
		except KeyError:
			return "file not found" 
	
	
	
	
		
	 

			
		
		
		
		
		
    
