#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Graphical User Interface for the isolated word recognition project
Made for the MIG SE team s
"""

from Tkinter import *
#from recording.recorder import recorder
#from utils.db import Db
#from main import main




def result(amp):             #fonction principale qui renvoie le mot reconnu
    return 'Cheval'

def ouverture(amp):         #fonction qui ouvre une deuxième fenêtre graphique, et qui affiche le résultat
    fenetre2=Tk()
    fenetre2.attributes('-fullscreen', 1) #plein écran
    
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
    

def enregistrer():
    db = Db("../../db/",verbose=False)
    fileName = recorder(db,"tmp",1,False,saisir.get())
    freq,amp = db.getWaveFile("tmp/" + fileName + ".wav")
    ouverture(amp)
    
def loginAuth():
    
    loginIn = login.get()
    passwordIn = password.get()
    if passwordIn == "" or loginIn == "":
        errorLabel.set('Erreur !')
    else:
        



fenetre1=Tk()
fenetre1.attributes('-fullscreen', 1)
fenetre1.configure(background='white')
titre=Label(fenetre1, text='MIG SE 2013',font =("DIN", "34","bold"), fg='#006eb8',bg='#ffffff')
titre.pack()
titre_logiciel=Label(fenetre1, text="Reconnaissance vocale\n\n",font =("DIN", "22"),bg='#ffffff')
titre_logiciel.pack()

errorLabel=Label(fenetre1, text="", font=("DIN", '14'))
errorLabel.pack()

loginLabel=Label(fenetre1, text="Identifiant : \n", font=("DIN", '14'),bg='#ffffff')
loginLabel.pack()
login = StringVar()
loginForm=Entry(textvariable=login, width=30)
loginForm.pack()

passwordLabel=Label(fenetre1, text="Mot de passe : \n", font=("DIN", '14'),bg='#ffffff')
passwordLabel.pack()
password = StringVar()
passwordForm=Entry(textvariable=password, width=30)
passwordForm.pack()

bouton_envoyer=Button(fenetre1, text='Se connecter', command=loginAuth, fg='#000000')
bouton_envoyer.pack()

demande_temps=Label(fenetre1, text="Combien de temps voulez-vous enregister ? (En s)\n", font=("DIN", '14'),bg='#ffffff')
demande_temps.pack()
saisir=StringVar()          # variable pour recevoir le texte saisi
saisie=Entry(textvariable=saisir, width=30)
saisie.pack()
espace1=Label(fenetre1, text= ' \n ',bg='#ffffff')
espace1.pack()
bouton_enr=Button(fenetre1, text='Enregistrer', command=enregistrer, fg='#ff0000')  #bouton qui enregistre et ouvre une nouvelle fenetre
bouton_enr.pack()
bouton_fermer1=Button(fenetre1,text='Quitter', command=fenetre1.quit)
bouton_fermer1.pack()
espace3=Label(fenetre1, text= ' \n  ',bg='#ffffff')
espace3.pack()
photo=PhotoImage(file="LOGO.gif")    #insertion de l'image
labl = Label(fenetre1, image=photo,bg='#ffffff')
labl.pack()
fenetre1.mainloop()
#print saisir.get()


