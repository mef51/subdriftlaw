#!/usr/bin/python

## convert CHIME .msgpack data to numpy arrays.

from cfod import chime_intensity as ci
import numpy as np
import os

# burstdirs = ['burst180814', 'burst180911', 'burst180917', 'burst180919']
# burstdirs = ['burst180917'] # this triggers a bug since the time resolution for 180917 is different from the hard coded cfod value see issue #5 on cfod
# burstdirs = ['burst180814', 'burst180911', 'burst180919']
for folder in burstdirs:
	print("Working on", folder, "...")
	fns = [folder+'/'+f for f in os.listdir(folder) if '.msgpack' in f]

	# hstack together
	intensity, weights, fpga0s, fpgaNs, binning, rfi_mask, frame0_nanos = ci.unpack_datafiles(fns)

	np.save(folder +'/{}_hstack'.format(folder), intensity)
	np.save(folder +'/{}weights_hstack'.format(folder), weights)

	# all together
	# for fn in fns:
	# 	print(fn)
	# 	downsample = True
	# 	if folder == 'burst180917':
	# 		downsample=False
	# 	intensity, weights, fpga0s, fpgaNs, binning, rfi_mask, frame0_nanos = ci.unpack_datafiles([folder+'/'+fn], downsample=downsample)
	# 	np.save(folder +'/'+ fn.split('.')[0], intensity)
	# 	np.save(folder +'/'+ fn.split('.')[0]+'weights', weights)
