#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Graphical User Interface for the isolated word recognition project
Made for the MIG SE team s
"""
from speechserver.clientAuth import *

from Tkinter import *
from core.recording.recorder import recorder
from core.recording.sync import syncFile, cutBeginning, sox_handling
from core.utils.db import Db
from core.utils.constantes import NB_ITERATIONS
from shell import handlingRecording
from core.hmm.markov import buildHMMs, saveHMMs

class Gui:
    def __init__(self):
        self.auth = AuthUser()
        #self.auth.logIn("giliam", self.auth.hashPass("test"))
        self.nbEnregistrement = 0
        self.listeEnregistrements = []
        self.db = Db("../db/")
        self.fenetre3enabled = False
        self.noiseOk = False
    
    def ouverture(self):         #fonction qui ouvre une deuxieme fenetre graphique, et qui affiche le resultat
        self.fenetre4=Tk()
        self.fenetre4.attributes('-alpha', 1) #plein ecran
        self.fenetre4.configure(background='white')
        self.fenetre4.title("MIG SE 2013 - Liste des mots enregistres")
        titre=Label(self.fenetre4, text='\nMIG SE 2013',font=("DIN", "34","bold"), fg='#006eb8', bg="#ffffff")
        titre.pack()
        titre_logiciel=Label(self.fenetre4, text="Reconnaissance vocale\n\n\n\n",font =("DIN", "22"), bg="#ffffff")
        titre_logiciel.pack()
          
        panneau2=Label(self.fenetre4, text='Liste des mots actuellements reconnus :\n\n', font=("DIN", '14'), bg="#ffffff")
        hmmList = self.db.getFile("hmmList.txt")
        res = hmmList.keys()
        resultat=Label(self.fenetre4, text="\n".join(res),font =("DIN", "28", "bold"), fg="#16d924", bg="#ffffff")
        espace=Label(self.fenetre4, text="\n \n", bg="#ffffff")
        panneau2.pack()
        resultat.pack()
        espace.pack()
        bouton_fermer=Button(self.fenetre4,text='Quitter', command=self.fenetre4.destroy)
        bouton_fermer.pack()
        espace4=Label(self.fenetre4, text= ' \n ', bg="#ffffff")
        espace4.pack()
        self.fenetre4.mainloop()
        
    def creationHmm(self):
        self.bouton_enr.config(text="Terminer l'enregistrement du HMM", command=self.fenetre3.destroy)
        self.noiseOk = False
        listVectors = []
        for l in self.listeEnregistrements:
            content = self.db.getWaveFile(l)
            content,log = handlingRecording(content[1],self.db,0,0,0)
            listVectors.append(content)
        hmmList = self.db.getFile("hmmList.txt")
        if hmmList.get(self.mot):
            hmmList[self.mot].append("client_" + self.mot + ".txt")
        else:
            hmmList[self.mot] = ["client_" + self.mot + ".txt"]
        self.db.addFile( "hmmList.txt",hmmList )
        self.db.addFile( "client_" + self.mot + ".txt", listVectors, "hmm/" )
        buildHMMs(hmmList.keys(),hmmList.values(), 500, Db.prefixPath + "hmm/")
        saveHMMs(Db.prefixPath + "hmm/save.hmm")

    def enregistrer(self):
        if self.nbEnregistrement == 0:
            self.mot = self.saisirMot.get()
        if not self.noiseOk:
            self.errorMessage3.set("Vous n'avez pas encore enregistre le bruit !")
        elif self.mot == "":
            self.errorMessage3.set("Entrez un mot")
        else:
            self.errorMessage3.set("")
            fileName = recorder(self.db,"tmp",1,False,1,confirm=False,fileName=self.mot + "_" + str( self.nbEnregistrement ) )
            sox_handling(Db.prefixPath + "waves/tmp/" + self.mot + "_" + str(self.nbEnregistrement) + ".wav", Db.prefixPath + "waves/noise/" + self.mot + ".wav", Db.prefixPath + "waves/tmp/" )
            cutBeginning(Db.prefixPath + "waves/tmp/", self.mot + "_" + str(self.nbEnregistrement) + ".wav", "cut_")
            syncFile(Db.prefixPath + "waves/tmp/", self.mot + "_" + str(self.nbEnregistrement) + ".wav", "sync_")
            self.listeEnregistrements.append("tmp/" + self.mot + "_" + str(self.nbEnregistrement) + ".wav")
            self.nbEnregistrement += 1
            self.bouton_enr.config(text="Lancer l'enregistrement numero " + str(self.nbEnregistrement + 1) )
            if self.nbEnregistrement == NB_ITERATIONS:
                self.creationHmm()
                
    
    def enregistrerNoise(self):
        self.mot = self.saisirMot.get()
        if self.mot == "":
            self.errorMessage3.set("Entrez un mot")
        else:
            self.errorMessage3.set("")
            fileName = recorder(self.db,"noise",1,False,1,confirm=False,fileName=self.mot )
            self.noiseOk = True
    
    def loginAuth(self):
        loginIn = self.loginC.get()
        passwordIn = self.passwordC.get()
        if passwordIn == "" or loginIn == "":
            self.errorMessage.set("Il manque le pseudonyme ou le mot de passe !\n")
        else:
            self.auth.logIn(loginIn, self.auth.hashPass(passwordIn) )
            self.fenetre2.destroy()
            self.bouton_loginpopup.config(text='Se deconnecter')
            self.errorMessage.set("")
            Button(self.fenetre1,text='Liste des mots enregistres', command=self.ouverture).pack()
            self.displayRecorder()
            
    def registerAuth(self):
        loginIn = self.loginR.get()
        passwordIn = self.passwordR.get()
        if passwordIn == "" or loginIn == "":
            self.errorMessage.set("Il manque le pseudonyme ou le mot de passe !\n")
        else:
            if self.auth.getClient(loginIn) != "":
                self.auth.newClient(loginIn, self.auth.hashPass(passwordIn), [])
                self.errorMessage.set("Vous etes bien enregistre(e)\n")
            else:
                self.errorMessage.set("Le pseudonyme est deja utilise")
    
    def fenetre3destroy(self):
        self.fenetre3enabled = False
        self.fenetre3.destroy()
    
    def displayRecorder(self):
        self.bouton_registerIn.pack()
        if not self.fenetre3enabled:
            self.fenetre3=Tk()
            self.fenetre3.attributes('-alpha', 1) #plein ecran
            self.fenetre3.configure(background='white')
            self.fenetre3.title("MIG SE 2013 - Enregistrement")
            titre=Label(self.fenetre3, text='\nMIG SE 2013',font =("DIN", "34","bold"), fg='#006eb8',bg='#ffffff')
            titre.pack()
            titre_logiciel=Label(self.fenetre3, text="Reconnaissance vocale\n\n\n\n",font =("DIN", "22"),bg='#ffffff')
            titre_logiciel.pack()
            self.errorMessage3 = StringVar(self.fenetre3)
            
            errorLegend=Label(self.fenetre3, textvariable=self.errorMessage3, fg='#B80002',bg='#ffffff')
            errorLegend.pack()
            
            demande_mot=Label(self.fenetre3, text="Entrez le mot que vous souhaitez enregistrer", font=("DIN", '14'),bg='#ffffff')
            demande_mot.pack()
            self.saisirMot=StringVar(self.fenetre3)          # variable pour recevoir le texte saisi
            saisieMot=Entry(self.fenetre3, textvariable=self.saisirMot, width=30,bg='#ffffff')
            saisieMot.pack()
            Label(self.fenetre3, text="Avant de proceder aux enregistrements necessaires, il convient d'enregistrer\
 du bruit pour permettre efficacement le traitement du signal \n", font=("DIN", '14'),bg='#ffffff').pack()
            self.bouton_bruit=Button(self.fenetre3, text='Enregistrer du bruit', command=self.enregistrerNoise, fg='#ff0000')  #bouton qui enregistre et ouvre une nouvelle fenetre
            self.bouton_bruit.pack()
            Label(self.fenetre3, text="Il est necessaire pour creer un modele de Markov cache de proceder a une dizaine d'enregistrements du meme mot\n\
 Vous aurez deux secondes a chaque enregistrement pour prononcer votre mot une fois l'acquisition lancee\n", font=("DIN", '14'),bg='#ffffff').pack()
            espace1=Label(self.fenetre3, text= ' \n ',bg='#ffffff')
            espace1.pack()
            self.bouton_enr=Button(self.fenetre3, text='Lancer l\'enregistrement numero 1', command=self.enregistrer, fg='#ff0000')  #bouton qui enregistre et ouvre une nouvelle fenetre
            self.bouton_enr.pack()
            bouton_fermer=Button(self.fenetre3,text='Quitter', command=self.fenetre3destroy)
            bouton_fermer.pack()
            espace4=Label(self.fenetre3, text= ' \n ',bg='#ffffff')
            espace4.pack()
            self.fenetre3enabled = True

    def displayLogIn(self):
        
        if self.auth.connected:
            self.auth.logOut()
            self.bouton_loginpopup.config(text='Se connecter / S\'inscrire')
        else:
            self.fenetre2 = Tk()
            self.fenetre2.title("MIG SE 2013")
            self.fenetre2.attributes('-alpha', 1)
            self.fenetre2.configure(background='white')
            
            self.loginC = StringVar(self.fenetre2)
            self.passwordC = StringVar(self.fenetre2)
            self.loginR = StringVar(self.fenetre2)
            self.passwordR = StringVar(self.fenetre2)
            self.errorMessage = StringVar(self.fenetre2)
            
            errorLegend=Label(self.fenetre2, textvariable=self.errorMessage, fg='#B80002',bg='#ffffff')
            errorLegend.pack()
            Label(self.fenetre2, text="\nSe connecter \n", font=("DIN", '14'),bg='#ffffff').pack()
            
            loginLabel=Label(self.fenetre2, text="Identifiant :", font=("DIN", '14'),bg='#ffffff')
            loginLabel.pack()
            loginForm=Entry(self.fenetre2, textvariable=self.loginC, width=30)
            loginForm.pack()

            passwordLabel=Label(self.fenetre2, text="\nMot de passe :", font=("DIN", '14'),bg='#ffffff')
            passwordLabel.pack()
            passwordForm=Entry(self.fenetre2, textvariable=self.passwordC, width=30)
            passwordForm.pack()

            bouton_envoyer=Button(self.fenetre2, text='Se connecter', command=self.loginAuth, fg='#000000')
            bouton_envoyer.pack()
            
            Label(self.fenetre2, text="\nS'inscrire \n", font=("DIN", '14'),bg='#ffffff').pack()
            
            loginRegisterLabel=Label(self.fenetre2, text="Identifiant : ", font=("DIN", '14'),bg='#ffffff')
            loginRegisterLabel.pack()
            loginRegisterForm=Entry(self.fenetre2, textvariable=self.loginR, width=30)
            loginRegisterForm.pack()

            passwordRegisterLabel=Label(self.fenetre2, text="\nMot de passe :", font=("DIN", '14'),bg='#ffffff')
            passwordRegisterLabel.pack()
            passwordRegisterForm=Entry(self.fenetre2, textvariable=self.passwordR, width=30)
            passwordRegisterForm.pack()

            bouton_envoyer=Button(self.fenetre2, text='S\'inscrire', command=self.registerAuth, fg='#000000')
            bouton_envoyer.pack()
    
    def main(self):
        self.fenetre1=Tk()
        self.fenetre1.title("MIG SE 2013")
        self.fenetre1.attributes('-zoomed', 1)
        self.fenetre1.configure(background='white')
        titre=Label(self.fenetre1, text="\nMIG SE 2013",font =("DIN", "34","bold"), fg='#006eb8',bg='#ffffff')
        titre.pack()
        titre_logiciel=Label(self.fenetre1, text="Reconnaissance vocale\n",font =("DIN", "22"),bg='#ffffff')
        titre_logiciel.pack()
        
        if not self.auth.connected:
            self.bouton_loginpopup=Button(self.fenetre1,text="Se connecter / S'inscrire", command=self.displayLogIn)
            self.bouton_loginpopup.pack()
            self.bouton_registerIn=Button(self.fenetre1,text="Enregistrer", command=self.displayRecorder)
        else:
            self.bouton_loginpopup=Button(self.fenetre1,text="Se deconnecter", command=self.displayLogIn)
            self.bouton_loginpopup.pack()
            self.bouton_registerIn=Button(self.fenetre1,text="Enregistrer", command=self.displayRecorder)
            self.displayRecorder()
            Button(self.fenetre1,text='Liste des mots enregistres', command=self.ouverture).pack()

        bouton_fermer1=Button(self.fenetre1,text='Quitter', command=self.fenetre1.destroy)
        bouton_fermer1.pack()
        
        self.recorderlabel=Label(self.fenetre1,bg='#ffffff')
        self.recorderlabel.pack()
        espace3=Label(self.fenetre1, text= ' \n  ',bg='#ffffff')
        espace3.pack()
        photo=PhotoImage(file="speechapp/img/logomigSE.gif")    #insertion de l'image
        labl = Label(self.fenetre1, image=photo,bg='#ffffff')
        labl.pack()
        self.fenetre1.mainloop()
        self.fenetre3.mainloop()
gui = Gui()
gui.main()
