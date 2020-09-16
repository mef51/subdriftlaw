import glob
import matplotlib.pyplot as plt
import numpy as np

from cfod import chime_intensity


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

	ref_freq = freq[0]

	shift = (k_dm * dm * (ref_freq ** -2 - freq ** -2) / dt)
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

burstdirs = ['180814', '180911', '180919']
if __name__ == "__main__":
for burst in burstdirs:
	# find msgpack files for 1 event (easiest to put them all in one directory)
	def loadburstdata(burst):
		fns = sorted(glob.glob("burst{}/*.msgpack".format(burst)))

		# load in data (every file is ~1 s, so dispersed sweep in multiple files)
		intensity, weights, fpga0s, fpgaNs, binning, rfi_mask, frame0_nanos = \
			chime_intensity.unpack_datafiles(fns)

		# load static bad channel mask
		bad_channels = read_static_mask("bad_channel_16K.mask")

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
		dt = 0.00098304  # s
		fbottom = 400.1953125  # MHz
		bw = 400.  # MHz
		nchan = 16384
		df = bw / nchan
		freq = np.arange(fbottom, fbottom + bw, df) + df / 2.

		# R2 DM
		dm = 189.4

		wfall = dedisperse(intensity, dm, freq, dt=dt*binning)
		print(wfall.shape)
		# band-averaged time-series
		ts = np.nanmean(wfall, axis=0)

		# find peak
		peak_idx = np.nanargmax(ts)

		sub = subband(wfall, 128)

		# plot
		fig, ax = plt.subplots(2, sharex=True,
			gridspec_kw={"hspace": 0., "height_ratios": [1, 3]})

		ax[0].plot(ts[peak_idx-30:peak_idx+50])
		ax[1].imshow(sub[...,peak_idx-30:peak_idx+50], origin="lower",
			aspect="auto", interpolation="nearest")

		ax[1].set_xlabel("Time [samples]")
		ax[1].set_ylabel("Frequency [subbands]")
		print("saving waterfall{}.png".format(burst))
		plt.savefig("waterfall{}.png".format(burst))
