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

##### Lecture du fichier de donnees (frequences/Intensite)

donnees = open("inputtemps.dat","r")

lignes = donnees.readlines()

donnees.close()

##### Initialisation des tableaux

s = len(lignes) # Nombre de lignes du fichier correspondant au nombre de points #

t = np.zeros(s) # Tableau des temps entier #

I = np.zeros(s) # Tableau des intensites #



##### Choix de la plage de frequences et remplissage des tableaux

# tmin = float(input("Minimal time : "))

# tmax = float(input("Maximal time : "))
tmin = 800
tmax = 1200

for i in range(1,s+1) :

	t[i-1] = float(lignes[i-1].split()[0])
	I[i-1] = float(lignes[i-1].split()[1])


	if (t[i-1] <= tmin) :

		indicemin = i-1

	if (t[i-1] <= tmax) :

		indicemax = i-1

n = indicemax-indicemin+1 # nombre de points sur la plage de frequences voulue

temps = np.zeros(n) # Tableau des temps sur la plage voulue

intensite = np.zeros(n) # Tableau des intensites sur la plage voulue

for i in range(1,n+1) :

	temps[i-1] = t[indicemin+(i-1)]

	intensite[i-1] = I[indicemin+(i-1)]


##### Calcul des grandeurs propres au signal

esperance = sum(temps*intensite)/sum(intensite)

variance = np.sqrt(sum(intensite*(temps-esperance)**2)/sum(intensite))

##### Definition de la fonction fit gaussienne (pas

def gaussienne(x,b,a,xo,sigma) :
	return b+a*np.exp(-(x-xo)**2/(2*(sigma**2)))

##### Codage du fit

parametres,covariance = curve_fit(gaussienne,temps,intensite,p0=[np.max(intensite),np.max(intensite),esperance,variance])

##### Ecriture et affichage des resultats

plt.plot(temps,intensite,'b+',label = 'data')
plt.plot(temps,gaussienne(temps,*parametres),'r',label = 'fit')
plt.legend()
plt.xlabel("bin")
plt.ylabel("I")
plt.title("Sommes sur toutes les frequences")
plt.show()

#print(parametres)

