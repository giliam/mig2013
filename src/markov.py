#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator as op
import numpy as np
import math
import sympy as sp
from sympy.matrices import Matrix, diag
import random
sp.init_printing(use_unicode=True)

def calcMat(v):
    n, m = v.shape
    l = []
    for i in range(n):
        l.append([])
        for j in range(n):
            if i ==j :
                l[i].append(v[i, 0]*v[i, 0])
            else:
                l[i].append(0.)

    return Matrix(l)

def modify(tmp):
    print("CHANGING BIATCHES")
    #print("tmp : {}".format(tmp))
    n, m = tmp.shape
    s = 0.
    for i in range(n):
        s += tmp[i, i]

    for i in range(n):
        if tmp[i, i] <= 0:
            tmp[i, i] = s/(n*n) # TODO : implement matrix-dependent value
    #print("now tmp : {}".format(tmp))
    return tmp

class ContinuousMarkov(object):
    def __init__(self, n, m, d, PI, A, C, G_mu, G_sigma):
        self.n = n
        self.rN = range(n)
        self.m = m
        self.rM = range(m)
        self.d = d
        self.rD = range(d)
        self.PI = PI
        self.A = A
        self.C = C
        self.G_mu = G_mu
        self.G_sigma = G_sigma

    def show(self):
        print("PI : {}\n".format(self.PI))
        print("A : {}\n".format(self.A))
        print("C : {}\n".format(self.C))
        print("G_mu : {}\n".format(self.G_mu))
        print("G_sigma : {}\n".format(self.G_sigma))

    def calcGaussianValue(self, sigma, x_):
        option = 1
        if option == 1:
            den = math.sqrt(math.pow(2*sp.pi, self.d) * sigma.det())
            v = x_.T*(sigma**-1)*x_
            exp = math.exp(-1./2.*v[0])
            if exp/den > 1:
                #print("COME ON, SON OF A BITCH !")
                return 1.1
                """print("sigma**-1 : {}".format(sigma**-1))
                print("x_ : {}".format(x_))
                print(sigma.det())
                print(sigma)
                print("v : {}".format(v))
                print("exp : {}".format(exp))
                print("den : {}".format(den))
                print("rap too big !!!! {}".format(exp/den))"""
            else:
                return exp/den
        else:
            den = 1
            v = x_.T*(sigma**-1)*x_
            exp = math.exp(-1./2.*v[0])
            if exp/den > 1:
                print("COME ON, SON OF A BITCH !")
                exp = den = 1
                """print("sigma**-1 : {}".format(sigma**-1))
                print("x_ : {}".format(x_))
                print(sigma.det())
                print(sigma)
                print("v : {}".format(v))
                print("exp : {}".format(exp))
                print("den : {}".format(den))
                print("rap too big !!!! {}".format(exp/den))"""
            return exp/den

    def calcProbabilitiesVector(self, x):
        p = [reduce(op.add, [self.C[j][m]*self.calcGaussianValue(self.G_sigma[j][m], x-self.G_mu[j][m]) for m in self.rM]) for j in self.rN]
        return p

    def calcProbabilitiesSequence(self, seq):
        return [self.calcProbabilitiesVector(seq[t]) for t in range(len(seq))]

    def forward(self, seq): # returns alpha[t in sequence][i in states]
        prob = self.calcProbabilitiesSequence(seq)
        alpha = [[self.PI[i]*prob[0][i] for i in self.rN]]

        for t in range(1, len(seq)):
            alpha.append([reduce(op.add, [alpha[t-1][j]*self.A[j][i] for j in self.rN])*prob[t][i] for i in self.rN])

        return alpha, reduce(op.add, [alpha[len(seq)-1][i] for i in self.rN])

    def backward(self, seq): # returns beta[t in sequence][i in states]
        prob = self.calcProbabilitiesSequence(seq)
        beta = [[1. for i in self.rN]]

        for t in range(len(seq)-2, -1, -1):
            beta.insert(0, [reduce(op.add, [self.A[i][j]*beta[0][j]*prob[t+1][j] for j in self.rN]) for i in self.rN])

        return beta, reduce(op.add, [beta[0][i]*prob[0][i]*self.PI[i] for i in self.rN])

    def calcXiOldGamma(self, seq, alpha, beta, p, prob): # returns xi[t in sequence-1][i in states][j in states] and oldGamma[t in sequence-1][i in states]
        xi = [[[alpha[t][i]*self.A[i][j]*prob[t+1][j]*beta[t+1][j]/p for j in self.rN] for i in self.rN] for t in range(len(seq)-1)]

        return xi, [[reduce(op.add, [xi[t][i][j] for j in self.rN]) for i in self.rN] for t in range(len(seq)-1)]

    def calcGamma(self, seq, alpha, beta, prob):
        gamma = []
        for t in range(len(seq)):
            gamma.append([])
            sumAB = 0
            for i in self.rN:
                sumAB += alpha[t][i]*beta[t][i]

            for i in self.rN:
                gamma[t].append([])
                AB = alpha[t][i]*beta[t][i]/sumAB
                for k in self.rM:
                    if prob[t][i] == 0: # This means the sum of probabilities is 0, thus a single one of them will be 0 too
                        gamma[t][i].append(0.) # We append 0
                    else:
                        gamma[t][i].append(AB*self.C[i][k]*self.calcGaussianValue(self.G_sigma[i][k], seq[t]-self.G_mu[i][k])/prob[t][i])

        return gamma

    def calcSums(self, seqs, gammas):
        littleSums = []
        littleVect = []
        littleMat = []
        fatSums = []
        for i in self.rN:
            littleSums.append([])
            littleVect.append([])
            littleMat.append([])
            fatSums.append(0)
            for k in self.rM:
                littleSums[i].append(0.)
                littleVect[i].append(Matrix([0. for a in self.rD]))
                littleMat[i].append(Matrix([[0. for b in self.rD] for a in self.rD]))
                for s in range(len(seqs)):
                    for t in range(len(seqs[s])):
                        littleSums[i][k] += gammas[s][t][i][k]
                        littleVect[i][k] += gammas[s][t][i][k]*seqs[s][t]
                        littleMat[i][k] += gammas[s][t][i][k]*calcMat(seqs[s][t]-self.G_mu[i][k])
                fatSums[i] += littleSums[i][k]

        return littleSums, littleVect, littleMat, fatSums

    def baumWelch(self, seqs, maxIt = 1000, epsilon = 10**-10):
        rS = range(len(seqs))
        oldLike = -1
        it = 0
        decrease = False

        while it < maxIt:
            alphas = []
            betas = []
            ps = []
            probs = [self.calcProbabilitiesSequence(seqs[s]) for s in rS]

            xis = []
            oldGammas = []
            gammas = []
            for s in rS:
                alpha, p = self.forward(seqs[s])
                beta, p = self.backward(seqs[s])
                alphas.append(alpha)
                betas.append(beta)
                ps.append(p)
                xi, oldGamma = self.calcXiOldGamma(seqs[s], alpha, beta, p, probs[s])
                xis.append(xi)
                oldGammas.append(oldGamma)
                gammas.append(self.calcGamma(seqs[s], alpha, beta, probs[s]))

            littleSums, littleVect, littleMat, fatSums = self.calcSums(seqs, gammas)

            PI = [reduce(op.add, [oldGammas[s][0][i] for s in rS])/len(seqs) for i in self.rN]
            A = []
            C = []
            G_mu = []
            G_sigma = []
            for i in self.rN:
                A.append([])
                den = reduce(op.add, [reduce(op.add, [oldGammas[s][t][i] for t in range(len(seqs[s])-1)]) for s in rS])
                if den == 0: # This means the probability to be in state i at time t is 0
                    # So probabilities to go from i at t to j at t+1 will be 0 for each j
                    for j in self.rN:
                        A[i].append(0.)
                else:
                    for j in self.rN:
                        num = reduce(op.add, [reduce(op.add, [xis[s][t][i][j] for t in range(len(seqs[s])-1)]) for s in rS])
                        A[i].append(num/den)

                C.append([])
                G_mu.append([])
                G_sigma.append([])
                for k in self.rM:
                    C[i].append(littleSums[i][k]/fatSums[i])
                    G_mu[i].append(littleVect[i][k]/littleSums[i][k])
                    tmp = littleMat[i][k]/littleSums[i][k]
                    if tmp.det() <= 0:
                        tmp = modify(tmp)
                        #print("NON INV !!!")
                    G_sigma[i].append(tmp)

            like = reduce(op.mul, ps)
            mean = reduce(op.add, ps)/len(ps)
            print("Likelyhood : {} (mean : {})\n".format(like, mean))
            rap = 1.
            if oldLike != -1:
                rap = like/oldLike
                if rap < 1:
                    decrease = True
                    break
                elif rap < (1+epsilon):
                    break

            oldLike = like
            self.PI = PI
            self.A = A
            self.C = C
            self.G_mu = G_mu
            self.G_sigma = G_sigma

            it += 1

        self.show()

        if it == maxIt:
            print("Ended on max iteration")
        elif decrease:
            print("Ended on decreasing likelyhood")
        else:
            print("Ended on stationnary likelyhood")

        print("Final likelyhood : {}".format(oldLike))


# Random number generator initilization
random.seed()

def generateSequence(model, deltas, num, var):
    N = num + random.randint(-var, var)
    n, m = model.shape
    seq = []
    for i in range(N):
        v = []
        for j in range(n):
            v.append(model[j, 0] + (random.random()-0.5)*deltas[j])
        seq.append(Matrix(v))

    return seq


def generateSequences(models, deltas, nums, vars, num):
    seqs = []
    for i in range(num):
        seqs.append([])
        for m in range(len(models)):
            seqs[i] += generateSequence(models[m], deltas[m], nums[m], vars[m])

    return seqs

def generateSigma(delta):
    l = []
    for i in range(len(delta)):
        l.append([])
        for j in range(len(delta)):
            if i == j:
                l[i].append(delta[i]*delta[i])
            else:
                l[i].append(0)

    return Matrix(l)

d = 2 # dimension d
n = 3 # n etats
m = 3 # m gaussiennes

modelO = Matrix([1, 1])
modelA = Matrix([1, 2])
modelU = Matrix([1.5, 1.5])
deltaO = [.5, .65]
deltaA = [0.35, .23]
deltaU = [0.45, 0.15]
sigmaO = generateSigma(deltaO)
sigmaA = generateSigma(deltaA)
sigmaU = generateSigma(deltaU)
numO = 10
numA = 10
numU = 10
varO = 3
varA = 3
varU = 3

seqs = generateSequences([modelO, modelA], [deltaO, deltaA], [numO, numA], [varO, varA], 10)
"""for i in range(len(seqs)):
    print("--------------------------")
    print(seqs[i])"""

OA_PI = [0.85, 0.05, 0.05]
OA_A = [[0.85, 0.13, 0.02], [0.05, 0.9, 0.05], [0.4, 0.2, 0.4]]
OA_C = [[0.9, 0.05, 0.05], [0.05, 0.9, 0.05], [0.05, 0.9, 0.05]]
OA_G_mu = [[modelO, modelA, modelU], [modelO, modelA, modelU], [modelO, modelA, modelU]]
OA_G_sigma = [[sigmaO, sigmaA, sigmaU], [sigmaO, sigmaA, sigmaU], [sigmaO, sigmaA, sigmaU]]

OA = ContinuousMarkov(n, m, d, OA_PI, OA_A, OA_C, OA_G_mu, OA_G_sigma)
OA.baumWelch(seqs)

trys = generateSequences([modelO, modelA], [deltaO, deltaA], [5, 5], [1, 1], 1)
test = trys[0]
trys = generateSequences([modelO, modelA], [deltaO, deltaA], [10, 10], [3, 3], 1)
test_ = trys[0]
trys = generateSequences([modelO, modelU], [deltaO, deltaU], [numO, numU], [varO, varU], 1)
test2 = trys[0]

alpha, p = OA.forward(test)
print("p : {}".format(p))
alpha, p = OA.forward(test_)
print("p : {}".format(p))
alpha, p = OA.forward(test2)
print("p : {}".format(p))

"""seqs = [[Matrix([1, 2]), Matrix([2, 1])], [Matrix([1, 0]), Matrix([0, 1])]]
PI = [.8, .1, .1]
A = [[.8, .1, .1], [.2, .4, .4], [.15, .25, .6]]
C = [[.1, .1, .8], [.7, .15, .15], [.2, .4, .4]]
G_mu = [[Matrix([4., 8.]), Matrix([-4., -8.]), Matrix([-6., 6.])], [Matrix([2., 3.]), Matrix([-4., 2.]), Matrix([3., 7.])], [Matrix([4.2, 9.]), Matrix([-5., -2.]), Matrix([-5., 5.])]]
G_sigma = [[Matrix([[1.*1., 0.], [0., .25*.25]]), Matrix([[1.*1., 0.], [0., 4.*4.]]), Matrix([[2.*2., 0.], [0., 2.*2.]])], [Matrix([[1.2*1.2, 0.], [0., .2*.2]]), Matrix([[1.5*1.5, 0.], [0., 2.*2.]]), Matrix([[2.2*2.2, 0.], [0., 2.3*2.3]])], [Matrix([[.35*.35, 0.], [0., .4*.4]]), Matrix([[1.1*1.1, 0.], [0., 1.2*1.2]]), Matrix([[1.5*1.5, 0.], [0., 1.3*1.3]])]]
M = ContinuousMarkov(n, m, d, PI, A, C, G_mu, G_sigma)


print(random.random())
print("Yello !\n--------------------------\n\n")
print("Test: \n")
#print(M.forward(seqs[0]))
#print(M.backward(seqs[0]))
M.baumWelch(seqs)"""

"""print("-----------------------------------\n")
n = 2
m = 3
d = 2
PI = [0.9, 0.1]
A = [[0.8, 0.2], [0.3, 0.7]]
C = [[0.1, 0.1, 0.8], [0.3, 0.4, 0.3]]
G_mu = [[Matrix([1, 2]), Matrix([1, 2]), Matrix([1, 2])], [Matrix([2, 1]), Matrix([2, 1]), Matrix([2, 1])]]
G_sigma = [[Matrix([[1, 0], [0, 1]]), Matrix([[1, 0], [0, 1]]), Matrix([[1, 0], [0, 1]])], [Matrix([[1, 0], [0, 1]]), Matrix([[1, 0], [0, 1]]), Matrix([[1, 0], [0, 1]])]]
M = ContinuousMarkov(n, m, d, PI, A, C, G_mu, G_sigma)"""
