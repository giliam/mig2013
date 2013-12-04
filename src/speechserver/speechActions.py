#!/usr/bin env python2
# -*- coding: utf-8 -*-

"""Ici se joue la décision dans les actions à effectuer à partir de la requêtes
du client

actions possibles : add_word_record, list_word_records, rm_word_record, 
                    recognize_spoken_word"""

from core.main import *
from core.utils.db import Db

from speechserver.audioConverter import *


ACTIONS = ["add_word","list_word_records","rm_word_record","recognize_spoken_word","listen_recording"]

class requestHandling:
    def __init__(self, clientDBid, action, data):
        self.dbWaves = Db('../db/', verbose=False)

        if not action in ACTIONS:
            return False

        if action == "recognize_spoken_word":
            audioBlob = data.getvalue("audioBlob")
            audioType = data.getvalue("audioType")
            if not (audioBlob or audioType):
                return None
            else:
                return self.recognize_spoken_word(audioBlob, audioType, clientDBid)

    def recognize_spoken_word(self, audioBlob, audioType, clientDBid):
        """ Handle the specific request to recognize a spoken word """
        TYPES = ['wav', 'ogg']
        if audioType not in TYPES:
            return False
        
        if audioType == 'ogg':
            audioBlob = convert_ogg_blob_to_wave_blob(audioBlob)
        
        respWord, log = handlingOneWord(sox_handling(audioBlob), self.dbWaves, 1, 1, 0, clientDBid)
        return {'respWord': respWord}
