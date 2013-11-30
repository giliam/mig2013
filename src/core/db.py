#!/usr/bin/python
# -*-coding:utf-8 -*
import os
import pickle
import scipy.io.wavfile
import wave
from numpy import int16

""" Instancie la base de données """
class Db:
    """ Créé un gestionnaire de fichiers pour stocker les HMM 
        Attributs :
            -> filesList : liste des fichiers gérés par la base de données """
            
    filesListName = "filesList"
    prefix = ""
    verbose = False
    
    def __init__(self, prefix = "", verbose = False, filesListName = "filesList"):
        """ Constructeur """
        Db.prefix = prefix
        Db.filesListName = filesListName
        Db.verbose = verbose
        self.log = ""
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
                if dirFile == "waves":
                    content = scipy.io.wavfile.read(Db.prefix + dirFile + "/" + fileName)
                    return content
                elif fileName in self.filesList:
                    with open(Db.prefix + dirFile + "/" + fileName,"r") as f:
                        content = pickle.Unpickler(f).load()
                    return content
            except IOError:
                raise Exception("La lecture de fichier a échoué")
        else:
            self.addLog("le fichier n'est pas géré pas la base de données")
            return ""


    
    
    def getWaveFile(self,fileName):
        """ Alias de getFile pour les Wave """
        return self.getFile(fileName,"waves")
    
    
    
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
        
        self.addFileToList(fileName,"waves")
        self.syncToFile()
        
        
    
    def addWaveFromAmp(self,fileName,freq,amp,dirName="waves/",addToList=True):
        scipy.io.wavfile.write(Db.prefix + dirName + fileName, freq, int16(amp))
        if addToList:
            self.addFileToList(fileName,"waves")
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
                self.addLog("L'insertion du fichier a bien été effectuée")
            else:
                self.addLog("Le fichier est déjà dans la bibliothèque")
        else:
            self.addLog("Le fichier n'existe pas")
            
            
    
    def addFile(self,fileName,content,dirFile=""):
        """ Ajoute un fichier à la liste des fichiers gérés par la base de données 
            Paramètres : 
                @fileName : nom du fichier dans le dossier storage 
        """
        if len(dirFile) == 0:
            dirFile = "storage"
        with open(Db.prefix + dirFile + "/" + fileName,"w") as f:
            pickle.Pickler(f).dump(content)
        self.addFileToList(fileName)
            
    
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
            self.addLog("La lecture de fichier a échoué")
            return False
    
    
    
    def deleteFileFromList(self,fileName,dirFile=""):
        """ Supprime un fichier de la liste des fichiers gérés par la base de données SANS supprimer le fichier physique
            Paramètres : 
                @fileName : nom du fichier dans le dossier storage 
        """
        if len(dirFile) == 0:
            dirFile = "storage"
        if fileName in self.filesList:
            self.filesList.remove(fileName)
            try:
                dirName = os.path.dirname(fileName)
                if os.access(Db.prefix + dirFile + "/" + fileName,os.F_OK):
                    os.remove(Db.prefix + dirFile + "/" + fileName)
                    self.addLog("Le fichier a bien été supprimé")
                else:
                    self.addLog("Le fichier n'existe pas")
            except OSError:
                self.addLog("La suppression a échoué")
            try:
                os.rmdir(Db.prefix + dirFile + "/" + dirName)
                self.addLog("Le dossier a bien été supprimé")
            except OSError:
                pass
            self.syncToFile()
            self.addLog("La suppression du fichier a bien été effectuée")
        else:
            self.addLog("Le fichier n'existe pas ou n'est pas géré par la base de données")
    
    
    
    def syncToFile(self):
        """ Met le fichier de stockage de la liste des fichiers à jour """
        try:
            with open(Db.prefix + Db.filesListName + ".txt","w") as f:
                pickle.Pickler(f).dump(self.filesList)
        except IOError:
            raise Exception("Le fichier n'existe pas")
    
    
    def sync(self, dirName = "", dirIni = "storage/"):
        """ Met le fichier de stockage de la liste des fichiers à jour en parcourant toute l'arborescence """
        for f in os.listdir(Db.prefix + dirIni + dirName):
            if os.path.isfile(os.path.join(Db.prefix + dirIni + dirName, f)):
                self.addFileToList(os.path.join(dirName, f),dirIni)
            else:
                self.sync(dirName + f + "/",dirIni)
    
    
    def reset(force=False):
        """ Reset la liste des fichiers """
        if force or int(input("Êtes-vous sûr de vouloir réinitialiser la liste des fichiers ? (Oui = 0/Non = 1)")) == 0:
            with open(Db.prefix + Db.filesListName + ".txt","w") as f:
                c = pickle.Pickler(f)
                c.dump([])
            print "Réinitialisation réussie pour les fichiers"
    reset = staticmethod(reset)
    
    
    
    
    def printFilesList(self,dirName="",printBool=True,*extRequired):
        """ Affiche la liste des fichiers gérés par la base de données
                Paramètres :
                    @*extRequired = "all" : envoie l'extension des fichiers à afficher sous forme de tuples de noms d'extensions 
                                                exemple : .wav, .txt """
        filesListExt = []
        for k,f in enumerate(self.filesList):
            #On récupère l'extension du fichier parcouru
            a,ext = os.path.splitext(f)
            d = os.path.dirname(f)
            if (dirName == "" or d == dirName ) and (ext in extRequired or len(extRequired) == 0):
                if printBool:
                    print k, " - ", f
                filesListExt.append(f)
        return filesListExt
    
    
    def printDirFiles(self,dirName="storage/"):
        """ Affiche la liste des dossiers dans un des sous-dossiers de stockage
                Paramètres :
                    @dirName = "storage/" : dossier qu'on parcourra """
        dirListExt = []
        l = os.listdir(Db.prefix + dirName)
        for k,f in enumerate(l):
            #On récupère l'extension du fichier parcouru
            print k, " - ", f
        return l
    
    def toString(self):
        print self.filesList
        
    def addLog(self,s,fileName=""):
        if Db.verbose:
            print s
        self.log += "\n" + s
        #self.addFile("dblog" + fileName + ".txt",self.log,"logs/")
        
    def logDump(self,fileName,log=""):
        if log == "":
            name = "dblog"
            log = self.log
        else:
            name = "handlinglog"
        self.addFile(name + fileName + ".txt",log,"logs/")
    
if __name__ == "__main__":
    db = Db()
    db.addFileToList("test.txt")
    db.getFile("test.txt")
    db.toString()
