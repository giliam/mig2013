#!/usr/bin/python
# -*-coding:utf-8 -*
import pickle
import sys

from core.db import Db


class AuthUser:
    def __init__(self, authDB):
        
    def newUser(self, userList, fileName="registre"):
	    """ Crée et initialise le dictionnaire contenant les utilisateurs et leurs données """
	    dbUser.addFile("users/" + fileName + ".txt", userList)


    def lecture(self, fileName="registre"):
	    """ Renvoie la liste des utilisateurs et leurs données """
	    return dbUser.getFile("users/" + fileName + ".txt")


    def ajouteUtilisateur(self, cle,valeur,fileName="registre"):
	    """ Ajoute un utilisateur et des données """
	    userList = lecture()
	    userList[cle] = valeur
	    dbUser.addFile("users/" + fileName + ".txt",userList)
                
        
    def affichage(userList):   
	    """ Affiche la liste des utilisateurs et leurs données """     
	    for cle,valeur in userList.items():
		    print(cle, ":", valeur)
	    if userList == {}:
		    print "Il n'y a pas d'utilisateur"


    def supprimeClient(cle):
	    """ Supprime un client du dictionnaire """ 
	    dico=lecture(dbUser)
	    del dico[cle]
            

    def renvoieClient(cle):
	    """ Retourne un client s'il se trouve dans la liste des utilisateurs """
	    dico=lecture()
	    if cle in dico:
		    return(dico[cle])


    def ajouteClient(nom,mdp,listeAcces):
	    """ Ajoute un utilisateur au système """
	    ajouteUtilisateur(nom,[mdp,listeAcces])
          
      
    def checkAuth(nom,mdp,acces):
	    """ Vérifie que le nom entré se trouve bien dans la liste des utilisateurs """
	    dico=lecture()
	    l = renvoieClient(nom)
	    if l[0] == mdp:
		    if acces in l[1]:
			    return True
	    return False


if __name__ == "__main__":
	cree({})
	affichage(lecture())
	ajouteClient("test","bob",1)
	affichage(lecture())
