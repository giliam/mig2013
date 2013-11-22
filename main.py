#!/usr/bin/python
# -*-coding:utf-8 -*

import sys
sys.path.append("db")
sys.path.append("recorder")

from db import Db
db = Db("db/")
choice = 0
while( not choice in range(1,3) ):
    try:
        choice = int(input("Que voulez-vous faire ?\n1-Enregistrer un élément\n2-Réaliser l'analyse d'un enregistrement\n"))
    except NameError:
        print "Ceci n'est pas un nombre !"

if choice == 1:
    from recorder import recorder
    recorder(db)
elif choice == 2:
    pass
else:
    pass
