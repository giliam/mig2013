#!/usr/bin/python
# -*-coding:utf-8 -*
""" Main du programme, permet le choix entre enregistrer un élément ou réaliser l'analyse d'un enregistrement déjà effectué """
import scipy.io.wavfile
import sys
sys.path.append("src")


from numpy import abs
from db import Db
from recorder import recorder
from passe_haut import passe_haut
from fenetre_hann import hann_window
from fft import fftListe
from mel import fct_mel_pas, mel_tab
from discrete_cosine_transform import inverseDCTII

db = Db("db/")
choice = -1
while( not choice in range(1,4) ):
    try:
        choice = int(input("Que voulez-vous faire ?\n1-Enregistrer un element\n\
2-Realiser l'analyse d'un mot\n3-Gestion des fichiers de la base de donnees\n"))
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
        action = int( input( "À partir de quelle action souhaitez-vous agir ?\n0-Tout\n1-Filtre passe-haut\n2-Fenêtre de Hann\n3-Transformée de Fourier Rapide\n4-Fonction Mel\n5-Création de la liste Mel\n6-Transformée de Fourier inverse\n " ) )
        for f in filesList:
            if fileOk == False:
                break
            m = db.getWaveFile(f)
            
            if action == 1:
                content = m[1]
            elif action == 2:
                content = db.getFile("handling/passe_haut_" + str(numeroTraitement) + ".txt")                
            elif action == 3:
                content = db.getFile("handling/hann_" + str(numeroTraitement) + ".txt")
            elif action == 4:
                content = db.getFile("handling/fft_" + str(numeroTraitement) + ".txt")
            elif action == 5:
                content = db.getFile("handling/mel_" + str(numeroTraitement) + ".txt")
            elif action == 6:
                content = db.getFile("handling/mel_tab_" + str(numeroTraitement) + ".txt")
            else:
                content = m[1]

            print "Extraction réussie...\n"
            if action <= 1:
                print "Filtre passe-haut en cours..."
                content = passe_haut(content)
                print "Filtre passe-haut terminé..."
                db.addFile("handling/passe_haut_" + str(numeroTraitement) + ".txt",content)
                print "Sauvegarde effectuée...\n"
            if action <= 2:
                print "Fenêtre de Hann en cours..."
                content = hann_window(content)
                print "Fenêtre de Hann terminée..."
                db.addFile("handling/hann_" + str(numeroTraitement) + ".txt",content)
                print "Sauvegarde effectuée...\n"
            if action <= 3:
                print "Transformée de Fourier rapide en cours..."
                content = fftListe(content)
                for k in range(len(content)):
                    for l in range(len(content[k])):
                        content[k][l]=abs(content[k][l])
                print "Transformée de Fourier rapide terminée..."
                db.addFile("handling/fft_" + str(numeroTraitement) + ".txt",content)
                print "Sauvegarde effectuée...\n"
            if action <= 4:
                print "Application de la fonction Mel en cours..."
                for k in range(len(content)):
                    content[k] = fct_mel_pas(content[k],1./44100.)
                print "Application de la fonction Mel terminée..."
                db.addFile("handling/mel_" + str(numeroTraitement) + ".txt",content)
                print "Sauvegarde effectuée...\n"
            if action <= 5:    
                print "Construction de la liste Mel en cours..."
                for k in range(len(content)):
                    content[k] = mel_tab(content[k],1./44100.)
                print "Construction de la liste Mel terminée..."
                db.addFile("handling/mel_tab_" + str(numeroTraitement) + ".txt",content)
                print "Sauvegarde effectuée...\n"
            if action <= 6:    
                print "Transformée de Fourier inverse en cours..."
                for k in range(len(content)):
                    content[k] = inverseDCTII(content[k])
                print "Transformée de Fourier inverse terminée..."
                db.addFile("handling/fft_inverse_" + str(numeroTraitement) + ".txt",content)
                print "Sauvegarde effectuée...\n"
            print "Ok"
            fileOk = False
            numeroTraitement+=1
elif choice == 3:
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
            scipy.io.wavfile.write("db/waves/mod/"+f, ampli[0], int16(ampli2))
    fileChoice = -1
    while( not fileChoice in range(len(filesList)) ):
        try:
            fileChoice = int( input( "Choisissez un fichier a traiter et entrez son numero : " ) )
        except NameError:
            print "Ceci n'est pas un nombre !"
    db.deleteFileFromList(filesList[fileChoice],dirName)
else:
    pass
