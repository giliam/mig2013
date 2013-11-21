#!/usr/bin/python
# -*-coding:utf-8 -*
import os
import pickle
import random
import wave 

""" Instancie la base de données """
class Db:
    """ Créé un gestionnaire de fichiers pour stocker les HMM 
        Attributs :
            -> filesList : liste des fichiers gérés par la base de données """
            
    filesListName = "filesList"
    prefix = ""
    
    def __init__(self, prefix = ""):
        """ Constructeur """
        Db.prefix = prefix
        try:
            with open(Db.prefix + Db.filesListName + ".txt","r") as f:
                self.filesList = pickle.Unpickler(f).load()
        except IOError:
            Db.reset(True)
            raise Exception("L'instanciation a été annulée car le fichier de gestion de la base de données n'existe pas")



    def getFile(self,fileName,dirFile=""):
        """ Ajoute un fichier à la liste des fichiers gérés par la base de données 
            Paramètres : 
                @fileName : nom du fichier dans le dossier storage
                @dirFile : ajoute une façon spécifique de gérer certains fichiers
        """
        if len(dirFile) == 0:
            dirFile = "storage"
        if fileName in self.filesList:
            try:
                if dirFile == "wave":
                    content = wavfile.read(Db.prefix + dirFile + "/" + fileName, "r")
                    return content
                elif fileName in self.filesList:
                    with open(Db.prefix + dirFile + "/" + fileName,"r") as f:
                        content = f.read()
                    return content
            except IOError:
                raise Exception("La lecture de fichier a échoué")
        else:
            print "le fichier n'est pas géré pas la base de données"
            return ""


    
    
    def getWaveFile(self,fileName):
        """ Alias de getFile pour les Wave """
        return self.getFile(fileName,"wave")
    
    
    
    def addWave(self,fileName,CHANNELS,FORMAT,RATE,frames,p):
        if os.access(Db.prefix + "waves/" + fileName,os.F_OK):
            pass
            #Il faudrait rajouter la gestion de l'existence de deux mêmes fichiers
        dirName = os.path.dirname(fileName)
        if not os.access(Db.prefix + "waves/" + dirName,os.F_OK):
            os.mkdir(Db.prefix + "waves/" + dirName)
        wf = wave.open(Db.prefix + "waves/" + fileName, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(FORMAT)
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        self.addFileToList(fileName)
        self.syncToFile()
    
    
    def addFileToList(self,fileName,dirFile=""):
        """ Ajoute un fichier à la liste des fichiers gérés par la base de données 
            Paramètres : 
                @fileName : nom du fichier dans le dossier storage 
        """
        if len(dirFile) == 0:
            dirFile = "storage"
        if os.access(Db.prefix + dirFile + "/" + fileName,os.F_OK):
            if not fileName in self.filesList:
                self.filesList.append(fileName)
                self.syncToFile()
                print "L'insertion du fichier a bien été effectuée"
            else:
                print "Le fichier est déjà dans la bibliothèque"
        else:
            print "Le fichier n'existe pas"
            
            
            
    def putDatasIntoFile(self,datas,fileName,dirFile=""):
        """ 
            Ajoute un jeu de données 
            Paramètres :
                @datas : a besoin d'implémenter la méthode __getstate__ ou d'être un tel type 
                @fileName : nom du fichier 
                @dirFile : ajoute une différence de stockage entre les types de fichiers
        """
        if len(dirFile) == 0:
            dirFile = "storage"
        try:
            with open(Db.prefix + dirFile + "/" + fileName,"w") as f:
                pickle.Pickler(f).dump(datas)
            self.addFileToList(fileName)
            self.syncToFile()
        except IOError:
            raise Exception("La lecture de fichier a échoué")
    
    
    
    def deleteFileFromList(self,fileName,dirFile=""):
        """ Supprime un fichier de la liste des fichiers gérés par la base de données SANS supprimer le fichier physique
            Paramètres : 
                @fileName : nom du fichier dans le dossier storage 
        """
        if len(dirFile) == 0:
            dirFile = "storage"
        if os.access(Db.prefix + dirFile + "/" + fileName,os.F_OK) and fileName in self.filesList:
            self.filesList.remove(fileName)
            self.syncToFile()
            print "La suppression du fichier a bien été effectuée"
        else:
            print "Le fichier n'existe pas ou n'est pas géré par la base de données"
    
    
    
    def syncToFile(self):
        """ Met le fichier de stockage de la liste des fichiers à jour """
        try:
            with open(Db.prefix + Db.filesListName + ".txt","w") as f:
                pickle.Pickler(f).dump(self.filesList)
        except IOError:
            raise Exception("Le fichier n'existe pas")
    
    
    
    def reset(force=False):
        """ Reset la liste des fichiers """
        if force or int(input("Êtes-vous sûr de vouloir réinitialiser la liste des fichiers ? (Oui = 0/Non = 1)")) == 0:
            with open(Db.prefix + Db.filesListName + ".txt","w") as f:
                c = pickle.Pickler(f)
                c.dump([])
            print "Réinitialisation réussie pour les fichiers"
    reset = staticmethod(reset)
    
    def toString(self):
        print self.filesList


if __name__ == "__main__":
    db = Db()
    db.addFileToList("test.txt")
    db.getFile("test.txt")
    db.toString()
