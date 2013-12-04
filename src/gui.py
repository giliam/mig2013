#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Graphical User Interface for the isolated word recognition project
Made for the MIG SE team s
"""
from speechserver.clientAuth import *

from Tkinter import *
from core.recording.recorder import recorder
from core.utils.db import Db
from core.main import main


class Gui:
    def __init__(self):
        self.auth = AuthUser()
    
    def result(self, amp):             #fonction principale qui renvoie le mot reconnu
        return 'Cheval'

    def ouverture(self, amp):         #fonction qui ouvre une deuxième fenêtre graphique, et qui affiche le résultat
        fenetre2=Tk()
        fenetre2.attributes('-alpha', 1) #plein écran
        
        titre=Label(fenetre2, text='\nMIG SE 2013',font =("DIN", "34","bold"), fg='#006eb8')
        titre.pack()
        titre_logiciel=Label(fenetre2, text="Reconnaissance vocale\n\n\n\n",font =("DIN", "22"))
        titre_logiciel.pack()
          
        panneau2=Label(fenetre2, text='Résultat:\n\n', font=("DIN", '14'))
        res=result(amp)
        resultat=Label(fenetre2, text= res,font =("DIN", "28", "bold"), fg="#16d924")
        espace=Label(fenetre2, text="\n \n")
        panneau2.pack()
        resultat.pack()
        espace.pack()
        bouton_fermer=Button(fenetre2,text='Quitter', command=fenetre2.quit)
        bouton_fermer.pack()
        espace4=Label(fenetre2, text= ' \n ')
        espace4.pack()
        """pho=Label(fenetre2, text="Phonems rencontrés:", font=("DIN", '14'))
        pho.pack()
        photo1=PhotoImage(file="LOGO1.gif")    #insertion de l'image qui ne marche pas
        labl1 = Label(fenetre2, image=photo1)
        labl1.pack()"""
        fenetre2.mainloop()
        

    def enregistrer(self):
        db = Db("../db/",verbose=False)
        fileName = recorder(db,"tmp",1,False,saisir.get())
        freq,amp = db.getWaveFile("tmp/" + fileName + ".wav")
        ouverture(amp)
        
    def loginAuth(self):
        loginIn = self.loginC.get()
        passwordIn = self.passwordC.get()
        if passwordIn == "" or loginIn == "":
            self.errorMessage.set("Il manque le pseudonyme ou le mot de passe !\n")
        else:
            print self.auth.hashPass(passwordIn)
            self.auth.logIn(loginIn, self.auth.hashPass(passwordIn) )
            self.fenetre2.destroy()
            self.bouton_loginpopup.config(text='Se déconnecter')
            self.displayRecorder()
            
    def registerAuth(self):
        loginIn = self.loginR.get()
        passwordIn = self.passwordR.get()
        if passwordIn == "" or loginIn == "":
            self.errorMessage.set("Il manque le pseudonyme ou le mot de passe !\n")
        else:
            if self.auth.getClient(loginIn) != "":
                self.auth.newClient(loginIn, auth.hashPass(passwordIn), [])
                self.errorMessage.set("Vous êtes bien enregistré(e)\n")
            else:
                self.errorMessage.set("Le pseudonyme est déjà utilisé")

    def displayRecorder(self):
        self.fenetre3=Tk()
        self.fenetre3.attributes('-alpha', 1) #plein écran
        self.fenetre3.configure(background='white')
        titre=Label(self.fenetre3, text='\nMIG SE 2013',font =("DIN", "34","bold"), fg='#006eb8',bg='#ffffff')
        titre.pack()
        titre_logiciel=Label(self.fenetre3, text="Reconnaissance vocale\n\n\n\n",font =("DIN", "22"),bg='#ffffff')
        titre_logiciel.pack()
        demande_mot=Label(self.fenetre3, text="Entrez le mot que vous souhaitez enregistrer", font=("DIN", '14'),bg='#ffffff')
        demande_mot.pack()
        saisirMot=StringVar()          # variable pour recevoir le texte saisi
        saisieMot=Entry(self.fenetre3, textvariable=saisirMot, width=30,bg='#ffffff')
        saisieMot.pack()
        demande_temps=Label(self.fenetre3, text="Il est nécessaire pour créer un modèle de Markov caché de procéder à une dizaine d'enregistrements du même mot\n\
        Vous aurez deux secondes à chaque enregistrement pour prononcer votre mot une fois l'acquisition lancée\n", font=("DIN", '14'),bg='#ffffff')
        demande_temps.pack()
        saisir=StringVar()          # variable pour recevoir le texte saisi
        saisie=Entry(self.fenetre3, textvariable=saisir, width=30,bg='#ffffff')
        saisie.pack()
        espace1=Label(self.fenetre3, text= ' \n ',bg='#ffffff')
        espace1.pack()
        self.bouton_enr=Button(self.fenetre3, text='Lancer l\'enregistrement numéro 1', command=self.enregistrer, fg='#ff0000')  #bouton qui enregistre et ouvre une nouvelle fenetre
        self.bouton_enr.pack()
        bouton_fermer=Button(self.fenetre3,text='Quitter', command=self.fenetre3.destroy)
        bouton_fermer.pack()
        espace4=Label(self.fenetre3, text= ' \n ',bg='#ffffff')
        espace4.pack()
        self.fenetre3.mainloop()    

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
            
            errorLegend=Label(self.fenetre2, textvariable=self.errorMessage,bg='#ffffff')
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
        titre=Label(self.fenetre1, text='MIG SE 2013',font =("DIN", "34","bold"), fg='#006eb8',bg='#ffffff')
        titre.pack()
        titre_logiciel=Label(self.fenetre1, text="Reconnaissance vocale\n",font =("DIN", "22"),bg='#ffffff')
        titre_logiciel.pack()
        self.bouton_loginpopup=Button(self.fenetre1,text="Se connecter / S'inscrire", command=self.displayLogIn)
        self.bouton_loginpopup.pack()
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
        #print saisir.get()
gui = Gui()
gui.main()
