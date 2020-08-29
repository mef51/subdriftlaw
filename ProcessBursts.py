#!/usr/bin/python3

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
from scipy import signal, ndimage
from tqdm import tqdm
from matplotlib import colors as mcolors
import functools
print = functools.partial(print, flush=True) # print doesn't happen til script ends so force it to flush... windows thing?
import pandas as pd
import corrfns
import itertools
import csv

bursts = pd.read_csv('bursts.csv')

# Gaussian 2d Fit Stuff
# Source: https://gist.github.com/andrewgiessel/6122739
# Source: https://stackoverflow.com/questions/21566379/fitting-a-2d-gaussian-function-using-scipy-optimize-curve-fit-valueerror-and-m
def gaussian(height, center_x, center_y, width_x, width_y, rotation):
	"""Returns a gaussian function with the given parameters"""
	width_x = float(width_x)
	width_y = float(width_y)

	rotation = np.deg2rad(rotation)
	center_x_old = center_x
	center_x = center_x * np.cos(rotation) - center_y * np.sin(rotation)
	center_y = center_x_old * np.sin(rotation) + center_y * np.cos(rotation)

	def rotgauss(x,y):
		xp = x * np.cos(rotation) - y * np.sin(rotation)
		yp = x * np.sin(rotation) + y * np.cos(rotation)
		g = height*np.exp( -(((center_x-xp)/width_x)**2  +((center_y-yp)/width_y)**2)/2.  )
		return g
	return rotgauss

def moments(data):
	"""Returns (height, x, y, width_x, width_y)
	the gaussian parameters of a 2D distribution by calculating its
	moments """
	total = data.sum()
	X, Y = np.indices(data.shape)
	x = (X*data).sum()/total
	y = (Y*data).sum()/total
	col = data[:, int(y)]
	width_x = np.sqrt(abs((np.arange(col.size)-y)**2*col).sum()/col.sum())
	row = data[int(x), :]
	width_y = np.sqrt(abs((np.arange(row.size)-x)**2*row).sum()/row.sum())
	height = data.max()
	return height, x, y, width_x, width_y, 2.0

def twoD_Gaussian(point, amplitude, xo, yo, sigma_x, sigma_y, theta):
	x, y = point
	xo = float(xo)
	yo = float(yo)
	a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
	b = (np.sin(2*theta))/(2*sigma_x**2) - (np.sin(2*theta))/(2*sigma_y**2)
	c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
	g = amplitude*np.exp( - a*((x-xo)**2) - b*(x-xo)*(y-yo) - c*((y-yo)**2))
	return g.ravel()

def fitgaussian(data):
	"""Returns (height, x, y, width_x, width_y)
	the gaussian parameters of a 2D distribution found by a fit"""
	params = moments(data)
	errorfunction = lambda p: np.ravel(gaussian(*p)(*np.indices(data.shape)) - data)
	p, success = scipy.optimize.leastsq(errorfunction, params)
	return p, success

def fitgaussiannlsq(data, sigma=0):
	# use curve-fit (non-linear leastsq)
	x = range(0, 1023); y = range(0, 1023)
	x, y = np.meshgrid(x, y)
	params = moments(data)#+ (0.,)
	sigma = np.zeros(len(data.ravel())) + sigma
	popt, pcov = scipy.optimize.curve_fit(twoD_Gaussian, (x, y), data.ravel(), p0=params, sigma=sigma, absolute_sigma=True)
	return popt, pcov

def dedisperse(intensity, DM, nu_high, chan_width, timestep):
	"""
	DM: pc/cm^3
	nu_high: MHz
	chan_width: MHz
	timestep: ms
	"""
	dedispersed = np.copy(intensity)

	shifts = [0 for i in range(0, len(intensity))]

	for i, row in enumerate(dedispersed):
		nu_low = nu_high - i*chan_width
		deltat = 4.14937759336e6 * (nu_low**-2 - nu_high**-2) * DM
		channelshift = -int(round(deltat/timestep))
		dedispersed[i] = np.roll(dedispersed[i], channelshift)

	return dedispersed

folder        = 'data'
outfolder     = 'figures'
parameterfile = 'frb121102params.csv'

sigmax_error = []
sigmay_error = []
angle_error  = []
drift_errors = []
drifts       = []
autocorrs    = []
auto_sigmas  = []
red_chisqs   = []
if os.path.exists(parameterfile) and False:
	popts = pd.read_csv(parameterfile, index_col=0)[['amplitude', 'xo', 'yo', 'sigmax', 'sigmay', 'theta']]
	perrs = pd.read_csv(parameterfile, index_col=0)[['amp_error', 'xo_error', 'yo_error', 'sigmax_error', 'sigmay_error', 'angle_error']]
else:
	popts, perrs = [], []

corredges = [(10, 300),
			 (10, 300),
			 (10, 300),
			 (10, 300),
			 (10, 300),
			 (10, 250),
			 (10, 300),
			 (10, 250),
			 (10, 300),
			 (10, 300),
			 (10, 300),
			 (10, 300),
			 (10, 300),
			 (10, 300),
			 (10, 300),
			 (10, 300)]

# Stuff for figure 4
burst2data = {}
burst3data = {}

### Stuff for DM/drift covariance
centerDM = 559.7 # pc/cm^3
leftDM = centerDM*0.99, centerDM*1.01 # "any bona fide dispersion measure variations are at the <= 1% level" - Michilli et al. 2018
trialDMs = np.linspace(centerDM*0.99, centerDM*1.01, num=10)
DMcovariancedata = []

for trialDM in tqdm([centerDM]):
	ploti = itertools.count(start=1, step=1)
	plt.figure(figsize=(24, 36))
	for burst, filename, edge, burstname in tqdm( zip(range(1, len(bursts['filename'])+1), bursts['filename'], bursts['edge'], bursts['name']), total=len(bursts['filename']) ):
		if 'gajjar' in filename:
			continue
		if burst in [9, 10]:
			continue
		if burst > 16:
			continue
		#print('processing {}'.format(filename))
		#junk, nchan, nbin, I, Q, U, V = np.loadtxt('{}/{}'.format(folder, filename), delimiter=' ', unpack=True)
		#Q, U, V = None, None, None

		junk, nchan, nbin, I = [], [], [], []
		with open('{}/{}'.format(folder, filename)) as infile:
			for line in infile:
				junki, nchani, nbini, Ii, _, _, _ = line.split(' ')
				junk.append(junki)
				nchan.append(nchani)
				nbin.append(nbini)
				I.append(Ii)
		junk  = np.array(junk, dtype=float)
		nchan = np.array(nchan, dtype=float)
		nbin  = np.array(nbin, dtype=float)
		I     = np.array(I, dtype=float)

		n = len(junk)
		edge = int(edge)
		# print("Data loaded")

		binmax = int(nbin[n-1])+1
		frequencymax = (int(nchan[n-1])+1)
		intensity = np.zeros((frequencymax, binmax))

		X = np.zeros(binmax)
		Y = np.zeros(frequencymax)

		# what are these?
		tmin = 500
		tmax = 1500

		#### 1. remove noise
		intensitynoise1 = np.zeros(tmin-1)
		intensitynoise2 = np.zeros(binmax-tmax)
		for i in tqdm(range(frequencymax-50,51,-1), desc='noise removal', disable=True):

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

		#### 2. find autocorrelation
		burstwindow = intensity[:,edge:edge+frequencymax]
		ddm = trialDM - centerDM
		burstwindow = dedisperse(burstwindow, ddm, (4100.78125 + 1.5625*burstwindow.shape[0]), 1.5625, 0.01024)

		# print("finding auto-correlation...")
		#corr = signal.correlate2d(burstwindow, burstwindow, mode='full')
		#print(corr.shape)
		corr = corrfns.auto_corr2D_viafft(burstwindow)

		#### 2.5 Autocorr noise
		autocorr_sigma = np.std( corr[:, corredges[burst-1][0]:corredges[burst-1][1]] )
		# print('autocorr_sigma', autocorr_sigma)
		auto_sigmas.append(autocorr_sigma)

		#### 3. Fit Gaussian to autocorrelation. Load from parameter file if already found.
		if os.path.exists(parameterfile) and ddm == 0:
			#print('loading fit...')
			# popt is [amplitude, xo, yo, sigma_x, sigma_y, theta]
			popt, perr = popts.iloc[burst-1], perrs.iloc[burst-1]
		else:
			# print("finding fit...")
			try:
				popt, pcov = fitgaussiannlsq(corr, sigma=autocorr_sigma)
				perr = np.sqrt(np.diag(pcov))
			except (RuntimeError, ValueError):
				print('no fit found')
				popt, perr = [-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1]

		popts.append(popt)
		perrs.append(perr)

		#### 3. Fit Gaussian to autocorrelation
		x = range(0, 1023); y = range(0, 1023)
		x, y = np.meshgrid(x, y)
		fitmap2 = twoD_Gaussian((x, y), *popt).reshape(1023, 1023)
		# print('solution nlsq:', popt)
		# print('parameter 1sigma:', perr)
		# print('pcov diag:', np.diag(pcov))
		# with np.printoptions(precision=3, suppress=True):
			# print('pcov:')
			# print(pcov)

		# calculate reduced chisquared
		residuals = corr - fitmap2
		chisq = np.sum((residuals / autocorr_sigma) ** 2)
		red_chisq = chisq / (corr.shape[0]*corr.shape[1] - len(popt)) # this is chisq/(M-N)
		red_chisqs.append(red_chisq)
		# print('reduced chisq:', red_chisq)

		### 3.5 Compute drift and error
		theta = popt[-1] if popt[3] > popt[4] else popt[-1] - np.pi/2
		# print('solver angle:', popt[-1], 'pos angle:', theta)
		slope = np.tan(theta)
		drift = 1.5625/0.01024 * slope # MHz/ms
		drift_error = (1.5625/0.01024) * (perr[-1] * (1/np.cos(theta))**2)
		sigmax_error.append(perr[3])
		sigmay_error.append(perr[4])
		angle_error.append(perr[5])
		drift_errors.append(drift_error)
		drifts.append(drift)
		#print('drift:', drift, "pm", drift_error)

		## DM covariance data: each row is [burst, trialdm, drift, drift_error, popt(6), perr(6)]
		DMcovariancedata.append(np.concatenate(([burst, trialDM, drift, drift_error], popt, perr)))
		with open('frb121102_dmcovariance.csv', 'a') as covariance_file:
			datawriter = csv.writer(covariance_file, delimiter=',')
			datawriter.writerow(DMcovariancedata[-1])

		#### 4. Plot
		cmap = plt.get_cmap('gray')
		cmap.set_bad(color = 'k', alpha = 1.) # potentially hides important errors in the data!

		#plt.figure(figsize=(17,8))
		#plt.subplot(121)

		plt.subplot(7, 4, next(ploti))
		plt.title("Burst #{}".format(burst))
		burstextents = [0,
			   10.24e-6 * burstwindow.shape[-1] * 1e3,
			   4100.78125 * 1e-3,
			   (4100.78125 + 1.5625*burstwindow.shape[-2]) * 1e-3]
		plt.imshow(burstwindow, cmap=cmap, interpolation='bicubic',aspect='auto', origin="lower", extent=burstextents)
		plt.xlabel("Time (ms)", size=15)
		plt.ylabel("Frequency (GHz)", size=15)
		plt.colorbar()

		#plt.subplot(122)
		plt.subplot(7, 4, next(ploti))
		#plt.title("Corr #{}. $\\nu_D$ = {:.2f} MHz/ms $\pm$ {:.2E}, peak = {:.0f}, $\sigma_x$ = {:.0f} $\sigma_y$ = {:.0f}".format(burst, drift, drift_error, np.max(corr), popt[3], popt[4]))
		plt.title("Corr #{}. $\\nu_D$ = {:.2f} MHz/ms $\pm$ {:.2E}, $\sigma_x$ = {:.0f} $\sigma_y$ = {:.0f}, tdm = {:.2f}".format(burst, drift, drift_error, popt[3], popt[4], trialDM))

		corrextents = [-10.24e-6 * (corr.shape[1]/2) * 1e3,
			   10.24e-6 * (corr.shape[1]/2) * 1e3 ,
			   (4100.78125 -  (2*4100.78125 + 1.5625*burstwindow.shape[0])/2 )*2,
			   ((4100.78125 + 1.5625*burstwindow.shape[-2]) -  (2*4100.78125 + 1.5625*burstwindow.shape[0])/2 )*2]
		#plt.imshow(corr, cmap=cmap, interpolation='bicubic',aspect='auto', origin="lower") # linear scale
		#plt.clim(0, np.max(corr)/10)
		plt.imshow(corr, cmap=cmap, interpolation='bicubic', aspect='auto', origin="lower", norm=mcolors.LogNorm(vmin=1), extent=corrextents)
		plt.xlabel("Time Shift (ms)", size=15)
		plt.ylabel("Frequency Shift (MHz)", size=15)
		plt.colorbar()

		if popt[0] != -1:
			plt.contour(fitmap2, [popt[0]/4, popt[0]*0.9], colors='w', alpha=0.5, origin='lower', extent=corrextents)

		if burst == 2:
			burst2data['corr'] = corr
			burst2data['burstwindow'] = burstwindow
			burst2data['fitmap'] = fitmap2
			burst2data['popt']  = popt
		if burst == 3:
			burst3data['corr'] = corr
			burst3data['burstwindow'] = burstwindow
			burst3data['fitmap'] = fitmap2
			burst3data['popt']  = popt

		# plt.tight_layout()
		# print('saved {}/burst_{}_figure.png'.format(outfolder, burst))

	plt.savefig('{}/burst_{}_dm_{}.png'.format(outfolder, burst, trialDM))
	plt.close()



# DMcovariancedata
# datadump = pd.DataFrame(DMcovariancedata, columns=['name', 'trialDM', 'drift', 'drift_error', 'amplitude', 'xo', 'yo', 'sigmax', 'sigmay', 'theta', 'amp_error', 'xo_error', 'yo_error', 'sigmax_error', 'sigmay_error', 'angle_error'])
# datadump.to_csv('frb121102_dmcovariance.csv')
