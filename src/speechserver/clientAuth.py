#!/usr/bin/python
# -*-coding:utf-8 -*
import pickle
import sys
sys.path.append("../../src")
from db import Db
dbUser = Db("../../db/",True,"userDbList")

class AuthUser:
    def __init__(self, dB
def cree(userList,fileName="registre"):
	global dbUser
	""" Crée et initialise le dictionnaire contenant les utilisateurs et leurs données """
	dbUser.addFile("users/" + fileName + ".txt",userList)


def lecture(fileName="registre"):
	global dbUser
	""" Renvoie la liste des utilisateurs et leurs données """
	return dbUser.getFile("users/" + fileName + ".txt")


def ajouteUtilisateur(cle,valeur,fileName="registre"):
	global dbUser
	""" Ajoute un utilisateur et des données """
	userList = lecture()
	userList[cle]=valeur
	dbUser.addFile("users/" + fileName + ".txt",userList)
            
    
def affichage(userList):   
	""" Affiche la liste des utilisateurs et leurs données """     
	for cle,valeur in userList.items():
		print(cle, ":", valeur)
	if userList == {}:
		print "Il n'y a pas d'utilisateur"


def supprimeClient(cle):
	""" Supprime un client du dictionnaire """ 
	global dbUser
	dico=lecture(dbUser)
	del dico[cle]
        

def renvoieClient(cle):
	""" Retourne un client s'il se trouve dans la liste des utilisateurs """
	global dbUser
	dico=lecture()
	if cle in dico:
		return(dico[cle])


def ajouteClient(nom,mdp,listeAcces):
	""" Ajoute un utilisateur au système """
	ajouteUtilisateur(nom,[mdp,listeAcces])
      
  
def checkAuth(nom,mdp,acces):
	""" Vérifie que le nom entré se trouve bien dans la liste des utilisateurs """
	global dbUser
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
