mar 28 2020
=====
* ecriture_matric_intensite.py shows the burst in frequency vs time grid. It is hella slow tho.
	* there is some processing and noise removal in here that I will just take for granted for now
* there are 16 burst with I,Q,U, and V
* just use scipy 2d autocorrelate

mar 30 2020
====

* scipy correlate2d is slow as shit oh my god like it won't even finish
* scipy fftconvolve is supposed to be the same thing but you transpose the second matrix?
	* its hella fast, i just dont understand the result
* https://stackoverflow.com/questions/51485146/efficient-2d-cross-correlation-in-python
* i put a window around the burst to make the data smaller and i get something reasonable with signal.correlate2d
* https://dsp.stackexchange.com/questions/36162/cross-correlate-a-2d-array

apr 2
====
* the form of the fitting function is e^(-y^2 - x^2) where x and y are the result of multiplying x' and y' by the rotation matrix (this allows the 2d gaussian to rotate)

april 11
====
* fitting stuff is working, now making script to process all the michilli bursts. 
* found the edge of the burst (see bursts.csv) that makes a square window of data for autocorrelation
    * some bursts (like bursts 11, 10, 9, 5, and 4) are really hard to see. Using a logscale for the colors kinda helps (`norm=matplotlib.colors.LogNorm()`)
    
april 14
=====
* there is degeneracy in the fit: the solver can make sigma_x really big and then rotate it like crazy or it can make sigma_y big and rotate it a little
* line grapher: https://www.desmos.com/calculator/e6vcn6n0nr

apr 15 meeting:
===
* do gajjar bursts, fix angle slope
* maybe use log scale for corr . fix colorbar
* fix scales, use physical units
* grab centre freq. from victor figure
* get error on theta