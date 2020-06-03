from __future__ import division
import math
import os
import sys
import time
import numpy as np
import scipy.stats as sct
from scipy.optimize import curve_fit
from math import log10
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy import pi as nombrepi
from lmfit import Model
from lmfit.models import LinearModel
import matplotlib as mpl

### Nothing has to be modified except for the number of donnees listed below on the code ###
fontsize = 14
family = 'serif'
plt.rcParams["font.family"] = family
### Reading the input file

donnees = open("courbe_FWHM.txt","r")

lignes = donnees.readlines()

donnees.close()

##### Define the fonction you want to fit the data to

def linear(x,a,b) :
	return a*x + b

##### Vector initialization

s = len(lignes) # Number of points on the plot #

erreurFWHM = np.zeros(s)
erreurf = np.zeros(s)

c = 0
cf = 0

for i in range(1,s+1) :

	erreurFWHM[i-1] = float(lignes[i-1].split()[3])
	erreurf[i-1] = float(lignes[i-1].split()[2])

	if (erreurFWHM[i-1] > 0) :
		c += 1
	if (erreurf[i-1] > 0) :
		cf += 1

f = np.zeros(s+2*c+2*cf) # Tableau des frequences #
FWHM = np.zeros(s+2*c+2*cf) # Tableau des FWHM #

horizontal = np.zeros((c,3))
vertical = np.zeros((c,3))
abscisse = np.zeros((c,3))
ordonnee = np.zeros((c,3))

p = 0
c2 = 0
for i in range(1,s+1) :
	if (erreurFWHM[i-1] > 0) :
		f[p] = float(lignes[i-1].split()[0])
		f[p+1] = float(lignes[i-1].split()[0])
		f[p+2] = float(lignes[i-1].split()[0])
		f[p+3] = float(lignes[i-1].split()[0])-erreurf[i-1]
		f[p+4] = float(lignes[i-1].split()[0])+erreurf[i-1]
		FWHM[p] = float(lignes[i-1].split()[1])-erreurFWHM[i-1]
		FWHM[p+1] = float(lignes[i-1].split()[1])
		FWHM[p+2] = float(lignes[i-1].split()[1])+erreurFWHM[i-1]
		FWHM[p+3] = float(lignes[i-1].split()[1])
		FWHM[p+4] = float(lignes[i-1].split()[1])

		horizontal[c2,0] = f[p+3]
		horizontal[c2,1] = f[p]
		horizontal[c2,2] = f[p+4]
		ordonnee[c2,:] = FWHM[p+1]

		vertical[c2,0] = FWHM[p]
		vertical[c2,1] = FWHM[p+1]
		vertical[c2,2] = FWHM[p+2]
		abscisse[c2,:] = f[p]

		c2 += 1
		p+=5

	else :
		f[p] = float(lignes[i-1].split()[0])
		FWHM[p] = float(lignes[i-1].split()[1])
		p+= 1

# Definition when you wawnt to plot with b = 0

def lineaire(x,a) :
	return a*x

gmodel = Model(lineaire)
out = gmodel.fit(FWHM,x = f,a = 100)
print(out.fit_report())

r = sct.pearsonr(f,FWHM)
print(r)

###### Here you need to change the numbers of points from an author ######

donnees_Micchili = 5
donnees_Law = 6
donnees_Scholz = 2
donnees_Spitler = 4
donnees_Gajjar = 4

# nothing to touch here #

freqM = np.zeros(donnees_Micchili)
freqL = np.zeros(donnees_Law)
freqSc = np.zeros(donnees_Scholz)
freqSp = np.zeros(donnees_Spitler)
freqG = np.zeros(donnees_Gajjar)
FWHMM = np.zeros(donnees_Micchili)
FWHML = np.zeros(donnees_Law)
FWHMSc = np.zeros(donnees_Scholz)
FWHMSp = np.zeros(donnees_Spitler)
FWHMG = np.zeros(donnees_Gajjar)

counter = 0
for i in range(1,donnees_Spitler+1) :
	freqSp[i-1] = f[counter]
	FWHMSp[i-1] = FWHM[counter+1]
	counter+= 5
for i in range(1,donnees_Scholz+1) :
	freqSc[i-1] = f[counter]
	FWHMSc[i-1] = FWHM[counter+1]
	counter+= 5
for i in range(1,donnees_Law+1) :
	freqL[i-1] = f[counter]
	FWHML[i-1] = FWHM[counter+1]
	counter+= 5
for i in range(1,donnees_Micchili+1) :
	freqM[i-1] = f[counter]
	FWHMM[i-1] = FWHM[counter+1]
	counter+= 5
for i in range(1,donnees_Gajjar+1) :
	freqG[i-1] = f[counter]
	FWHMG[i-1] = FWHM[counter+1]
	counter+= 5

# You can change the colors as you want, the title, etc ... #

couleur = ['m']*donnees_Spitler + ['g']*donnees_Scholz + ['b']*donnees_Law + ['k']*donnees_Micchili + ['c']*donnees_Gajjar

for i in range(1,c+1) :

	plt.plot(abscisse[i-1],vertical[i-1],'%s'%couleur[i-1])
	plt.plot(horizontal[i-1],ordonnee[i-1],'%s'%couleur[i-1])


plt.plot(freqG,FWHMG, 'cx', label = "Gajjar et al. (2018)")
plt.plot(freqM,FWHMM, 'ko', label = "Michilli et al. (2018)")
plt.plot(freqL,FWHML, 'bs', label = "Law et al. (2017)")
plt.plot(freqSc,FWHMSc, 'g+', label = "Scholz et al. (2016)")
plt.plot(freqSp,FWHMSp, 'm.', label = "Spitler et al. (2016)")
plt.plot(f,out.best_fit, 'r')
plt.xlabel(u"$\\nu_\\mathrm{obs}$ (GHz)", fontsize=fontsize, family=family)
plt.ylabel("FWHM (MHz)", fontsize=fontsize, family=family)
plt.tick_params(labelsize=fontsize-2)
plt.legend(fontsize=fontsize-4)
# for f in['png', 'eps', 'pdf']: plt.savefig('FWHM_modifiee.{}'.format(f), dpi = 1000)
for f in['png', 'eps', 'pdf']: plt.savefig('../paper_figures/Doppler-FRB121102.{}'.format(f), dpi = 1000)
plt.show()
