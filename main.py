#!/usr/bin/python
# -*-coding:utf-8 -*
""" Main du programme, permet le choix entre enregistrer un élément ou réaliser l'analyse d'un enregistrement déjà effectué """
import scipy.io.wavfile
import sys
sys.path.append("src")
from quantification import quantification
from db import Db
from recorder import recorder
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
        filesList = db.printFilesList(dirList[dirChoice])
        for f in filesList:
            m = db.getWaveFile(f)
            print m
elif choice == 3:
    choice3 = -1
    while( not choice3 in range(1,2) ):
        try:
            choice3 = int(input("Que voulez-vous faire ?\n1-Supprimer un fichier\n2-Supprimer un wav\n"))
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
    fileChoice = -1
    while( not fileChoice in range(len(filesList)) ):
        try:
            fileChoice = int( input( "Choisissez un fichier a traiter et entrez son numero : " ) )
        except NameError:
            print "Ceci n'est pas un nombre !"
    db.deleteFileFromList(filesList[fileChoice],dirName)
else:
    pass
