#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np

folder = 'spitler'
datafiles = ['burst1','burst4','burst8','burst9','burst10','burst11']


for datafile in datafiles:
	data = np.genfromtxt(folder + '/' + datafile + '.csv', delimiter=' ')

	x = data[:,0] * 1e9 # hz
	restfreq = 1.4e9 #hz
	velocity = 3e8 * (x - restfreq) / restfreq # m/s
	velocity = velocity/1000

	y = data[:,1]

	plt.plot(velocity, y, 'k-')
	plt.xlabel('Velocity (km/s)')
	plt.ylabel('S/N')
	plt.title('Burst #' + datafile.split('burst')[1])
	plt.savefig(folder + '/' + datafile + '.pdf')
	plt.clf()
	# plt.show()

	# exit()
