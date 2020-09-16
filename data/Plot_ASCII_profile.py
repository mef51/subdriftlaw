import numpy as np
from matplotlib import pyplot

#junk, nchan, nbin, I, Q, U, V = np.loadtxt('13_puppi_57748_C0531+33_0594_49.dm559.72.calibP.RM.F.ASCII', delimiter=' ', unpack=True)

junk, nchan, nbin, I, Q, U, V = np.loadtxt('06_puppi_57747_C0531+33_0558_3687.dm559.72.calibP.RM.F.ASCII', delimiter=' ', unpack=True)

# print len(nbin), len(I), len(Q), len(U), len(V)

I_mean = np.mean(I[:500])
Q_mean = np.mean(Q[:500])
U_mean = np.mean(U[:500])
V_mean = np.mean(V[:500])

L = np.sqrt(Q**2+U**2)
L_mean = np.mean(L[:500])

I = I-I_mean
Q = Q-Q_mean
U = U-U_mean
V = V-V_mean
L = L-L_mean

pyplot.plot(nbin,I,color='black')
pyplot.plot(nbin,L,color='red')
pyplot.plot(nbin,V,color='blue')

pyplot.show()


