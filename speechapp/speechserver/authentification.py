import pickle
import os
os.chdir("C:/Users/Axel/Desktop/")

print(__file__)

def creer(dico):
	with open("registre.txt","w") as f:
		pickle.Pickler(f).dump(dico)

def lecture():
	with open("registre.txt","r") as f:
		contenu = pickle.Unpickler(f).load()
	return(contenu)

def append(cle,valeur):
	dico=lecture()
	dico[cle]=valeur
	with open("registre.txt","w") as f:
		pickle.Pickler(f).dump(dico)
		
def affichage(dico):	
	for cle in dico:
		print(cle, ":", dico[cle])

def removeClient(cle):
	dico=lecture()
	del dico["cle"]
	init(dico)
	
def renvoitClient(cle):	
	if 'cle' in dic:
		return(dic['cle'])
		
def nouveauClient(mdp,listeAcces):	
	return([mdp,listeAcces])

def ajoutClient(nom,mdp,listeAcces):
	append(nom,nouveauClient(mdp,listeAcces))
	
"""systeme de test"""	
creer({})
ajoutClient("Bob","mdpbob",[1,0,0])
ajoutClient("Joe","mdpjoe",[1,0,1])
affichage(lecture())
