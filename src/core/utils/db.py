#!/usr/bin/python
# -*-coding:utf-8 -*
import os
import pickle
import scipy.io.wavfile
import wave
from numpy import int16

class Db:
    """ Files manager to store .wav and hmm
        Attributes :
            -> filesList : name of the file containing the list of files stored """
            
    filesListName = "filesList"
    prefixPath = ""
    verbose = False
    
    def __init__(self, prefixPath = "", verbose = False, filesListName = "filesList"):
        """ Constructor which needs prefix of the directory which contains (or will contain) the stored files """
        Db.prefixPath = prefixPath
        Db.filesListName = filesListName
        Db.verbose = verbose
        self.log = ""
        try:
            with open(Db.prefixPath + Db.filesListName + ".txt","r") as f:
                self.filesList = pickle.Unpickler(f).load()
        except IOError:
            Db.reset(True)
            raise Exception("L'instanciation a été annulée car le fichier de gestion de la base de données n'existe pas")



    def getFile(self,fileName,dirFile=""):
        """ Add a file to the list of files handled par the database system
            Parameters : 
                @fileName : name of the file in the storage directory prefixed by dirFile
                @dirFile : add a prefix to files and give others handling available
        """
        if len(dirFile) == 0:
            dirFile = "storage"
        if fileName in self.filesList:
            try:
                if dirFile == "waves":
                    content = scipy.io.wavfile.read(Db.prefixPath + dirFile + "/" + fileName)
                    return content
                elif fileName in self.filesList:
                    with open(Db.prefixPath + dirFile + "/" + fileName,"r") as f:
                        content = pickle.Unpickler(f).load()
                    return content
            except IOError:
                raise Exception("La lecture de fichier a échoué")
        else:
            self.addLog("le fichier n'est pas géré pas la base de données")
            return ""


    
    
    def getWaveFile(self,fileName):
        """ Alias of getFile for .wav """
        return self.getFile(fileName,"waves")
    
    
    
    def addWave(self,fileName,CHANNELS,FORMAT,RATE,frames,p):
        if os.access(Db.prefixPath + "waves/" + fileName,os.F_OK):
            pass
            #Il faudrait rajouter la gestion de l'existence de deux mêmes fichiers
        dirName = os.path.dirname(fileName)
        if not os.access(Db.prefixPath + "waves/" + dirName,os.F_OK):
            os.mkdir(Db.prefixPath + "waves/" + dirName)
        wf = wave.open(Db.prefixPath + "waves/" + fileName, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(FORMAT)
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        self.addFileToList(fileName,"waves")
        self.syncToFile()
        
        
    
    def addWaveFromAmp(self,fileName,freq,amp,dirName="waves/",addToList=True):
        scipy.io.wavfile.write(Db.prefixPath + dirName + fileName, freq, int16(amp))
        if addToList:
            self.addFileToList(fileName,"waves")
            self.syncToFile()
    
    
    def addFileToList(self,fileName,dirFile=""):
        """ Add a file to the list. Needs that the file already exists
            Parameters : 
                @fileName : name of the file in the storage directory prefixed by dirFile
                @dirFile : prefix of the file
        """
        if len(dirFile) == 0:
            dirFile = "storage"
        if os.access(Db.prefixPath + dirFile + "/" + fileName,os.F_OK):
            if not fileName in self.filesList:
                self.filesList.append(fileName)
                self.syncToFile()
                self.addLog("L'insertion du fichier a bien été effectuée")
            else:
                self.addLog("Le fichier est déjà dans la bibliothèque")
        else:
            self.addLog("Le fichier n'existe pas")
            
            
    
    def addFile(self,fileName,content,dirFile=""):
        """ Add a file to the list and to the storage directory
            Parameters :
                @fileName : name of the file in the storage directory prefixed by dirFile
                @content : the content to pickle in the file 
                @dirFile : prefix of the file
        """
        if len(dirFile) == 0:
            dirFile = "storage"
        with open(Db.prefixPath + dirFile + "/" + fileName,"w") as f:
            pickle.Pickler(f).dump(content)
        self.addFileToList(fileName)
            
    
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
                if os.access(Db.prefixPath + dirFile + "/" + fileName,os.F_OK):
                    os.remove(Db.prefixPath + dirFile + "/" + fileName)
                    self.addLog("Le fichier a bien été supprimé")
                else:
                    self.addLog("Le fichier n'existe pas")
            except OSError:
                self.addLog("La suppression a échoué")
            try:
                os.rmdir(Db.prefixPath + dirFile + "/" + dirName)
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
            with open(Db.prefixPath + Db.filesListName + ".txt","w") as f:
                pickle.Pickler(f).dump(self.filesList)
        except IOError:
            raise Exception("Le fichier n'existe pas")
    
    
    def sync(self, dirName = "", dirIni = "storage/"):
        """ Met le fichier de stockage de la liste des fichiers à jour en parcourant toute l'arborescence """
        for f in os.listdir(Db.prefixPath + dirIni + dirName):
            if os.path.isfile(os.path.join(Db.prefixPath + dirIni + dirName, f)):
                self.addFileToList(os.path.join(dirName, f),dirIni)
            else:
                self.sync(dirName + f + "/",dirIni)
    
    
    def reset(force=False):
        """ Reset la liste des fichiers """
        if force or int(input("Êtes-vous sûr de vouloir réinitialiser la liste des fichiers ? (Oui = 0/Non = 1)")) == 0:
            with open(Db.prefixPath + Db.filesListName + ".txt","w") as f:
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
        l = os.listdir(Db.prefixPath + dirName)
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
