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
	del dico[cle]
	init(dico)
	
def renvoitClient(cle):
	dico=lecture()
	if cle in dico:
		return(dico[cle])
		
def ajoutClient(nom,mdp,listeAcces):
	append(nom,[mdp,listeAcces])
	
def checkAuth(nom,mdp,acces):
	res=False
	dico=lecture()
	if renvoitClient(nom)[0]==mdp:
		if acces in renvoitClient(nom)[1]:
			res=True
	return(res)
	
"""systeme de test"""	
creer({})
ajoutClient("A","a",["a"])
ajoutClient("Joe","mdpjoe",["a","b"])
print(renvoitClient("A"))
print(renvoitClient("A")[1])
affichage(lecture())
print(checkAuth("A","a","a"))
