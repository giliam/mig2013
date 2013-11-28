#!/usr/bin env python2
# -*- coding: utf-8 -*-

"""Ici se joue la décision dans les actions à effectuer à partir de la requêtes
du client

actions possibles : add_word_record, list_word_records, rm_word_record, 
                    recognize_spoken_word"""
import scipy.io.wavfile
import sys
sys.path.append("src")

from constantes import *
from numpy import abs,int16
from db import Db
from recorder import recorder
from synchronisation import synchro
from passe_haut import passe_haut
from fenetre_hann import hann_window
from fft import fftListe
from creationVecteurHMM import creeVecteur
from triangularFilterbank import triangularFilter
from inverseDCT import inverseDCTII
from tableauEnergyPerFrame import construitTableauEnergy
import coreProject

def requestHandling(clientDb, action, data):
	
	if not action in ["add_word","list_word_records","rm_word_record","recognize_spoken_word","listen_recording"]:
		return "Unavailable action"
	
	if action == "add_word": #Pas encore possible de stocker un HMM, à voir plus tard
		try:				
			word = data["word"]
			content = data["audiofile"]
		except IOError:
			return "File not found"
		
			
			
	elif action == "recognize_spoken_word":
		try:
			content = data["audiofile")]
		word,log = handlingOneWord(content,clientDb,1,1):
		return word
		
	elif action == "lits_word_records": #renvoie un tableau de mots enregistrés
		tab = zeros(len(clientDb))
		i = 0
		try:
			for k,v in clientDb.iteritems():
				tab[i] = k
				i += 1
			return tab
		except IOError:
			return "File not found"
	
	elif action == "rm_word_record":
		try:
			word = data["word"]
			del clientDb[word]
		except IOException:
			return "File not found"
	
	elif action == "listen_recording"
		try:
			return data["audiofile"]
		except IOException:
			return "file not found" 
	
	
	
	
		
	 

			
		
		
		
		
		
    
