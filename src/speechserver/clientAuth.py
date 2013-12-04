#!/usr/bin/python
# -*-coding:utf-8 -*

import hashlib
from core.utils.db import Db

DEBUG = False

class AuthUser:
    """ Classe pour gérer l'authentification des applications clientes sur notre
        serveur applicatif """

    def __init__(self, fileName="registre"):
        self.userListFile = fileName
        self.db = Db("../db/", "userDbList", DEBUG)
        self.userList = self.db.getFile("users/" + fileName + ".txt")
	self.username = ""
	self.password = ""
	self.connected = False

    
    def newClient(self, client, hashedPass, authorizedDBs):
	""" Ajoute un utilisateur et des données """
        if not self.getClient(client):
            self.userList[client] = hashedPass, authorizedDBs
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


    def getClients(self):
	print self.userList

    def getClient(self, client):
	""" Retourne un client s'il se trouve dans la liste des utilisateurs """
	if self.userList.get(client):
	    return self.userList[client]
	else:
	    return False


    def checkAuth(self, client, submittedHashedPass, clientDB=""):
	""" Vérifie que le nom entré se trouve bien dans la liste des utilisateurs """
	if self.getClient(client):
	    hashedPass, clientDBs = self.getClient(client)
	    if hashedPass == submittedHashedPass:
		if clientDB == "" or clientDB in clientDBs:
		    return True
	return False
    
    def logIn(self, client, submittedHashedPass):
	""" Connecte l'utilisateur """
	if self.getClient(client):
	    hashedPass, clientDBs = self.getClient(client)
	    if hashedPass == submittedHashedPass:
		self.username = client
		self.password = submittedHashedPass
		self.connected = True
		return True
	return False
    
    def logOut(self):
	self.username = ""
	self.password = ""
	self.connected = False
    
    def hashPass(self,password):
	return hashlib.sha224(password).hexdigest()
    
    
    def commit(self):
        """ Write the changes of the userlist to the DB on disk """
        self.db.addFile("users/" + self.userListFile + ".txt", self.userList)


    def __str__(self):   
	""" Affiche la liste des utilisateurs et leurs données """
        data = ["%s :\t %s" % (client, clientData) for client, clientData in self.userList.items()]
	return '\n'.join(data)


if __name__ == "__main__":
    authUserHandler = AuthUser()
    print(authUserHandler)
    authUserHandler.newClient("demo","demo",[1])
    print(authUserHandler)
