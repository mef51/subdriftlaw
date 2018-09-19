from __future__ import division
import math
import os
import sys
import time
import numpy as np
import scipy.stats
from scipy.optimize import curve_fit
from math import log10
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy import pi as nombrepi

data = str(input("Numero de plot : "))

junk, nchan, nbin, I, Q, U, V = np.loadtxt('data/16_puppi_57772_C0531+33_0007_2695.dm559.72.calibP.RM.DD.ASCII', delimiter=' ', unpack=True)

inputfile = open("input.dat","w")

n = len(junk)

frequencemax = int(nchan[n-1])+1

binmax = int(nbin[n-1])+1

frequence = np.zeros(frequencemax)

intensite = np.zeros(frequencemax)

pas = 1.5625 # given by the author

## here you will choose the range of time where the signal is (you can choose larger) after
## seeing it with the ecriture-matrice-intensite.py

# burst # 16
tmin = 800
tmax = 1100

# burst #1
# tmin = 1500
# tmax = 2000

# nothing to touch here, juste calculating the noise, and summing on time #

intensitebruit1 = np.zeros(tmin-1)
intensitebruit2 = np.zeros(binmax-tmax)
variance = np.zeros(binmax)

for i in range(1,frequencemax+1) :

	frequence[i-1] = (i-1)

	### Calcul des incertitudes sur chaque frequence

	for j in range(1,binmax+1) :

		variance[j-1] =  I[j-1 + binmax*(frequencemax-i)]

	### Calcul de l'intensite du signal ###

	for j in range(tmin,tmax+1) :

		intensite[i-1] = intensite[i-1] + (I[j-1 + binmax*(frequencemax-i)])/(tmax+1-tmin) # frequences rangees en ordre inverse

	### Calcul du bruit et soustraction ###

	for j in range(1,tmin) :

		intensitebruit1[j-1] = (I[j-1 + binmax*(frequencemax-i)])/(tmin-1)

	for j in range(tmax+1,binmax+1) :

		intensitebruit2[j-1-tmax] = (I[j-1 + binmax*(frequencemax-i)])/(binmax-tmax)

	intensite[i-1] = intensite[i-1] - (sum(intensitebruit1)+sum(intensitebruit2))/2

	inputfile.write(str(frequence[i-1]))
	inputfile.write(" ")

	inputfile.write(str(intensite[i-1]))
	inputfile.write(" ")

	variance_freq = np.var(variance)
	inputfile.write(str(variance_freq))
	inputfile.write(" ")

	moyenne_freq = np.mean(variance)
	inputfile.write(str(moyenne_freq))

	inputfile.write("\n")


### Now you have the file "input(numberoftheburst).dat" ready to be used.

inputfile.close()
