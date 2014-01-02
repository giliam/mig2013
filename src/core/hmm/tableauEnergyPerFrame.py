#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import add
import math

def construitTableauEnergy(content):
	er = [0 for j in range(len(content))]
	for k in range(len(content)):
		er[k]=math.log(reduce(add,[abs(content[k][i])*abs(content[k][i]) for i in range(len(content))]))
	return er		
