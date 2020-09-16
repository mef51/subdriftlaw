#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import os
from tqdm import tqdm
import skimage.measure
import corrfns

def dedisperse(intensity, DM, nu_high, chan_width, timestep):
	# Dedispersion
	dedispersed = np.copy(intensity)

	shifts = [0 for i in range(0, len(intensity))]
	k_DM = 1. / 2.41e-7    # ms, MHz
	# k_DM = 4.14937759336e6 # ms, MHz
	# nu_high = 1488
	# timestep = 1.265 # ms
	for i, row in enumerate(dedispersed):
		nu_low = nu_high - i*chan_width
		deltat = k_DM * (nu_low**-2 - nu_high**-2) * DM
		#print(deltat/timestep)
		channelshift = -int(round(deltat/timestep))
		dedispersed[i] = np.roll(dedispersed[i], channelshift)

	return dedispersed


# burstdirs = ['burst180814', 'burst180911', 'burst180917', 'burst180919']
# burstdirs = ['burst180814', 'burst180911', 'burst180919']
burstdirs = ['burst180814']

res = {    #(tres, fres)
	'burst180814': (0.983, 16384/400),
	'burst180911': (0.983, 16384/400),
	'burst180917': (1.966, 16384/400),
	'burst180919': (0.983, 16384/400),
}

for burst in tqdm(burstdirs):
	burstfile  = '{}_hstack.npy'.format(burst)
	weightfile = '{}weights_hstack.npy'.format(burst)

	cmap = plt.get_cmap('gray_r')
	cmap.set_bad(color = 'w', alpha = 1.)

	data    = np.load("{}/{}".format(burst, burstfile))
	weights = np.load("{}/{}".format(burst, weightfile))

	data    = data[:, :]
	weights = weights[:, :]
	weights[13312:14592] = 0
	weights[11776:12032] = 0
	weights[2060:2850]   = 0
	weights[768:1024]    = 0

	np.putmask(data, ~weights.astype(bool), np.nan)
	data = data - 1*data[:, 0:200].mean(axis=1)[:,None]
	data = dedisperse(data, 190, 800, res[burst][1], res[burst][0])
	downsample = 256
	data = skimage.measure.block_reduce(data, block_size=(downsample, 1), func=np.nanmean)
	print(data.shape)

	tchanstep = 128 # ~ 100 ms

	pli = 1
	plt.figure(figsize=(100,160))
	for window in tqdm(np.split(data, tchanstep, axis=1)):
		plt.subplot(16, 10, pli)
		pli += 1

		extents = (pli*tchanstep*res[burst][0], res[burst][0]*window.shape[1]+pli*tchanstep*res[burst][0], 400, 800)
		corrextents = (-extents[1], extents[1], -(extents[3]-extents[2])*2, (extents[3]-extents[2])*2)

		plt.imshow(window, origin="lower", aspect="auto", interpolation="nearest", cmap=cmap, extent=extents)
		# windowcorr = corrfns.auto_corr2D_viafft(np.nan_to_num(window))
		# plt.imshow(windowcorr, origin="lower", aspect="auto", interpolation="nearest", cmap="gray")

		# plt.clim(0, np.max(window)/4)
		plt.xlabel("Time shift [ms]")
		plt.ylabel("Frequency shift [MHz]")

	print("saving...")
	plt.tight_layout()
	outfile = '{}.png'.format(burst)
	plt.savefig(outfile)
	print('saved', outfile)


	#if burst == 'burst180814': plt.savefig('bursts180814.png')
	#if burst == 'burst180814': plt.savefig('bursts180814search.png')
