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
    
    def __init__(self, prefixPath = "", filesListName = "filesList", verbose = False):
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
            raise Exception("L'instanciation a ete annulee car le fichier de gestion de la base de donnees n'existe pas")



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
                raise Exception("La lecture de fichier a echoue")
        else:
            self.addLog("le fichier n'est pas gere pas la base de donnees")
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
                self.addLog("L'insertion du fichier a bien ete effectuee")
            else:
                self.addLog("Le fichier est dejà dans la bibliothèque")
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
        """ Remove a file from the list but does NOT remove the file from the disk
            Parameters : 
                @fileName : name of the file in the storage directory prefixed by dirFile
                @dirFile : prefix of the file
        """
        if len(dirFile) == 0:
            dirFile = "storage"
        if fileName in self.filesList:
            self.filesList.remove(fileName)
            try:
                dirName = os.path.dirname(fileName)
                if os.access(Db.prefixPath + dirFile + "/" + fileName,os.F_OK):
                    os.remove(Db.prefixPath + dirFile + "/" + fileName)
                    self.addLog("Le fichier a bien ete supprime")
                else:
                    self.addLog("Le fichier n'existe pas")
            except OSError:
                self.addLog("La suppression a echoue")
            try:
                os.rmdir(Db.prefixPath + dirFile + "/" + dirName)
                self.addLog("Le dossier a bien ete supprime")
            except OSError:
                pass
            self.syncToFile()
            self.addLog("La suppression du fichier a bien ete effectuee")
        else:
            self.addLog("Le fichier n'existe pas ou n'est pas gere par la base de donnees")
    
    
    
    def syncToFile(self):
        """ Synchronize the list of the files stored from the current attribute """
        try:
            with open(Db.prefixPath + Db.filesListName + ".txt","w") as f:
                pickle.Pickler(f).dump(self.filesList)
        except IOError:
            raise Exception("Le fichier n'existe pas")
    
    
    def recursiveSync(self, dirName = "", dirIni = "storage/"):
        """ Synchronize the list of the files stored by studying recursively the current tree """
        for f in os.listdir(Db.prefixPath + dirIni + dirName):
            if os.path.isfile(os.path.join(Db.prefixPath + dirIni + dirName, f)):
                self.addFileToList(os.path.join(dirName, f),dirIni)
            else:
                self.sync(dirName + f + "/",dirIni)

    def sync(self, dirName = "", dirIni = "storage/" ):
        #Delete files that don't exist anymore in the list
        for k,f in enumerate(self.filesList):
            if not os.access(Db.prefixPath + dirIni + f,os.F_OK) and not os.access(Db.prefixPath + "storage/" + f,os.F_OK):
                del self.filesList[k]
        self.addFile(Db.filesListName + ".txt", self.filesList)
        self.recursiveSync(dirName, dirIni)
    
    
    def reset(force=False):
        """ Reset the files list """
        msg = "etes-vous sur de vouloir reinitialiser la liste des fichiers ? (Oui = 0/Non = 1)"
        if force or int(input(msg)) == 0:
            with open(Db.prefixPath + Db.filesListName + ".txt","w") as f:
                c = pickle.Pickler(f)
                c.dump([])
            print "Reinitialisation reussie pour les fichiers"
    reset = staticmethod(reset)
    
    
    def syncHmm(self):
        hmmList = self.getFile("hmmList.txt")
        for k,f in hmmList.items():
            if not os.access(Db.prefixPath + "hmm/" + f,os.F_OK):
                del hmmList[k]
        self.addFile("hmmList.txt", hmmList)
    
    def printFilesList(self,dirName="",printBool=True,*extRequired):
        """ Display the files list
            Parameters:
                @dirName : a prefixed 
                @*extRequired : contains the extensions to display (e.g. <.wav, .txt>) """
        filesListExt = []
        n = 0
        for k,f in enumerate(self.filesList):
            #On recupère l'extension du fichier parcouru
            a,ext = os.path.splitext(f)
            d = os.path.dirname(f)
            if (dirName == "" or d == dirName ) and (len(extRequired) == 0 or ext in extRequired):
                if printBool:
                    print n, " - ", k, " - ", f
                    n += 1
                filesListExt.append(f)
        return filesListExt
    
    
    def printDirFiles(self,dirName="storage/"):
        """ Display the list of files in a directory
            Parameters :
                @dirName = "storage/" : directory to browse """
        dirListExt = []
        l = os.listdir(Db.prefixPath + dirName)
        for k,f in enumerate(l):
            #On recupère l'extension du fichier parcouru
            print k, " - ", f
        return l
    
    def __str__(self):
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
    print(db)
