#!/usr/bin/python3
###
# Computes the burst drift of an FRB using a 2d autocorrelation
# auth: moh, based on victor's ectrture_matrice_intensite.py dat: march 28, 2020
###

# scipy.signal.correlate2d
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
from scipy import signal
from tqdm import tqdm
from matplotlib import colors as mcolors
import functools
print = functools.partial(print, flush=True) # print doesn't happen til script ends so force it to flush... windows thing?

burst = 16
print('loading data...')
junk, nchan, nbin, I, Q, U, V = np.loadtxt('data/{}_puppi_57772_C0531+33_0007_2695.dm559.72.calibP.RM.DD.ASCII'.format(burst), delimiter=' ', unpack=True)

n = len(junk)

binmax = int(nbin[n-1])+1
frequencymax = (int(nchan[n-1])+1)
print("dimensions:", binmax, frequencymax)
intensity = np.zeros((frequencymax,binmax))

X = np.zeros(binmax)
Y = np.zeros(frequencymax)

tmin = 500

tmax = 1500

intensitynoise1 = np.zeros(tmin-1)
intensitynoise2 = np.zeros(binmax-tmax)
for i in tqdm(range(frequencymax-50,51,-1), desc='noise removal'):

	Y[i-1] = 4.15 + (i-1) * 1.5625 # ?

	for j in range(1,tmin) :

		intensitynoise1[j-1] = (I[j-1 + binmax*(frequencymax-i)])/(tmin-1)


	for j in range(tmax+1,binmax+1) :

		intensitynoise2[j-1-tmax] = (I[j-1 + binmax*(frequencymax-i)])/(binmax-tmax)

	a = sum(intensitynoise1)
	b = sum(intensitynoise2)

	for j in range(1,binmax+1) :
		X[j-1] = j-1
		intensity[i-1,j-1] = I[j-1 + binmax*(frequencymax-i)] - (a+b)/2

for i in tqdm(range(52,frequencymax-49), desc='variance'):
	for j in range(tmax+1,binmax+1) :
		intensitynoise2[j-1-tmax] = intensity[i-1,j-1]

	mean = np.mean(intensitynoise2)
	variance = np.var(intensitynoise2)

print("finding auto-correlation...")
corr = signal.correlate2d(intensity[20:30], intensity[20:30], boundary='fill', mode='full')
print('omg finally finished')
# Plot

# abscisse,ordonnee = np.meshgrid(X,Y)

cmap = "gray"
plt.imshow(intensity, cmap=cmap, interpolation='bicubic',aspect='auto', origin="lower")
plt.imshow(corr, cmap=cmap, interpolation='bicubic',aspect='auto', origin="lower")
plt.title("Burst #{}".format(burst))
plt.show()
