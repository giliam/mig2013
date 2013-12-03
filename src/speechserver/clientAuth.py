#!/usr/bin/python
# -*-coding:utf-8 -*
import pickle
import sys

from core.utils.db import Db

DEBUG = False

class AuthUser:
    """ Classe pour gérer l'authentification des applications clientes sur notre
        serveur applicatif """

    def __init__(self, fileName="registre"):
        self.userListFile = fileName
        self.db = Db("../../db/", "userDbList", DEBUG)
        self.userList = self.db.getFile("users/" + fileName + ".txt")

    def newClient(self, client, hashedPass, authorizedDBs):
	    """ Ajoute un utilisateur et des données """
        if not self.userList.get(client):
            self.userList[client] = [hashedPass, authorizedDBs]
	        self.commit()
            return True
        return False

    def updateClient(self, client, hashedPass, authorizedDBs):
	    """ Ajoute un utilisateur et des données """
        if self.userList.get(client):
	        self.userList[client] = [hashedPass, authorizedDBs]
	        self.commit()
            return True
        return False


    def rmClient(self, client):
	    """ Supprime un client du dictionnaire """ 
        if self.userList.get(client):
	        del self.userList[client]
	        self.commit()
            return True
        return False


    def getClient(self, client):
	    """ Retourne un client s'il se trouve dans la liste des utilisateurs """
        return self.userList.get(client)


    def checkAuth(self, client, submittedHashedPass, clientDB):
	    """ Vérifie que le nom entré se trouve bien dans la liste des utilisateurs """
	    hashedPass, clientDBs = self.getClient(client)
	    if hashedPass == submittedHashedPass:
		    if clientDB in clientDBs:
			    return True
	    return False


    def commit(self):
        """ Write the changes of the userlist to the DB on disk """
        self.db.addFile("users/" + self.userListFile + ".txt", userList)


    def __str__(self):   
	    """ Affiche la liste des utilisateurs et leurs données """
        data = ["%s :\t %s" % (client, clientData) for client, clientData in userList.items()]
		return '\n'.join(data)


if __name__ == "__main__":
    authUserHandler = AuthUser()
	print(authUserHandler)
	authUserHandler.newClient("test","bob",[1])
	print(authUserHandler)
