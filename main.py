#!/usr/bin/python
# -*-coding:utf-8 -*
""" Main du programme, permet le choix entre enregistrer un élément ou réaliser l'analyse d'un enregistrement déjà effectué """
import sys
sys.path.append("db")
sys.path.append("recorder")

from db import Db
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
    from recorder import recorder
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
elif choice == 3:
    db.printDirFiles()
else:
    pass
