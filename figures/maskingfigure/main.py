import numpy as np
from fns import *
# plotting
import matplotlib as mpl
# Correction for mpl issue
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import scipy.optimize as opt

angle = 10
plt.rcParams["font.family"] = "serif"
# Image size
nx = 500
ny = 500

# Noise and gauss details
noise_amp = .25
angle_lo = np.pi * angle / 180. # np.pi/18.
angle_hi = np.pi * angle / 180. # np.pi/18.
sig_x = 15. * 1. # (.75 + .5 * np.random.rand())
sig_y = 90. * 1. # (.75 + .5 * np.random.rand())

# Band removal
remband = 25
bandcentre = 0

angle = angle_lo + np.random.rand() * (angle_hi - angle_lo)
signal = noise_amp * (-.5 + np.random.rand(nx, ny))

# Create x and y indices
x = np.linspace(-nx/2, nx/2, num=nx)
y = np.linspace(-ny/2, ny/2, num=ny)
y, x = np.meshgrid(x, y)    # Note: meshgrid seems to swap the xy roles that we'd prefer (??? For investigation)

# Add a gaussian onto the noise
signal += twoD_Gaussian((x, y), 0., 1., sig_x, sig_y, angle).reshape(nx, ny)

# Display it
exts = [0, 80, 400, 800]
fontsize  = 22
ticksize  = 16
labelsize = 20
print("The angle is " + str(angle*180/np.pi) + " deg.")
plt.figure(figsize=(10, 5))
# ax = plt.subplot(1, 3, 1)
# plt.imshow(np.rot90(signal), extent=exts, aspect='auto')
# plt.title("Original Signal", fontsize=fontsize)
# plt.xlabel('Time (ms)', fontsize=labelsize)
# plt.ylabel('Frequency (MHz)', fontsize=labelsize)

# Display with a mask
signal_masked = signal.copy()
signal_masked[:, int((ny-remband)/2)+bandcentre:int((ny+remband)/2)+bandcentre].fill(0.)
ax2 = plt.subplot(1, 2, 1)
plt.imshow(np.rot90(signal_masked), extent=exts, aspect='auto')
# ax2.set_yticks([])
plt.title("Masked Synthetic Signal", fontsize=fontsize)
plt.xlabel('Time (ms)', fontsize=labelsize)
plt.ylabel('Frequency (MHz)', fontsize=labelsize)
plt.xticks(fontsize=ticksize), plt.yticks(fontsize=ticksize)
# Remove a band
print("Removing band...")
signal_squeezed = np.concatenate((signal[:, 0:int((ny-remband)/2)+bandcentre],
                                signal[:, int((ny+remband)/2)+bandcentre:ny]), axis=1)
# plt.imshow(np.rot90(signal_squeezed))
# plt.title("Squeezed Signal")
# plt.show(block=False)
# plt.cla()

# Compute the autocorrelation of the zero-padded signal
print("Computing the ac of the zero-padded signal...")
signal_zp_ac = auto_corr2D_viafft(signal_masked, normalize=False, rescale=False)
maxval = np.max(signal_zp_ac)
minval = np.min(signal_zp_ac)

# Show the result
signal_zp_ac_scaled = (signal_zp_ac-minval)/(maxval-minval)
plt.subplot(1, 2, 2)
plt.imshow(np.rot90(signal_zp_ac_scaled), extent=[-80, 80, -400, 400], aspect='auto')
plt.title("2D Autocorrelation", fontsize=fontsize)
plt.xlabel('Time Shift (ms)', fontsize=labelsize)
plt.ylabel('Frequency Shift (MHz)', fontsize=labelsize)
plt.xticks(fontsize=ticksize), plt.yticks(fontsize=ticksize)
plt.tight_layout()
# plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.2, hspace=None)
# plt.show()
plt.savefig('Fig_SM_Pipeline.pdf')
exit()


# Compute the autocorrelation of the squeezed data
signal_sq_ac = auto_corr2D_viafft(signal_squeezed, normalize=False, rescale=False)
maxval = np.max(signal_sq_ac)
minval = np.min(signal_sq_ac)

# Show the result
signal_sq_ac_scaled = (signal_sq_ac-minval)/(maxval-minval)
plt.imshow(np.rot90(signal_sq_ac_scaled))
plt.title("Autocorrelation of Squeezed Signal")
plt.show(block=False)
plt.cla()

# Report results
print("")
print("The gaussian was generated from the below parameters:")
print("noise: {:.2f}".format(noise_amp) +
      ", amp: 1.00, sig_x: {:.2f}".format(sig_x) +
      ", sig_y: {:.2f}".format(sig_y) +
      ", angle: {:.2f}".format(angle * 180./np.pi))

# # Perform the fit on the squeezed data
# initial_guess = (0., 1., 10., 100., np.pi/7.)
# popt, pcov = opt.curve_fit(twoD_Gaussian, (x, y), signal.ravel(), p0=initial_guess)
#
# print("")
# print("Acting on the clean data, the fit yields:")
# print("offs: {:.2f}".format(popt[0]) +
#       ", amp: {:.2f}".format(popt[1]) +
#       ", sig_x: {:.2f}".format(popt[2]) +
#       ", sig_y: {:.2f}".format(popt[3]) +
#       ", angle: {:.2f}".format((popt[4] % (2.*np.pi)) * 180. / np.pi))

# # Fit on the raw data with banded domain imposed
# x_banded = np.concatenate((x[:, 0:int((ny-remband)/2)+bandcentre], x[:, int((ny+remband)/2)+bandcentre:ny]), axis=1)
# y_banded = np.concatenate((y[:, 0:int((ny-remband)/2)+bandcentre], y[:, int((ny+remband)/2)+bandcentre:ny]), axis=1)
# popt, pcov = opt.curve_fit(twoD_Gaussian, (x_banded, y_banded), signal_banded.ravel(), p0=initial_guess)
#
# print("")
# print("Acting on the dirty (band-removed) data, the fit yields:")
# print("offs: {:.2f}".format(popt[0]) +
#       ", amp: {:.2f}".format(popt[1]) +
#       ", sig_x: {:.2f}".format(popt[2]) +
#       ", sig_y: {:.2f}".format(popt[3]) +
#       ", angle: {:.2f}".format((popt[4] % (2.*np.pi)) * 180. / np.pi))


# Fit on the zero-padded AC data
nx_zp_ac, ny_zp_ac = signal_zp_ac.shape[0], signal_zp_ac.shape[1]

# Create x and y indices
x_zp_ac = np.linspace(-nx_zp_ac/2, nx_zp_ac/2, num=nx_zp_ac)
y_zp_ac = np.linspace(-ny_zp_ac/2, ny_zp_ac/2, num=ny_zp_ac)
x_zp_ac, y_zp_ac = np.meshgrid(x_zp_ac, y_zp_ac)
x_zp_ac = x_zp_ac.T
y_zp_ac = y_zp_ac.T

initial_guess = (0., .5, 14., 141., np.pi/7.)
popt, pcov = opt.curve_fit(twoD_Gaussian, (x_zp_ac, y_zp_ac), signal_zp_ac_scaled.ravel(), p0=initial_guess)

print("")
print("Acting on the zero-padded auto-correlated signal, the fit yields:")
print("offs: {:.2f}".format(popt[0]) +
      ", amp: {:.2f}".format(popt[1]) +
      ", sig_x: {:.2f}".format(popt[2]) +
      ", sig_y: {:.2f}".format(popt[3]) +
      ", angle: {:.2f}".format((popt[4] % (2.*np.pi)) * 180. / np.pi))
print("These sigmas translate back to conventional space as:")
print("sig_x: {:.2f}".format(popt[2]/np.sqrt(2.)) +
      ", sig_y: {:.2f}".format(popt[3]/np.sqrt(2.)))
print("As % error from true:")
print("sig_x: {:.2f}".format(100.*(popt[2]/np.sqrt(2.) - sig_x)/sig_x) + "%" +
      ", sig_y: {:.2f}".format(100.*(popt[3]/np.sqrt(2.) - sig_y)/sig_y) + "%" +
      ", angle: {:.2f}".format(100.*(popt[4] % (2.*np.pi) - angle)/angle) + "%")


# # Fit on the squeezed AC data
# nx_ac, ny_ac = signal_ac.shape[0], signal_ac.shape[1]
#
# # Create x and y indices
# x_ac = np.linspace(-nx_ac/2, nx_ac/2, num=nx_ac)
# y_ac = np.linspace(-ny_ac/2, ny_ac/2, num=ny_ac)
# x_ac, y_ac = np.meshgrid(x_ac, y_ac)
# x_ac = x_ac.T
# y_ac = y_ac.T
#
# initial_guess = (0., .5, 14., 141., np.pi/7.)
# popt, pcov = opt.curve_fit(twoD_Gaussian, (x_ac, y_ac), signal_ac_scaled.ravel(), p0=initial_guess)
#
# print("")
# print("Acting on the autocorrelated data, the fit yields:")
# print("offs: {:.2f}".format(popt[0]) +
#       ", amp: {:.2f}".format(popt[1]) +
#       ", sig_x: {:.2f}".format(popt[2]) +
#       ", sig_y: {:.2f}".format(popt[3]) +
#       ", angle: {:.2f}".format((popt[4] % (2.*np.pi)) * 180. / np.pi))
# print("These sigmas translate back to conventional space as:")
# print("sig_x: {:.2f}".format(popt[2]/np.sqrt(2.)) +
#       ", sig_y: {:.2f}".format(popt[3]/np.sqrt(2.)))
# print("As % error from true:")
# print("sig_x: {:.2f}".format(100.*(popt[2]/np.sqrt(2.) - sig_x)/sig_x) + "%" +
#       ", sig_y: {:.2f}".format(100.*(popt[3]/np.sqrt(2.) - sig_y)/sig_y) + "%" +
#       ", angle: {:.2f}".format(100.*(popt[4] % (2.*np.pi) - angle)/angle) + "%")

# Fit on the AC data with banded domain imposed
# nx_sq_ac_band, ny_sq_ac_band = signal_sq_ac_scaled.shape[0], signal_sq_ac.shape[1]+remband

# Create x and y indices
# x_sq_ac_band = np.linspace(-nx_sq_ac_band/2, nx_sq_ac_band/2, num=nx_sq_ac_band)
# y_sq_ac_band = np.linspace(-ny_sq_ac_band/2, ny_sq_ac_band/2, num=ny_sq_ac_band)
# x_sq_ac_band, y_sq_ac_band = np.meshgrid(x_sq_ac_band, y_sq_ac_band)
# x_sq_ac_band = x_sq_ac_band.T
# y_sq_ac_band = y_sq_ac_band.T
# x_sq_ac_band = np.concatenate((x_sq_ac_band[:, 0:int((ny_sq_ac_band-remband)/2+bandcentre)],
#                               x_sq_ac_band[:, int((ny_sq_ac_band+remband)/2+bandcentre):ny_sq_ac_band]), axis=1)
# y_sq_ac_band = np.concatenate((y_sq_ac_band[:, 0:int((ny_sq_ac_band-remband)/2+bandcentre)],
#                               y_sq_ac_band[:, int((ny_sq_ac_band+remband)/2+bandcentre):ny_sq_ac_band]), axis=1)
#
# initial_guess = (0., .5, 14., 141., np.pi/7.)
# popt, pcov = opt.curve_fit(twoD_Gaussian, (x_sq_ac_band, y_sq_ac_band), signal_sq_ac_scaled.ravel(), p0=initial_guess)
#
# print("")
# print("Acting on the autocorrelated data with a banded domain, the fit yields:")
# print("offs: {:.2f}".format(popt[0]) +
#       ", amp: {:.2f}".format(popt[1]) +
#       ", sig_x: {:.2f}".format(popt[2]) +
#       ", sig_y: {:.2f}".format(popt[3]) +
#       ", angle: {:.2f}".format((popt[4] % (2.*np.pi)) * 180. / np.pi))
# print("These sigmas translate back to conventional space as:")
# print("sig_x: {:.2f}".format(popt[2]/np.sqrt(2.)) +
#       ", sig_y: {:.2f}".format(popt[3]/np.sqrt(2.)))
# print("As % error from true:")
# print("sig_x: {:.2f}".format(100.*(popt[2]/np.sqrt(2.) - sig_x)/sig_x) + "%" +
#       ", sig_y: {:.2f}".format(100.*(popt[3]/np.sqrt(2.) - sig_y)/sig_y) + "%" +
#       ", angle: {:.2f}".format(100.*(popt[4] % (2.*np.pi) - angle)/angle) + "%")
