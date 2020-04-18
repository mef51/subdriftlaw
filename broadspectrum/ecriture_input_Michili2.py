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

inputfile = open("inputtemps%s.dat"%data,"w")

n = len(junk)

tempsmax = int(nbin[n-1])+1

centrefreq = 50

freqmax = (int(nchan[n-1])+1)

temps = np.zeros(tempsmax)

intensite = np.zeros(tempsmax)
Q2 = np.zeros(tempsmax)
U2 = np.zeros(tempsmax)
V2 = np.zeros(tempsmax)


for i in range(1,tempsmax+1) :

	temps[i-1] = nbin[i-1]

	for j in range(1+centrefreq,freqmax+1-centrefreq) :

		intensite[i-1] = intensite[i-1] + (I[(j-1)*tempsmax + (i-1)])/(freqmax-2*centrefreq)
		Q2[i-1] = Q2[i-1] + (Q[(j-1)*tempsmax + (i-1)])/(freqmax-2*centrefreq)
		U2[i-1] = U2[i-1] + (U[(j-1)*tempsmax + (i-1)])/(freqmax-2*centrefreq)
		V2[i-1] = V2[i-1] + (V[(j-1)*tempsmax + (i-1)])/(freqmax-2*centrefreq)


	inputfile.write(str(temps[i-1]))
	inputfile.write(" ")

	inputfile.write(str(intensite[i-1]))
	inputfile.write(" ")

	inputfile.write(str(Q2[i-1]))
	inputfile.write(" ")

	inputfile.write(str(U2[i-1]))
	inputfile.write(" ")

	inputfile.write(str(V2[i-1]))
	inputfile.write("\n")



inputfile.close()
