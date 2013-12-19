#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from math import *
from numpy import *

"""Creation de Mel. Axel
Description : on est dans le domaine frequentiel.
On prend en entrer la liste amplitude-freq.
on renvoit une nouvelle liste tq liste(g(f))=amp(f)
(on affecte les amplitudes a des nouvelles frequences)"""

# fonction integrant le pas de frequence
def fct_mel_pas(listMel,pas):
	""" on conserve les memes valeurs d'amplitudes. on les affecte a des indices differents selon la formule de mel. """
	N=len(listMel)
	N1=int(((2595.0*log10(1.0+((N-1.0)*pas)/700.0))+1)/pas)+1
	list1=zeros(N1,float) #N1 est la valeur maximale de la frequence apres modification par mel.
	for i in range(N1):
		list1[i] = -1.
	for i in range(N):
		amp=listMel[i]
		f=i*pas
		mf=int(2595.0*log10(1+f/700.0))
		mi=int(mf/pas)
		list1[mi]=amp
		# on affecte les amplitudes de f a mel de f
	if list1[0] == -1.:
		i = 0
		while list1[i] == -1.:
				i = i + 1
		list1[0] = list1[i]
	#on vient de mettre le premier indice a une valeur non egale a -1
	#le dernier indice est necessairement egale
	i = 0
	while list1[N1 - i - 1] == -1.:
		i = i + 1
	N1 = N1 - i
	list2 = zeros(N1, float)
	for i in range(N1):
		list2[i] = list1[i]
	#maintenant les deux bornes sont differentes de -1. On va remplir les amplitudes interieures
	for i in range (1, N1 - 1):
		if list2[i] == -1:
			j = 1
			k = 1
			while list2[i + j] == -1:
					j = j + 1
			while list2[i - k] == -1:
					k = k + 1
			list2[i]=((list2[i - 1]+(list2[i + j]-list2[i - k])/(j + k))) #remplissage des cases vides de maniere affine
	#toutes les amplitudes sont differentes de -1.
	return(list2)


def tab_capture(listMel,pas,melbas,melhaut):
	""" somme les valeurs d'une liste entre deux indicies et renvoit le log """
	indbas=min(int(melbas/pas),len(listMel))
	indhaut=min(int(melhaut/pas),len(listMel))
	amp=0
	for i in range(indbas,indhaut):
		amp=listMel[i]+amp
	########################################################################
	##			DeBOGAGE DeGUEULASSE
	##			ATTENTION
	########################################################################
	return(log10(amp))
	
def mel_tab(listMel,pas):
	""" construction de la liste mel SANS FILTRE """
	list1=zeros(24,float)
	list1[0]=tab_capture(listMel,pas,0,325)
	list1[1]=tab_capture(listMel,pas,142,483)
	list1[2]=tab_capture(listMel,pas,325,622)
	list1[3]=tab_capture(listMel,pas,483,820)
	list1[4]=tab_capture(listMel,pas,622,958)
	list1[5]=tab_capture(listMel,pas,820,1136)
	list1[6]=tab_capture(listMel,pas,958,1290)
	list1[7]=tab_capture(listMel,pas,1136,1447)
	list1[8]=tab_capture(listMel,pas,1290,1603)
	list1[9]=tab_capture(listMel,pas,1447,1771)
	list1[10]=tab_capture(listMel,pas,1603,1932)
	list1[11]=tab_capture(listMel,pas,1771,2084)
	list1[12]=tab_capture(listMel,pas,1932,2249)
	list1[13]=tab_capture(listMel,pas,2084,2411)
	list1[14]=tab_capture(listMel,pas,2249,2569)
	list1[15]=tab_capture(listMel,pas,2411,2734)
	list1[16]=tab_capture(listMel,pas,2569,2889)
	list1[17]=tab_capture(listMel,pas,2734,3051)
	list1[18]=tab_capture(listMel,pas,2889,3210)
	list1[19]=tab_capture(listMel,pas,3051,3373)
	list1[20]=tab_capture(listMel,pas,3210,3535)
	list1[21]=tab_capture(listMel,pas,3373,3693)
	list1[22]=tab_capture(listMel,pas,3535,3855)
	list1[23]=tab_capture(listMel,pas,3693,4016)
	"""recherche du min fini du tableau"""
	noo=float("-infinity")
	min=noo
	for i in range(24):
		if list1[i] > float("-infinity"):
			if list1[i]>=min:
				min=list1[i]
	for i in range(24):
		if list1[i] > float("-infinity"):
			if list1[i]<=min:
				min=list1[i]
	""" remplacement de -inf par min/100.0"""
	for i in range(24):
		if list1[i]==float("-infinity"):
			list1[i]=min/100.
	return(list1)
        
#systeme de test
if __name__ == '__main__':
    pas = 10
    l = zeros(1000, float)
    for i in range(len(l)):
        l[44] = 10
    list2 = fct_mel_pas(l, pas)
    print('<frequence transformee, frequence initiale>')

    for i in range (0, len(list2)):
        print(list2[i], l[i])
	print(mel_tab(list2,pas))
