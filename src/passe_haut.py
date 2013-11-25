from math import *
from numpy import *

#Creation de passe haut. Axel

def passe_haut (X):
	N = len(X)
	Y = zeros(N,float)
	for i in range(1,N):
		Y[i] = X[i]-0.95*X[i-1]
	Y[0] = X[0]
	return(Y)
