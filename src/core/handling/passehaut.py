#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from math import *
from numpy import zeros

"""Creation de passe haut. Axel"""

def passe_haut (X):
	N = len(X)
	Y = zeros(N, float)
	for i in range(1, N):
		Y[i] = X[i] - 0.95 * X[i - 1]
	Y[0] = X[0]
	return(Y)
