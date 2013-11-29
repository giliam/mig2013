
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 08:26:19 2013

@author: Mac
"""

from Tkinter import *
#from main import main

def result():             #fonction principale qui renvoie le mot reconnu
    return 'Cheval'

def ouverture():         #fonction qui ouvre une deuxième fenêtre graphique, et qui affiche le résultat
    #print saisir.get()
    fenetre2=Tk()
    fenetre2.attributes('-fullscreen', 1) #plein écran
    
    titre=Label(fenetre2, text='\nMIG SE 2013',font =("DIN", "34","bold"), fg='#006eb8')
    titre.pack()
    titre_logiciel=Label(fenetre2, text="Reconnaissance vocale\n\n\n\n",font =("DIN", "22"))
    titre_logiciel.pack()
      
    panneau2=Label(fenetre2, text='Résultat:\n\n', font=("DIN", '14'))
    res=result()
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
    #print saisir.get()
    ouverture()
    

fenetre1=Tk()
fenetre1.attributes('-fullscreen', 1)
fenetre1.configure(background='white')
titre=Label(fenetre1, text='MIG SE 2013',font =("DIN", "34","bold"), fg='#006eb8',bg='#ffffff')
titre.pack()
titre_logiciel=Label(fenetre1, text="Reconnaissance vocale\n\n",font =("DIN", "22"),bg='#ffffff')
titre_logiciel.pack()
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
