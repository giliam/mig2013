#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hmm
import pickle
import math

def getData(name):
    with open(name,"r") as f:
        content = pickle.Unpickler(f).load()

    return content

def getID(d):
    l = []
    for i in range(d):
        l.append([])
        for j in range(d):
            if i==j:
                l[i].append(1.)
            else:
                l[i].append(0.)

    return l

def uniformPI(n):
    PI = []
    for i in range(n):
        PI.append(1./n)
    return PI

def uniformA(n):
    A = []
    for i in range(n):
        A.append(uniformPI(n))
    return A

def uniformC(n, m):
    C = []
    for i in range(n):
        C.append(uniformPI(m))
    return C

def uniformG_sigma(n, m, d):
    G_sigma = []
    for i in range(n):
        G_sigma.append([])
        for j in range(m):
            G_sigma[i].append(getID(d))
    return G_sigma

def normalize(l):
    t = 0
    for i in range(len(l)):
        t += l[i]*l[i]
    t = math.sqrt(t)

    if t == 0:
        return l

    for i in range(len(l)):
        l[i] /= t

    return l

def distL(a, b):
    r = 0
    for i in range(len(a)):
        r += (a[i]-b[i])*(a[i]-b[i])

    return math.sqrt(r)

def coupures(l):
    l_ = []
    for i in range(len(l)-1):
        l_.append(distL(l[i], l[i+1]))

    normalize(l_)

    coupures = []
    for i in range(len(l)-1):
        if l_[i] >= 0.35:
            coupures.append(i)

    return coupures

def add(l, l_):
    for i in range(len(l_)):
        done = False
        for j in range(len(l)):
            if l_[i] == l[j][0]:
                l[j] = (l[j][0], l[j][1]+1)
                done = True
                break
            elif l_[i] < l[j][0]:
                l.insert(j, (l_[i], 1))
                done = True
                break
        if done == False:
            l.append((l_[i], 1))
    return l

def convert(l):
    max = 0
    for i in range(len(l)):
        if l[i][0] > max:
            max = l[i][0]

    l_ = [0 for k in range(max+1)]
    for i in range(len(l)):
        l_[l[i][0]] = l[i][1]

    return l_

def spikes(l):
    changed = True
    while changed == True:
        changed = False
        l_ = [0 for k in range(len(l))]

        if l[1] > l[0] and l[0] != 0:
            l_[1] += l[0]
            changed = True
        else:
            l_[0] += l[0]

        for i in range(1, len(l)-1):
            if l[i-1] > l[i] and l[i] != 0:
                l_[i-1] += l[i]
                changed = True
            elif l[i+1] > l[i] and l[i] != 0:
                l_[i+1] += l[i]
                changed = True
            else:
                l_[i] += l[i]

        if l[len(l)-2] > l[len(l)-1] and l[len(l)-1] != 0:
            l_[len(l)-2] += l[len(l)-1]
            changed = True
        else:
            l_[len(l)-1] += l[len(l)-1]

        l = l_

    l_ = []

    for i in range(len(l)):
        if l[i] > 0:
            l_.append(i)

    return l_

def metaCoupures(seqs):
    l = []
    for i in range(len(seqs)):
        add(l, coupures(seqs[i]))

    l = convert(l)
    l = spikes(l)

    morceaux = [[] for k in range(len(l)+1)]
    for i in range(len(seqs)):
        k = 0
        for j in range(len(seqs[i])):
            morceaux[k].append(seqs[i][j])
            if k < len(l) and j == l[k]:
                k += 1

    mus = []
    for i in range(len(morceaux)):
        mu = [0 for k in range(len(morceaux[i][0]))]
        for j in range(len(morceaux[i])):
            for k in range(len(morceaux[i][j])):
                mu[k] += morceaux[i][j][k]

        for k in range(len(morceaux[i][0])):
            mu[k] /= len(morceaux[i])
        mus.append([mu])

    return mus

def buildHMMs(HMMs, HMMsPath, maxIt, path="db/"):
    G_mu = []
    seqs = []
    for i in range(len(HMMsPath)):
        seqs.append(getData(path + HMMsPath[i]))
        G_mu = G_mu + metaCoupures(seqs[i])

    n = len(G_mu)
    m = 1
    d = 13

    for i in range(len(HMMs)):
        hmm.createMarkov(HMMs[i], n, m, d, uniformPI(n), uniformA(n), uniformC(n, m), G_mu, uniformG_sigma(n, m, d))
        x = hmm.baumWelch(HMMs[i], seqs[i], maxIt)
        if x == 0.5:
            print("HMM '{}' final likelyhood (log) : -inf".format(HMMs[i]))
            print("WARNING : HMM yielded 0 likelyhood !")
        elif x == 0.8:
            print("ERROR : HMM '{}' not found !".format(HMMs[i]))
        elif x >= 1:
            print("HMM '{}' final likelyhood (log) : {}".format(HMMs[i], 1-x))
            print("WARNING : Baum-Welch algorithm ended because of iterations' limit ({})".format(maxIt))
        else:
            pass
            #print("HMM '{}' final likelyhood (log) : {}".format(HMMs[i], x))
def recognize(seq):
    return(hmm.recognize(seq))

def recognizeList(name,path):
    seqs = getData(path)
    for i in range(len(seqs)):
        print("Sequence {} of {} recognized as : {}".format(i, name, hmm.recognize(seqs[i])))
    print("")
    
if __name__ == "__main__":
    HMMs = ["Deux", "Trois", "Cinq"]

    buildHMMs(HMMs, 500)

    recognizeList("Julien")
    recognizeList("Adrien")
