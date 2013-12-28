#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Module de conversion de fichiers ogg en wav
Il faut avoir sox et soundrecorder sur le serveur"""
import pysox
import os
import hashlib
import scipy.io.wavfile
from core.recording import sync
from random import randint
from time import sleep

TMP_DIR = "tmp/"

def path_orig_ogg(id):
    return TMP_DIR + "orig_" + str(id) + ".ogg"


def path_mid_wave(id):
    return TMP_DIR + "orig_" + str(id) + ".wav"

def path_mid_wave_splitted(id):
    return TMP_DIR, "orig_" + str(id) + ".wav"

def path_final_wave(id):
    return TMP_DIR + "wave_final_" + str(id) + ".wav"

def path_final_wave_splitted(id):
    return TMP_DIR, "wave_final_" + str(id) + ".wav"

def rm_multi(*files):
    """Remove multiple files"""
    for path in files:
        os.remove(path)

def handleOGGBlob(oggBlob):
    """Converti le blob ogg en blob wav"""
    id = randint(1, 1000)
    while os.access(path_orig_ogg(id), os.W_OK):
        id = randint(1, 1000)

    writeBlobToDisk(oggBlob, path_orig_ogg(id))

    #Now convert the file

    print(path_orig_ogg(id))
    os.system('soundconverter -b -m audio/x-wav -s .wav "%s"' %  path_orig_ogg(id))
    #Resample to 44.1kHz

    return finalHandling(id)


def finalHandling(id):
    print('final handling started')
    #os.system('sox -r 44.1k -e signed -c 1 -b 16 %s %s' % (path_mid_wave(id), path_final_wave(id)))
    os.system('cp %s %s' % (path_mid_wave(id), path_final_wave(id)))
    print('soxed')
    #And read the oggBlob

    '''with open(path_final_wave(id), 'r') as finalwavefile:
        waveBlob =  finalwavefile.read()'''


    dir, file = path_final_wave_splitted(id)
    print(dir, file)
    waveBlob = cutsyncaudio(dir, file)
    
    #Remove the files
    rm_multi(path_mid_wave(id), )#path_final_wave(id))
    print("success")
    return waveBlob

def handleWAVBlob(audioBlob):
    id = randint(1, 1000)
    while os.access(path_mid_wave(id), os.W_OK):
        id = randint(1, 1000)

    writeBlobToDisk(audioBlob, path_mid_wave(id))
    print path_mid_wave(id)
    print "bringing id to finalHandling"
    return finalHandling(id)

    

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
 

def convert_ogg_to_wav(ogg_path, out_wav_path):
    try:
        with open(ogg_path, 'r') as origoggfile:
            waveBlob = handleOGGBlob(origoggfile.read())
    except:
        return "Impossible to open ogg file"      

    try:
        with open(out_wav_path, 'w') as out_wav:
             out_wav.write(waveBlob)
             out_wav.flush()
             os.fsync(out_wav)
    except:
        return "Impossible to write wav blob to dest file"

    return waveBlob
    
def sox_handling(wavBlob,pathToTmp="../db/waves/tmp/"):
    tempFileName = hashlib.sha224(str(randint(0,1e10))).hexdigest()
    fileName = pathToTmp + str(tempFileName) + ".wav"
    with open(fileName, 'w') as origoggfile:
         origoggfile.write(wavBlob)
         origoggfile.flush()
         os.fsync(origoggfile)

    os.system('ffmpeg -i "' + fileName + '" -vn -ss 00:00:00 -t 00:00:01 "' + pathToTmp + 'noiseaud.wav"')
    print("noise extracted")
    os.system('sox "' + pathToTmp + 'noiseaud.wav" -n noiseprof "' + pathToTmp + 'noise.prof"')
    print("noise selected")
    sleep(1)
    os.system('sox "' + fileName + '" "' + fileName + '" noisered "' + pathToTmp + 'noise.prof" 0.21')
    print("noise trashed")
    #os.remove(pathToTmp + "noise.prof")
    #os.remove(pathToTmp + "noiseaud.wav")

    wav_content = scipy.io.wavfile.read(fileName)
    return wav_content


if __name__ == '__main__':
    print(sox_handling(convert_ogg_to_wav('test.oga', 'test.wav')))
