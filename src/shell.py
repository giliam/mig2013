#!/usr/bin/python
# -*-coding:utf-8 -*
""" Main du programme, permet le choix entre enregistrer un element ou realiser l'analyse d'un enregistrement deja effectue """
import scipy.io.wavfile
import os
from core.utils.constantes import *
from numpy import abs,int16
from core.utils.db import Db
from core.recording.recorder import recorder
from core.recording.sync import syncFile, cutBeginning
from core.handling.passe_haut import passe_haut
from core.handling.fenetre_hann import hann_window
from core.hmm.creationVecteurHMM import creeVecteur
from core.handling.triangularFilterbank import triangularFilter
from core.handling.inverseDCT import inverseDCTII
from core.hmm.tableauEnergyPerFrame import construitTableauEnergy
from core.handling.fft import *
from core.hmm.markov import buildHMMs, saveHMMs, loadHMMs, recognize, recognizeList

def main(verbose=True,action=-1,verboseUltime=True):
    db = Db("../db/",verbose=verbose)
    #HMMs = {}
    #db.addFile("hmmList.txt", HMMs)
    choice = -1
    while( not choice in range(1,8) ):
        try:
            if verboseUltime:
                choice = int(input("Que voulez-vous faire ?\n1-Enregistrer un element\n\
2-Realiser l'analyse d'un mot\n3-Tester\n4-Afficher resultats intermediaires\n5-Gestion des fichiers de la base de donnees\n\
6-Creation d'un HMM\n7-Gerer les HMM\n----------------------------\n"))
            else:
                choice = 2
        except NameError:
            print "Ceci n'est pas un nombre !"
    ####################################
    ###        ENREGISTREMENT        ###
    ####################################
    if choice == 1:
        #Realiser un enregistrement
        recorder(db)
        
        
    ####################################
    ###      ANALYSE D'UN SON        ###
    ####################################
    elif choice == 2:
        fileOk = False
        while not fileOk:
            #On choisit le dossier a afficher
            print "Voici la liste des mots a etudier : "
            dirList = db.printDirFiles("waves/")
            dirChoice = -1
            while( not dirChoice in range(len(dirList)) ):
                try:
                    dirChoice = int( input( "Choisissez un fichier a traiter et entrez son numero : " ) )
                except NameError:
                    print "Ceci n'est pas un nombre !"
            print "Dossier choisi : ", dirList[dirChoice]
            fileOk = True
            numeroTraitement = 0
            filesList = db.printFilesList(dirList[dirChoice])
            print filesList
            action = int( input( "A partir de quelle action souhaitez-vous agir ?\n0-Tout\n1-Filtre passe-haut\n2-Fenetre de Hann\n3-Transformee de Fourier Rapide\n4-Fonction Mel\n5-Creation de la liste Mel\n6-Transformee de Fourier inverse\n7-Creation de vecteurs\n " ) )
            for f in filesList:
                dirName = os.path.dirname(f)
                m = db.getWaveFile(f)
                if action == 2:
                    content = db.getFile("handling/passe_haut_" + dirName + "_" + str(numeroTraitement) + ".txt")                
                elif action == 3:
                    content = db.getFile("handling/hann_" + dirName + "_" + str(numeroTraitement) + ".txt")
                elif action == 4:
                    content = db.getFile("handling/fft_" + dirName + "_" + str(numeroTraitement) + ".txt")
                elif action == 5:
                    content = db.getFile("handling/mel_" + dirName + "_" + str(numeroTraitement) + ".txt")
                elif action == 6:
                    content = db.getFile("handling/mel_tab_" + dirName + "_" + str(numeroTraitement) + ".txt")
                elif action == 7:
                    content = db.getFile("handling/fft_inverse_" + dirName + "_" + str(numeroTraitement) + ".txt")
                else:
                    content = m[1]
                mot,log = handlingOneWord(content,db,dirName,numeroTraitement)
                if verbose:
                    print log
                fileOk = False
                numeroTraitement+=1
                print "Mot reconnu pour " + f + ": ", mot
                
                
    ####################################
    ###         TEST GLOBAL          ###
    ####################################
    elif choice == 3:
        fileName = recorder(db,"tmp",1,False,2,1)
        cutBeginning( Db.prefixPath + "waves/tmp/", fileName + ".wav", "cut_" )
        syncFile( Db.prefixPath + "waves/tmp/", "cut_" + fileName + ".wav", "sync_" )
        db.addFileToList("tmp/sync_cut_" + fileName + ".wav", "waves/")
        finalTest("tmp/sync_cut_" + fileName + ".wav")
        
    ####################################
    ###   RESULTATS INTERMEDIAIRES   ###
    ####################################
    elif choice == 4:
        print "Voici la liste des mots a etudier : "
        dirList = db.printDirFiles("storage/handling/")
        dirChoice = -1
        while( not dirChoice in range(len(dirList)) ):
            try:
                dirChoice = int( input( "Choisissez un fichier a traiter et entrez son numero : " ) )
            except NameError:
                print "Ceci n'est pas un nombre !"
        print "Fichier choisi : ", dirList[dirChoice]
        amp = db.getFile("handling/" + str(dirChoice))
        db.addWaveFromAmp("output/" + str(dirChoice) + ".wav",44100,amp,"output/",False)
        
    
    ######################################
    ### GESTION DES FICHIERS DE LA BDD ###
    ######################################
    elif choice == 5:
        choice3 = -1
        while( not choice3 in range(1,6) ):
            try:
                choice3 = int(input("Que voulez-vous faire ?\n1-Supprimer un fichier\n2-Supprimer un wav\n3-Synchroniser la BDD\n4-Synchroniser les wav\n5-Synchroniser tous les fichiers\n"))
            except NameError:
                print "Ceci n'est pas un nombre !"
        if choice3 == 1:
            print "Fichiers : "
            filesList = db.printDirFiles()
            dirName = "storage/"
        elif choice3 == 2:
            print "Dossiers des waves : "
            filesList = db.printDirFiles("waves/")
            dirName = "waves/"
        elif choice3 == 3:
            db.sync()
            db.sync("", "waves/")
        elif choice3 == 4:
            print "Voici la liste des mots a etudier : "
            dirList = db.printDirFiles("waves/")
            dirChoice = -1
            while( not dirChoice in range(len(dirList)) ):
                try:
                    dirChoice = int( input( "Quel mot souhaitez vous traiter?: " ) )
                except NameError:
                    print "Ceci n'est pas un nombre !"
            print "Dossier choisi : ", dirList[dirChoice]
            filesList = db.printFilesList(dirList[dirChoice])
            for f in filesList:
                cutBeginning( Db.prefixPath + "waves/", f, "" )
                syncFile( Db.prefixPath + "waves/", f, "" )
        elif choice3 == 5:
            db.sync()
            db.sync("", "waves/")
            
    #################################
    ###     CREATION D'UN HMM     ###
    #################################
    elif choice == 6:
        fileOk = False
        while not fileOk:
            #On choisit le dossier a afficher
            print "Voici la liste des mots a etudier : "
            dirList = db.printDirFiles("waves/")
            dirChoice = -1
            while( not dirChoice in range(len(dirList)) ):
                try:
                    dirChoice = int( input( "Choisissez un fichier a traiter et entrez son numero : " ) )
                except NameError:
                    print "Ceci n'est pas un nombre !"
            print "Dossier choisi : ", dirList[dirChoice]
            fileOk = True
            filesList = db.printFilesList(dirList[dirChoice])
            if len(filesList) < 6:
                print "Pas assez d'enregistrements"
                continue
            listVectors = []
            numeroTraitement = 0
            for f in filesList:
                dirName = os.path.dirname(f)
                m = db.getWaveFile(f)
                content,log = handlingRecording(m[1],db,dirName,numeroTraitement)
                listVectors.append(content)
                fileOk = False
                numeroTraitement+=1
            print "Sauvegarde :"
            db.addFile(dirList[dirChoice] + ".txt",listVectors, "hmm/")
            hmmList = db.getFile("hmmList.txt")
            if hmmList.get(dirList[dirChoice]):
                hmmList[dirList[dirChoice]].append(dirList[dirChoice] + ".txt")
            else:
                hmmList[dirList[dirChoice]] = [dirList[dirChoice] + ".txt"]
            print "Extraction :"
            db.addFile("hmmList.txt",hmmList)
            buildHMMs(hmmList.keys(),hmmList.values(), 500, Db.prefixPath + "hmm/")
            saveHMMs(Db.prefixPath + "hmm/save.hmm")
    ####################################
    ###        LISTER LES HMMs       ###
    ####################################
    elif choice == 7:
        hmmList = db.getFile("hmmList.txt")
        print hmmList

def handlingOneWord(content,db,dirChoice,numeroTraitement,action=0):
    """ Fait le traitement d'un mot pour en construire les vecteurs de Markov et tester ensuite la compatibilite avec les automates existants 
            Retourne un tuple (motLePlusCompatible,log) """
    content,log = handlingRecording(content,db,dirChoice,numeroTraitement,action)
    loadHMMs(Db.prefixPath + "hmm/save.hmm")
    return recognize(content),log


def handlingRecording(content,db,dirChoice,numeroTraitement,action=0):
    log = ""
    if action <= 1:
        log += "Filtre passe-haut en cours...\n"
        content = passe_haut(content)
        log += "Filtre passe-haut termine...\n"
        #db.addFile("handling/passe_haut_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt",content)
        #db.addWaveFromAmp("tmp/bob.wav", 44100, content)
        log += "Sauvegarde effectuee...\n\n"
    if action <= 2:
        log += "Fenetre de Hann en cours...\n"
        content = hann_window(content)
        log += "Fenetre de Hann terminee...\n"
        #db.addFile("handling/hann_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt",content)
        log += "Sauvegarde effectuee...\n\n"
    if action <= 3:
        log += "Transformee de Fourier rapide en cours...\n"
        content = fftListe(content,True)
        energyTable = construitTableauEnergy(content)
        for k in range(len(content)):
            for l in range(len(content[k])):
                content[k][l]=abs(content[k][l])
        log += "Transformee de Fourier rapide terminee...\n"
        #db.addFile("handling/fft_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt",content)
        log += "Sauvegarde effectuee...\n\n"
    """
    if action <= 4:
        log += "Application de la fonction Mel en cours..."
        for k in range(len(content)):
            content[k] = fct_mel_pas(content[k],10)
        log += "Application de la fonction Mel terminee..."
        db.addFile("handling/mel_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt",content)
        log += "Sauvegarde effectuee...\n"
    if action <= 5:    
        log += "Construction de la liste Mel en cours..."
        for k in range(len(content)):
            content[k] = mel_tab(content[k],10)
        log += "Construction de la liste Mel terminee..."
        db.addFile("handling/mel_tab_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt",content)
        log += "Sauvegarde effectuee...\n"
    """
    if action <=5:
        log += "Application de la fonction Mel en cours...\n"
        for k in range(len(content)):
            content[k] = triangularFilter(content[k],RATE)
        log += "Application de la fonction Mel terminee...\n"
        #db.addFile("handling/mel_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt",content)
        log += "Sauvegarde effectuee...\n\n"
    if action <= 6:    
        log += "Transformee de Fourier inverse en cours...\n"
        for k in range(len(content)):
            content[k] = inverseDCTII(content[k])
        log += "Transformee de Fourier inverse terminee...\n"
        #db.addFile("handling/fft_inverse_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt",content)
        log += "Sauvegarde effectuee...\n"
    if action <= 7:    
        log += "Creation de vecteurs HMM en cours...\n"
        content = creeVecteur(content, energyTable)
        log += "Creation de vecteurs HMM terminee...\n"
        #db.addFile("handling/vecteurs_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt",content)
        log += "Sauvegarde effectuee...\n\n"
    #db.logDump(str(dirChoice) + "_" + str(numeroTraitement),log)
    #db.logDump(str(dirChoice) + "_" + str(numeroTraitement))
    return content,log

#def handlingOneWord(content,db,dirChoice,numeroTraitement,action=0,hmmList=[]):
def finalTest(fileName = ""):
    db = Db("../db/",verbose=False)
    fileOk = False
    while not fileOk:
        #On choisit le dossier a afficher
        if fileName == "":
            print "Voici la liste des mots a etudier : "
            dirList = db.printDirFiles("waves/")
            dirChoice = -1
            while( not dirChoice in range(len(dirList)) ):
                try:
                    dirChoice = int( input( "Choisissez un fichier a traiter et entrez son numero : " ) )
                except NameError:
                    print "Ceci n'est pas un nombre !"
            print "Dossier choisi : ", dirList[dirChoice]
            fileOk = True
            numeroTraitement = 0
            filesList = db.printFilesList(dirList[dirChoice])
            print filesList
            fileChoice = -1
            while( not fileChoice in range(len(filesList)) ):
                try:
                    fileChoice = int( input( "Choisissez un fichier a traiter et entrez son numero : " ) )
                except NameError:
                    print "Ceci n'est pas un nombre !"
            print "Fichier choisi : ", filesList[fileChoice]
            n = fileChoice
            f = filesList[fileChoice]
            d = dirList[dirChoice]
            fileOk = False
        else:
            f = fileName
            fileOk = True
            n = 1
            d = ""
        dirName = os.path.dirname(f)
        m = db.getWaveFile(f)
        mot,log = handlingOneWord(m[1],db,d,n)
        print "Le mot reconnu est", mot
        print "-----------------------------"
if __name__ == "__main__":
    main(False)
