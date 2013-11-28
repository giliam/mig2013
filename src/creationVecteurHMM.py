from constantes import TAILLE_FINALE_MFCC

D = TAILLE_FINALE_MFCC

#tabMel = [[(i+1)*(k+1) for i in range(D)] for k in range(3)] #liste des tableaux de mel de l'echantillon sonore

#print tabMel

def creeVecteur(tabMel, energyTable):
	choice = -1
	output = [[0 for i in range(D)] for k in range(len(tabMel))]
	for t in range(len(tabMel)):
		output[t] = tabMel[t][0:D]
		output[t][D-1] = energyTable[t]
	while( not choice in range(2) ):
		try:
			choice = 1
			#choice = int( input( "Voulez-vous incorporer les differences premieres ? \n 0 : non   1 : oui : " )) 
		except NameError:
			print "Choix non valable"
		if (choice == 1):
			delta = [[0 for k in range(D-1)] for i in range(len(tabMel))]
			choice = -1
			for t in range(1,len(tabMel)):
				for k in range(D-1):
					delta[t][k] = output[t][k]-output[t-1][k]
			for t in range(1, len(tabMel)):
				for k in range(D-1):
					output[t][k] += delta[t][k]
			#print "output :"
			#print output
			#print "delta :"
			#print delta
			while( not choice in range(2) ):
				try:
					choice = 1
					#choice = int( input( "Voulez-vous incorporer les differences secondes ? \n 0 : non   1 : oui " ) )
				except NameError:
					print "Choix non valable"
				if (choice == 1):
					for t in range(1,len(tabMel)):
						for k in range(D-1):
							output[t][k] += delta[t][k]-delta[t-1][k]
				break
		break
	return output
#print(creeVecteur(tabMel))			
