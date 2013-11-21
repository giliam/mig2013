#!/usr/bin/python
# -*-coding:utf-8 -*
import os
import pickle
""" Instancie la base de données """
class Db:
    """ Créé un gestionnaire de fichiers pour stocker les HMM 
        Attributs :
            -> filesList : liste des fichiers gérés par la base de données """
    def __init__(self):
        """ Constructeur """
        try:
            with open("storage/list.txt","r") as f:
                self.filesList = pickle.Unpickler(f).load()
        except IOError:
            Db.reset()
            raise Exception("L'instanciation a été annulée car le fichier de gestion de la base de données n'existe pas")
        
    def getFile(self,filePath):
        """ Ajoute un fichier à la liste des fichiers gérés par la base de données """
        if filePath in self.filesList:
            try:
                with open(filePath,"r") as f:
                    contenu = f.read()
                return contenu
            except IOError:
                raise Exception("La lecture de fichier a échoué")
        else:
            print "le fichier n'est pas géré pas la base de données"
            return ""
    
    
    def addFileToList(self,filePath):
        """ Ajoute un fichier à la liste des fichiers gérés par la base de données """
        if os.access(filePath,os.F_OK):
            self.filesList.append(filePath)
            self.syncToFile()
            print "L'insertion du fichier a bien été effectuée"
        else:
            print "Le fichier n'existe pas"
    
    
    def syncToFile(self):
        """ Met le fichier de stockage de la liste des fichiers à jour """
        try:
            with open("storage/list.txt","w") as f:
                pickle.Pickler(f).dump(self.filesList)
        except IOError:
            raise Exception("Le fichier n'existe pas")
    
    
    def reset(force=False):
        """ Reset la liste des fichiers """
        if force or int(input("Êtes-vous sûr de vouloir réinitialiser la liste des fichiers ? (Oui = 0/Non = 1)")) == 0:
            with open("storage/list.txt","w") as f:
                c = pickle.Pickler(f)
                c.dump([])
            print "Réinitialisation réussie"
    reset = staticmethod(reset)
    
db = Db()
db.addFileToList("storage/test.txt")
db.getFile("storage/test.txt")
