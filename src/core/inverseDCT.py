#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sc
import math
from operator import add

TAILLE_TABLEAU_MEL_ENTREE = 24

NOMBRE_COMPOSANTES_GARDEES = 13

B = TAILLE_TABLEAU_MEL_ENTREE


def inverseDCTI(x): # x represente le tableau en mel donne par les fonctions precedentes
	X = np.zeros(B)
	for k in range(B):
		X[k] = (0.5*(x[0]+math.pow(-1, k)*x[B-1]) + reduce(add, [x[n]*math.cos(math.pi*n*k/(B-1)) for n in range(1,B-1)]))*math.sqrt(2./(B-1))
	return X

def inverseDCTII(x):
	X = [0 for i in range(B)]
	X[0] = reduce(add, [x[n] for n in range(B)])/math.sqrt(B)
	for k in range(1, B):
		X[k]= reduce(add, [x[n]*math.cos(math.pi*(n+0.5)*k/B) for n in range(B)])*math.sqrt(2./B)
	return X

def inverseDCTIII(x):
	X = np.zeros(B)
	for k in range(B):
		X[k] = (0.5*x[0]+reduce(add, [x[n]*math.cos(math.pi*n*(k+0.5)/B) for n in range(1,B)]))*math.sqrt(2./B)
	return X

if __name__ == "__main__":
	a = [math.cos(i) for i in range(24)]
	print(inverseDCTI(a))
	print(inverseDCTII(a))
	print(inverseDCTIII(a))
