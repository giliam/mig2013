#!/usr/bin/python
# -*-coding:utf-8 -*
import pickle
import sys
sys.path.append("../../src")
from db import Db
print(__file__)
dbUser = Db("../../db/",True,"userDbList")
#Initialisation
dbUser.addFile("users/registre.txt",{})
#Lecture
userList = dbUser.getFile("users/registre.txt")

userList["cle1"] = "valznizugn"
userList["cle21"] = "vaazeleur"
userList["cle3"] = "valedfgnur"
userList["cle54"] = "valvvv<iopeur"
dbUser.addFile("users/registre.txt",userList)
#Affichage
print userList

#Suppression
del userList["cle1"]

#Renvoie le client
if "cle1" in userList:
	print userList["cle1"]
		
#Nouveau client
def ajoutClient(userList,username,password):
	if username in userList:
		print "Existe déjà"
	else:
		userList[username] = password
		print "Bien ajouté"
	dbUser.addFile("users/registre.txt",userList)
