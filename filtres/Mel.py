from math import *
from numpy import *

#Creation de Mel. Axel
#Description : on est dans le domaine frequentiel. On prend en entrer la liste amplitude-freq. on renvoit une nouvelle liste tq liste(g(f))=amp(f) (on affecte les amplitudes a des nouvelles frequences)

def fct_mel(list):
	# on conservre les memes valeurs d'amplitudes. on les affecte a des indices differents selon la formule de mel.
	N=len(list)
	N1=int(2595.0*log(1.0+(N-1.0)/700.0))+1
	list1=zeros(N1,float) #N1 est la valeur maximale de la frequence apres modification par mel.
	for i in range(N1):
		list1[i]=-1.
	for i in range(N):
		list1[int(2595.0*log(1+i/700.0))]=list[i]
		# on affecte les amplitudes de f a mel de f
	if list1[0]==-1.:
		i=0
		while list1[i]==-1.:
			i=i+1
		list1[0]=list1[i]
	#on vient de mettre le premier indice a une valeur non egale a -1
	#le dernier indice est necessairement egale
	i=0
	while list1[N1-i-1]==-1.:
		i=i+1
	N1=N1-i
	list2=zeros(N1,float)
	for i in range(N1):
		list2[i]=list1[i]
	#maintenant les deux bornes sont differentes de -1. On va remplir les amplitudes interieures
	for i in range (1,N1-1):
		if list2[i]==-1:
			j=1
			k=1
			while list2[i+j]==-1:
				j=j+1
			while list2[i-k]==-1:
				k=k+1
			list2[i]=((list2[i-1]+(list2[i+j]-list2[i-k])/(j+k))) #remplissage des cases vides de maniere affine
	#toutes les amplitudes sont differentes de -1.
	return(list2)


	
	
def fct_mel_pas(list,pas):
	# on conservre les memes valeurs d'amplitudes. on les affecte a des indices differents selon la formule de mel.
	N=len(list)
	N1=int(((2595.0*log(1.0+((N-1.0)*pas)/700.0))+1)/pas)+1
	list1=zeros(N1,float) #N1 est la valeur maximale de la frequence apres modification par mel.
	for i in range(N1):
		list1[i]=-1.
	for i in range(N):
		amp=list[i]
		f=i*pas
		mf=int(2595.0*log(1+f/700.0))
		mi=int(mf/pas)
		list1[mi]=amp
		# on affecte les amplitudes de f a mel de f
	if list1[0]==-1.:
		i=0
		while list1[i]==-1.:
			i=i+1
		list1[0]=list1[i]
	#on vient de mettre le premier indice a une valeur non egale a -1
	#le dernier indice est necessairement egale
	i=0
	while list1[N1-i-1]==-1.:
		i=i+1
	N1=N1-i
	list2=zeros(N1,float)
	for i in range(N1):
		list2[i]=list1[i]
	#maintenant les deux bornes sont differentes de -1. On va remplir les amplitudes interieures
	for i in range (1,N1-1):
		if list2[i]==-1:
			j=1
			k=1
			while list2[i+j]==-1:
				j=j+1
			while list2[i-k]==-1:
				k=k+1
			list2[i]=((list2[i-1]+(list2[i+j]-list2[i-k])/(j+k))) #remplissage des cases vides de maniere affine
	#toutes les amplitudes sont differentes de -1.
	return(list2)

pas=0.01
l=zeros(50000,int)
for i in range(50000):
	l[i]=i*pas
list=fct_mel(l)
list2=fct_mel_pas(l,0.1)
print('<frequence transformee, frequence initiale>')
for i in range (0,len(l),100):
	print(list2[i],l[i])
