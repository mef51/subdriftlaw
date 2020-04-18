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
from matplotlib import colors as mcolors

data = str(input("Numero de plot : "))

junk, nchan, nbin, I, Q, U, V = np.loadtxt('data/16_puppi_57772_C0531+33_0007_2695.dm559.72.calibP.RM.DD.ASCII', delimiter=' ', unpack=True)

inputfile = open("intensite%s.dat"%data,"w")

n = len(junk)

binmax = int(nbin[n-1])+1

frequencemax = (int(nchan[n-1])+1)

#~ temps = np.zeros(tempsmax)
#~ frequence = np.zeros(feqmax)

intensite = np.zeros((frequencemax,binmax))

X = np.zeros(binmax)
Y = np.zeros(frequencemax)

tmin = 500

tmax = 1500

intensitebruit1 = np.zeros(tmin-1)
intensitebruit2 = np.zeros(binmax-tmax)

for i in range(frequencemax-50,51,-1) :

	Y[i-1] = 4.15 + (i-1) * 1.5625

	for j in range(1,tmin) :

		intensitebruit1[j-1] = (I[j-1 + binmax*(frequencemax-i)])/(tmin-1)


	for j in range(tmax+1,binmax+1) :

		intensitebruit2[j-1-tmax] = (I[j-1 + binmax*(frequencemax-i)])/(binmax-tmax)

	a = sum(intensitebruit1)
	b = sum(intensitebruit2)

	for j in range(1,binmax+1) :

		X[j-1] = j-1

		intensite[i-1,j-1] = I[j-1 + binmax*(frequencemax-i)] - (a+b)/2

		inputfile.write(str(intensite[i-1,j-1]))
		inputfile.write(" ")

	inputfile.write("\n")

inputfile.close()

# Variance

inputfile2 = open("variance%s.dat"%data,"w")

for i in range(52,frequencemax-49) :

	for j in range(tmax+1,binmax+1) :

		intensitebruit2[j-1-tmax] = intensite[i-1,j-1]

	moyenne = np.mean(intensitebruit2)
	variance = np.var(intensitebruit2)
	inputfile2.write(str(i-1))
	inputfile2.write(" ")
	inputfile2.write(str(variance))
	inputfile2.write(" ")
	inputfile2.write(str(moyenne))
	inputfile2.write("\n")

inputfile2.close()

# Plot

abscisse,ordonnee = np.meshgrid(X,Y)

cmap = "gray"

plotcolor = plt.imshow(intensite,cmap=cmap, interpolation='bicubic',aspect='auto', origin="lower")
plt.title("freq_vs_temps numero %s"%data)
plt.show()



