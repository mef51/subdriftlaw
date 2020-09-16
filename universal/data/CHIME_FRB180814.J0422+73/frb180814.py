#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import os
import skimage.measure

def dedisperse(intensity, DM, nu_high, chan_width, timestep):
	dedispersed = np.copy(intensity)

	shifts = [0 for i in range(0, len(intensity))]
	k_DM = 1. / 2.41e-7    # ms, MHz
	for i, row in enumerate(dedispersed):
		nu_low = nu_high - i*chan_width
		deltat = k_DM * (nu_low**-2 - nu_high**-2) * DM
		channelshift = -int(round(deltat/timestep))
		dedispersed[i] = np.roll(dedispersed[i], channelshift)

	return dedispersed

res = {    #(tres, fres)
	'burst180814': (0.983, 16384/400),
}

burst = 'burst180814'
burstfile  = '{}_hstack.npy'.format(burst)
weightfile = '{}weights_hstack.npy'.format(burst)

cmap = plt.get_cmap('gray_r')
cmap.set_bad(color = 'w', alpha = 1.)

data    = np.load("{}/{}".format(burst, burstfile))
weights = np.load("{}/{}".format(burst, weightfile))

# remove noisy channels
weights[13312:14592] = 0
weights[11776:12032] = 0
weights[2060:2850]   = 0
weights[768:1024]    = 0

np.putmask(data, ~weights.astype(bool), np.nan) # set noise to nan so it doesnt affect downsample

data = data - 1*data[:, 0:200].mean(axis=1)[:,None] # remove background
data = dedisperse(data, 190, 800, res[burst][1], res[burst][0]) # dedisperse

downsample = 256
data = skimage.measure.block_reduce(data, block_size=(downsample, 1), func=np.nanmean)
print(data.shape)

tchanstep = 128 # ~ 100 ms

pli = 1
plt.figure(figsize=(100,160))
for window in np.split(data, tchanstep, axis=1):
	plt.subplot(16, 10, pli)
	pli += 1

	extents = (pli*tchanstep*res[burst][0], res[burst][0]*window.shape[1]+pli*tchanstep*res[burst][0], 400, 800)
	corrextents = (-extents[1], extents[1], -(extents[3]-extents[2])*2, (extents[3]-extents[2])*2)

	plt.imshow(window, origin="lower", aspect="auto", interpolation="nearest", cmap=cmap, extent=extents)
	plt.xlabel("Time shift [ms]")
	plt.ylabel("Frequency shift [MHz]")

print("saving...")
plt.tight_layout()
outfile = '{}.png'.format(burst)
plt.savefig(outfile)
print('saved', outfile)
