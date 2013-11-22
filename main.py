#!/usr/bin/python
# -*-coding:utf-8 -*
""" Main du programme, permet le choix entre enregistrer un élément ou réaliser l'analyse d'un enregistrement déjà effectué """
import sys
sys.path.append("db")
sys.path.append("recorder")

from db import Db
db = Db("db/")
choice = -1
while( not choice in range(1,3) ):
    try:
        choice = int(input("Que voulez-vous faire ?\n1-Enregistrer un élément\n2-Réaliser l'analyse d'un enregistrement\n"))
    except NameError:
        print "Ceci n'est pas un nombre !"

if choice == 1:
    #Réaliser un enregistrement
    from recorder import recorder
    recorder(db)
elif choice == 2:
    fileOk = False
    while not fileOk:
        #Analyser un enregistrement
        print "Voici la liste des fichiers : "
        filesList = db.printFilesList(".wav")
        fileChoice = -1
        while( not fileChoice in range(len(db.filesList)) ):
            try:
                fileChoice = int( input( "Choisissez un fichier à traiter et entrez son numéro : " ) )
            except NameError:
                print "Ceci n'est pas un nombre !"
        if fileChoice in filesList:
            print "Fichier choisi : ", db.filesList[fileChoice]
            fileOk = True
            contentFile = db.getWaveFile(db.filesList[fileChoice])
        else:
            print "Ce fichier n'est pas dans la liste, veuillez recommencer"
else:
    pass
