#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Module de conversion de fichiers ogg en wav
Il faut avoir sox et soundrecorder sur le serveur"""

import os
import scipy.io.wavfile
from core.recording import sync
from random import randint

TMP_DIR = "tmp/"

def pathAudio(id, audioType="wav"):
    return TMP_DIR + "sample_%s.%s" % (id, audioType)




def handleBlob(audioBlob, audioType):
    """Converti le blob ogg en blob wav"""

    id = randint(1, 1000)
    while os.access(pathAudio(id), os.W_OK):
        id = randint(1, 1000)

    writeBlobToDisk(audioBlob, pathAudio(id, audioType))


    if audioType != "wav":
        cmd = "gst-launch-1.0 filesrc location=%s ! decodebin ! audioconvert ! audioresample ! audio/x-raw, rate=44100, channels=1 ! wavenc ! filesink location=%s"  % (pathAudio(id, audioType), pathAudio(id))
        os.system(cmd)
        os.remove(pathAudio(id, audioType))

    dir, file = TMP_DIR, "sample_%s.wav" % id
    print(dir, file)
    waveBlob = cutsyncaudio(dir, file)
    
    os.remove(pathAudio(id))

    return waveBlob

   

def writeBlobToDisk(audioBlob, path):
    with open(path, 'w') as origfile:
        origfile.write(audioBlob)
        origfile.flush()
        os.fsync(origfile)


def cutsyncaudio(dir, file):
    sync.cutBeginning(dir, file, prefix='')
    sync.syncFile(dir, file, prefix='')

    waveBlob = scipy.io.wavfile.read(dir + file)

    return waveBlob
