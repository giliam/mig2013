#!/usr/bin/env python2
# -*- coding; utf-8 -*-

"""Module de conversion de fichiers ogg en wav
Il faut avoir sox et soundrecorder sur le serveur"""

import os
from random import randint

TMP_DIR = "tmp/"

def path_orig_ogg(id):
    return TMP_DIR + "orig_" + str(id) + ".ogg"


def path_mid_wave(id):
    return TMP_DIR + "orig_" + str(id) + ".wav"


def path_final_wave(id):
    return TMP_DIR + "wave_final_" + str(id) + ".wav"


def rm_multi(*files):
    """Remove multiple files"""
    for path in files:
        os.remove(path)

def convert_ogg_blob_to_wave_blob(oggBlob):
    """Converti le blob ogg en blob wav"""
    id = randint(1, 1000)
    while os.access(path_orig_ogg(id), os.W_OK):
        id = randint(1, 1000)

    with open(path_orig_ogg(id), 'w') as origoggfile:
         origoggfile.write(oggBlob)
         origoggfile.flush()
         os.fsync(origoggfile)
         origoggfile.close()

    #Now convert the file

    os.system('soundconverter -b -m audio/x-wav -s .wav "%s"' %  path_orig_ogg(id))
    #Resample to 44.1kHz
    os.system('sox -r 44.1k -e signed -c 2 -b 16 %s %s' % (path_mid_wave(id), path_final_wave(id)))

    #And read the oggBlob

    with open(path_final_wave(id), 'r') as finalwavefile:
        waveBlob =  finalwavefile.read()
        finalwavefile.close()
    
    #Remove the files
    rm_multi(path_orig_ogg(id), path_mid_wave(id), path_final_wave(id))
    return waveBlob

def convert_ogg_to_wav(ogg_path, out_wav_path):
    try:
        with open(ogg_path, 'r') as origoggfile:
            waveBlob = convert_ogg_blob_to_wave_blob(origoggfile.read())
            origoggfile.close()
    except:
        return "Impossible to open ogg file"      

    try:
        with open(out_wav_path, 'w') as out_wav:
             out_wav.write(waveBlob)
             out_wav.flush()
             os.fsync(out_wav)
             out_wav.close()
    except:
        return "Impossible to write wav blob to dest file"

    return True

if __name__ == '__main__':
    print(convert_ogg_to_wav('test.oga', 'test.wav')) 