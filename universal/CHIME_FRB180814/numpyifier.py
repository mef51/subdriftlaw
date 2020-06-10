#!/usr/bin/python

## Python 2 script to convert CHIME data to numpy arrays.
# Python 2 cuz cfod doesnt work in Python 3

from cfod import chime_intensity as ci
import numpy as np
import os

fns = filter(lambda f: '.msgpack' in f, os.listdir('.'))
print(len(fns[:8]))
intensity, weights, fpga0s, fpgaNs, binning, rfi_mask, frame0_nanos = ci.unpack_datafiles(fns)
np.save('intensity', intensity)
