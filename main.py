#!/usr/bin/python
# -*-coding:utf-8 -*
""" Main du programme, permet le choix entre enregistrer un élément ou réaliser l'analyse d'un enregistrement déjà effectué """
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
from creationVecteurHMM import creeVecteur
from triangularFilterbank import triangularFilter
from inverseDCT import inverseDCTII
from tableauEnergyPerFrame import construitTableauEnergy
from fft import *
from hmm import *

def main(verbose=True,action=-1,verboseUltime=True):
    db = Db("db/",verbose)
    choice = -1
    while( not choice in range(1,6) ):
        try:
            if verboseUltime:
                choice = int(input("Que voulez-vous faire ?\n1-Enregistrer un element\n\
2-Realiser l'analyse d'un mot\n3-Tester\n4-Afficher résultats intermédiaires\n5-Gestion des fichiers de la base de donnees\n"))
            else:
                choice = 2
        except NameError:
            print "Ceci n'est pas un nombre !"

    if choice == 1:
        #Réaliser un enregistrement
        recorder(db)
    elif choice == 2:
        fileOk = False
        while not fileOk:
            #On choisit le dossier à afficher
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
            action = int( input( "À partir de quelle action souhaitez-vous agir ?\n0-Tout\n1-Filtre passe-haut\n2-Fenêtre de Hann\n3-Transformée de Fourier Rapide\n4-Fonction Mel\n5-Création de la liste Mel\n6-Transformée de Fourier inverse\n7-Creation de vecteurs\n " ) )
            for f in filesList:
                try:
                    m = db.getWaveFile(f)
                except IOError:
                    break
                if action == 1:
                    content = m[1]
                elif action == 2:
                    content = db.getFile("handling/passe_haut_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt")                
                elif action == 3:
                    content = db.getFile("handling/hann_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt")
                elif action == 4:
                    content = db.getFile("handling/fft_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt")
                elif action == 5:
                    content = db.getFile("handling/mel_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt")
                elif action == 6:
                    content = db.getFile("handling/mel_tab_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt")
                elif action == 7:
                    content = db.getFile("handling/fft_inverse_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt")
                else:
                    content = m[1]
                handlingOneWord(content,db,dirChoice,numeroTraitement)
                fileOk = False
                numeroTraitement+=1
    elif choice == 3:
        print "Vous allez d'abord réaliser l'enregistrement du mot que vous cherchez à tester"
        fileName = recorder(db,"tmp",1,False)
        freq,amp = db.getWaveFile("tmp/" + fileName + ".wav")
        m,l = handlingOneWord(amp,db,fileName,0)
        print m
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
    elif choice == 5:
        choice3 = -1
        while( not choice3 in range(1,4) ):
            try:
                choice3 = int(input("Que voulez-vous faire ?\n1-Supprimer un fichier\n2-Supprimer un wav\n3-Synchroniser les wav\n"))
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
                ampli = db.getWaveFile(f)
                ampli2 = synchro(ampli[1], COEFF_LISSAGE, T_MIN, COEFF_COUPE)
                db.addWaveFromAmp("mod/" + f,ampli[0],ampli2)
        elif choice3 == 4:
            fileChoice = -1
            while( not fileChoice in range(len(filesList)) ):
                try:
                    fileChoice = int( input( "Choisissez un fichier a traiter et entrez son numero : " ) )
                except NameError:
                    print "Ceci n'est pas un nombre !"
            db.deleteFileFromList(filesList[fileChoice],dirName)
    else:
        pass



def handlingOneWord(content,db,dirChoice,numeroTraitement,action=0):
    """ Fait le traitement d'un mot pour en construire les vecteurs de Markov et tester ensuite la compatibilité avec les automates existants 
            Retourne un tuple (motLePlusCompatible,log) """
    log = ""
    if action <= 1:
        log += "Filtre passe-haut en cours..."
        content = passe_haut(content)
        log += "Filtre passe-haut termine..."
        db.addFile("handling/passe_haut_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt",content)
        log += "Sauvegarde effectuee...\n"
    if action <= 2:
        log += "Fenêtre de Hann en cours..."
        content = hann_window(content)
        log += "Fenêtre de Hann terminee..."
        db.addFile("handling/hann_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt",content)
        log += "Sauvegarde effectuee...\n"
    if action <= 3:
        log += "Transformee de Fourier rapide en cours..."
        content = fftListe(content)
        energyTable = construitTableauEnergy(content)
        for k in range(len(content)):
            for l in range(len(content[k])):
                content[k][l]=abs(content[k][l])
        log += "Transformee de Fourier rapide terminee..."
        db.addFile("handling/fft_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt",content)
        log += "Sauvegarde effectuee...\n"
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
        log += "Application de la fonction Mel en cours..."
        for k in range(len(content)):
            content[k] = triangularFilter(content[k],RATE)
        log += "Application de la fonction Mel terminee..."
        db.addFile("handling/mel_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt",content)
        log += "Sauvegarde effectuee...\n"
    if action <= 6:    
        log += "Transformee de Fourier inverse en cours..."
        for k in range(len(content)):
            content[k] = inverseDCTII(content[k])
        log += "Transformee de Fourier inverse terminee..."
        db.addFile("handling/fft_inverse_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt",content)
        log += "Sauvegarde effectuee...\n"
    if action <= 7:    
        log += "Creation de vecteurs HMM en cours..."
        content = creeVecteur(content, energyTable)
        log += "Creation de vecteurs HMM terminee..."
        db.addFile("handling/vecteurs_" + str(dirChoice) + "_" + str(numeroTraitement) + ".txt",content)
        log += "Sauvegarde effectuee...\n"
    """if action == 8:
        log += "Premier essai de Markov..."
        #Nombre de phonems et nombre d'états
        n = len(content)
        m = n
        #
        d = 13
        PI = 
        A = 
        C = 
        mu = 
        sigma = 
        content = ContinuousMarkov(n, m, d, OA_PI, OA_A, OA_C, OA_G_mu, OA_G_sigma)
        print "Premier essai de Markov réussi !
        db.addFile("handling/markov_" + str(numeroTraitement) + ".txt",content)
        log += "Sauvegarde effectuee...\n"
    """
    db.logDump(str(dirChoice) + "_" + str(numeroTraitement),log)
    db.logDump(str(dirChoice) + "_" + str(numeroTraitement))
    motLePlusCompatible = "cheval"
    return motLePlusCompatible,log

if __name__ == "__main__":
    main(True)
