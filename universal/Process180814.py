import glob
import matplotlib.pyplot as plt
import numpy as np
import os, itertools
from cfod import chime_intensity
import corrfns, fitburst
from tqdm import tqdm
import pandas as pd

def dedisperse(wfall, dm, freq, dt):
	"""Dedisperse a dynamic spectrum.

	Parameters
	----------
	wfall : array_like
		Dynamic spectra of shape (nchan, nsamp).
	dm : float
		Dispersion measure to dedisperse to, in pc cm-3.
	freq : array_like
		Center frequencies of all channels, in MHz. Should have shape nchan.
	dt : float
		Sampling time, in s.

	Returns
	-------
	wfall : array_like
		Dedispersed dynamic spectra of shape (nchan, nsamp).

	"""
	k_dm = 1. / 2.41e-4
	dedisp = np.zeros_like(wfall)

	ref_freq = freq[0]### ORIGINAL
	# ref_freq = freq[-1]
	print("ref_freq", ref_freq)

	shift = (k_dm * dm * (ref_freq ** -2 - freq ** -2) / dt) ### ORIGINAL (low freq anchor)
	# shift = (k_dm * dm * (freq ** -2 - ref_freq ** -2) / dt)
	shift = shift.round().astype(int)

	for i, ts in enumerate(wfall):
		dedisp[i] = np.roll(ts, shift[i])

	return dedisp


def subband(wfall, nsub):
	nchan, nsamp = wfall.shape
	sub_factor = nchan // nsub
	return np.nanmean(wfall.reshape(-1, sub_factor, nsamp), axis=1)


def read_static_mask(static_mask):
	bad_chans = []
	x = np.loadtxt(static_mask, skiprows=1, comments="#")
	for i in range(len(x)):
		bad_chans += list(range(int(x[i][0]), int(x[i][1]), 1))
	return bad_chans

def loadburstdata(burst, tres, datadir='data/CHIME_FRB180814.J0422+73/', ddm=0, downsample=128, plot=False, save=True, forceFreshLoad=False):
	"""
	tres: time resolution in milliseconds
	"""
	dm = 189.4 + ddm
	outputfile = "{}_dm{}".format(burst, dm)

	if os.path.isfile('{}{}.npy'.format(datadir, outputfile)) and not forceFreshLoad:
		return np.load('{}{}.npy'.format(datadir, outputfile))

	fns = sorted(glob.glob("{}burst{}/*.msgpack".format(datadir, burst)))

	# load in data (every file is ~1 s, so dispersed sweep in multiple files)
	intensity, weights, fpga0s, fpgaNs, binning, rfi_mask, frame0_nanos = \
		chime_intensity.unpack_datafiles(fns)

	# load static bad channel mask
	bad_channels = read_static_mask("{}bad_channel_16K.mask".format(datadir))

	# set masked and missing channels to np.nan
	intensity[bad_channels, ...] = np.nan
	intensity[weights == 0.] = np.nan

	# normalize channels
	for i in range(intensity.shape[0]):
		if not np.isnan(intensity[i][0]):
			ts = intensity[i]
			mean = np.nanmean(ts)
			std = np.nanstd(ts)
			intensity[i,...] = (ts - mean) / std

	# CHIME/FRB constants
	dt = tres/1000 # s
	fbottom = 400.1953125  # MHz
	bw = 400.  # MHz
	nchan = 16384
	df = bw / nchan
	freq = np.arange(fbottom, fbottom + bw, df) + df / 2.

	print(binning)
	wfall = dedisperse(intensity, dm, freq, dt=dt*binning)
	print(wfall.shape)
	# band-averaged time-series
	ts = np.nanmean(wfall, axis=0)

	# find peak
	peak_idx = np.nanargmax(ts)
	sub = subband(wfall, downsample)
	print(tres)
	tleft, tright = 30, 50
	# if tres == 0.98304:
	# 	tleft, tright = 30, 50
	# elif tres == 1.96608:
	# 	tleft, tright = 80, 100
	# 	tleft, tright = 30, 50

	# plot
	if plot:
		fig, ax = plt.subplots(2, sharex=True,
			gridspec_kw={"hspace": 0., "height_ratios": [1, 3]})

		ax[0].plot(ts[peak_idx-tleft:peak_idx+tright])
		ax[1].imshow(sub[...,peak_idx-tleft:peak_idx+tright], origin="lower",
			aspect="auto", interpolation="nearest")

		ax[1].set_xlabel("Time [samples]")
		ax[1].set_ylabel("Frequency [subbands]")
		print("saving waterfall{}.png".format(burst))
		plt.savefig("waterfall{}.png".format(burst))
	if save:
		# np.save('{}{}'.format(datadir, outputfile), sub[...,peak_idx-30:peak_idx+50])
		np.save('{}{}'.format(datadir, outputfile), sub[...,peak_idx-tleft:peak_idx+tright])


	# return sub[...,peak_idx-30:peak_idx+50]
	# return sub[...,peak_idx-80:peak_idx+100]
	return sub[...,peak_idx-tleft:peak_idx+tright]

def processBurst(burstwindow, burstkey, p0=[], popt_custom=[], bounds=(-np.inf, np.inf), nclip=None, clip=None, ploti=None):
	"""
	Given a waterfall of a burst, will use the 2d autocorrelation+gaussian fitting method to find the drift and make a plot of the burst and fit.
	Parameters are added to the global lists above before being saved in a table. Eventually I may want to make this more standalone
	"""

	corr = corrfns.auto_corr2D_viafft(burstwindow)
	if nclip != None or clip != None:
		corr = np.clip(corr, nclip, clip)
	#print(burstwindow.shape, corr.shape)
	#### Autocorr noise
	autocorr_sigma = np.std( corr[:, 0:50] )
	# print('autocorr_sigma', autocorr_sigma)
	# auto_sigmas.append(autocorr_sigma)

	#### Fit Gaussian to autocorrelation. Load from parameter file if already found.
	print("finding fit {}...".format(burstkey))
	try:
		popt, pcov = fitburst.fitgaussiannlsq(corr, p0=p0, sigma=autocorr_sigma, bounds=bounds)
		perr = np.sqrt(np.diag(pcov))
		print('solution nlsq:', popt)
		print('parameter 1sigma:', perr)
		#print('pcov diag:', np.diag(pcov))
	except (RuntimeError, ValueError):
		print('no fit found')
		popt, perr = [-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1]
		if popt_custom != []:
			popt = popt_custom
	popts.append(popt)
	perrs.append(perr)

	x, y = np.meshgrid(range(0, corr.shape[1]), range(0, corr.shape[0]))
	#popt[5] = 0.1
	fitmap = fitburst.twoD_Gaussian((y, x), *popt).reshape(corr.shape[0], corr.shape[1])

	# calculate reduced chisquared
	residuals = corr - fitmap
	chisq = np.sum((residuals / autocorr_sigma) ** 2)
	red_chisq = chisq / (corr.shape[0]*corr.shape[1] - len(popt)) # this is chisq/(M-N)
	red_chisqs.append(red_chisq)
	# print('reduced chisq:', red_chisq)

	# Calculate drifit
	theta = popt[5] if abs(popt[3]) > abs(popt[4]) else popt[5] - np.pi/2
	angles.append(theta) #if theta > 0 else angles.append(theta + 2*np.pi)
	slope = np.tan(theta)
	conversion = freq_res / (time_res)
	drift = conversion * slope # MHz/ms
	theta_err = perr[-1] # do i need to correct this for pixel scale?
	drift_error = conversion * (theta_err * (1/np.cos(theta))**2)

	drifts.append(drift)
	drift_errors.append(drift_error)

	#### Plot
	extents = (0,
			   time_res*burstwindow.shape[1],
			   lowest_freq - freq_res/2.,
			   lowest_freq + freq_res*burstwindow.shape[0])

	corrextents = (-extents[1], extents[1], -(extents[3]-extents[2])*2, (extents[3]-extents[2])*2)

	if ploti == None:
		plt.figure(figsize=(15, 5))
		plt.subplot(121)
	else:
		plt.subplot(3, 2, next(ploti))
	plt.title("Burst #{}".format(burstkey))
	plt.imshow(burstwindow, aspect='auto', cmap=cmap, extent=extents, origin='lower') # white is 0, black is 1
	plt.xlabel("Time (ms)")
	plt.ylabel("Frequency (MHz)")

	if ploti == None:
		plt.subplot(122)
	else:
		plt.subplot(3, 2, next(ploti))
	plt.title("Correlation #{}".format(burstkey))
	plt.imshow(corr, aspect='auto', cmap='gray', extent=corrextents, origin='lower')
	plt.clim(0, np.max(corr)/20)

	if popt[0] > 0:
		plt.contour(fitmap, [popt[0]/4, popt[0]*0.9], colors='b', alpha=0.75, extent=corrextents, origin='lower')

	return drifts, drift_errors, popts, perrs, angles, red_chisqs

#######################


# burstdirs = ['180814', '180911', '180919']
burstdirs = ['180814', '180917']

datadir='data/CHIME_FRB180814.J0422+73'

cmap = plt.get_cmap('gray_r')
cmap.set_bad(color = 'w', alpha = 1.)

res = {    #(tres, fres)
	'180814': (0.98304, 400/16384),
	'180911': (0.98304, 400/16384),
	# '180917': (1.96608, 400/16384),
	'180917': (0.98304, 400/16384),
	'180919': (0.98304, 400/16384),
}

# time_res = 0.98304 # ms
freq_res = 400/16384*128 # MHz
lowest_freq = 400.20751953125 # MHZ

dm = 189.4
# for ddm in tqdm([189 - dm, 189.8 - dm, 190 - dm, 188.9 - dm, 0]):
for ddm in tqdm([0]):
	plt.figure(figsize=(10, 15))
	ploti = itertools.count(start=1, step=1)
	popts, perrs, drifts, drift_errors, angles, red_chisqs, keys = [], [], [], [], [], [], []
	parameterfile = '{}/chime_180814_fit_params_dm{}.csv'.format(datadir, dm + ddm)
	errorfile     = '{}/chime_180814_param_errors_dm{}.csv'.format(datadir, dm + ddm)
	for burst in burstdirs:
		print(burst)
		time_res = res[burst][0] # ms
		keys.append(int(burst))

		# find msgpack files for 1 event (easiest to put them all in one directory)
		burstwindow = loadburstdata(burst, tres=time_res, ddm=ddm, forceFreshLoad=True)
		if burst == '180919': 	# clean up some remaining noise on 180919
			burstwindow[27:32, ...] = np.nan
			burstwindow[104:106, ...] = np.nan

		burstwindow = np.nan_to_num(burstwindow)
		processBurst(burstwindow, int(burst), ploti=ploti)

	popts = pd.DataFrame(popts, index=keys, columns=['amplitude', 'xo', 'yo', 'sigmax', 'sigmay', 'theta'])
	perrs = pd.DataFrame(perrs, index=keys, columns=['amp_error', 'xo_error', 'yo_error', 'sigmax_error', 'sigmay_error', 'angle_error'])

	popts['drift (mhz/ms)']       = drifts
	popts['angle']                = angles
	perrs['drift error (mhz/ms)'] = drift_errors
	perrs['red_chisq']            = red_chisqs

	popts.to_csv(parameterfile, index_label='name')
	perrs.to_csv(errorfile, index_label='name')

	plt.savefig("FRB180814_ddm_{}.png".format(ddm))
	# plt.show()
