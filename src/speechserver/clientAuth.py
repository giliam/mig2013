#!/usr/bin/python
# -*-coding:utf-8 -*
import pickle
import sys

from core.utils.db import Db

DEBUG = False

class AuthUser:
    def __init__(self, authDB):
        self.db = Db("../../db/", "userDbList", DEBUG)
        self.userList = self.db.getFile("users/" + fileName + ".txt")

    def init_set(self, userList, fileName="registre"):
	    """ Crée et initialise le dictionnaire contenant les utilisateurs et leurs données """
	    self.db.addFile("users/" + fileName + ".txt", userList)


    def newUser(self, client, hashedPass, authorizedDbs, fileName="registre"):
	    """ Ajoute un utilisateur et des données """
        if not self.userList.get(client):
	        self.userList[cle] = valeur
	        self.db.addFile("users/" + fileName + ".txt",userList)
            return True
        return False
                
        
    def __str__(self):   
	    """ Affiche la liste des utilisateurs et leurs données """
        data = ["%s :\t %s" % (client, clientData) for client, clientData in userList.items()]
		return '\n'.join(data)


    def rmClient(client):
	    """ Supprime un client du dictionnaire """ 
        if self.userList.get(client):
	        del self.userList[client]
            return True
        return False
            

    def getClient(client):
	    """ Retourne un client s'il se trouve dans la liste des utilisateurs """
	    return self.userList.get(client):


    def addClient(nom, mdp, listeAcces):
	    """ Ajoute un utilisateur au système """
	    ajouteUtilisateur(nom,[mdp,listeAcces])
          
      
    def checkAuth(self.nom, mdp, acces):
	    """ Vérifie que le nom entré se trouve bien dans la liste des utilisateurs """
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
