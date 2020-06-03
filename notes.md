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
	* some bursts (like bursts 11, 10, 9, 5, and 4) are really hard to see. Using a logscale for the colors kinda helps (`plt.imshow(..., norm=mcolors.LogNorm(vmin=0, vmax=5000))`)

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

apr 18
=====
* switching to log scale for corr helps a lot. needed to flag bad values as black (there are negative values for some reason)
* angle is clockwise from the negative y-axis. Weird. https://www.desmos.com/calculator/xa91ccx6gp
	* sign error in twoD_gaussian. fixed. angle is counter-clockwise from positive x axis as intended
* pcov gives variances of the parameters, root of that gives standard dev (error)

apr 19
===
* if sigma_y > sigma_x: theta = theta - pi/2
* michilli 2018 fig.1: time and freq. resolutions are 20.48us and 6.24 MHz
* email says 10.24us and 1.5625 MHz
* freq channel 0 = 4100.78125 MHz
* fixed the axes

apr 20
===
* with the right angle slope is just tan(theta).
	* to get MHz/ms units multiply slope by 1.5625MHz/0.01024ms

apr 21
===
* plots with drift speed and error done. need to get the central frequency
* donnees_freq_intensite.pdf has central frequencies for burst 1, 3, 6, 14, and 16
	* i think these were generated with either fit.py or fit2.py
	* not sure how valid a single gaussian fit is for these bursts, which look like multiple gaussian peaks?
* for the central frequencies of the 5 bursts victor found, the lower frequency bursts have more drift! this is what Martin predicted.


apr 22
===
* meeting:
	* put log scale on burst
	* do mhz/ms like in chime paper

apr 23
===
* TODO:
	* do gajjar (6-8 GHz) bursts
	* fix the fit for burst #10
	* make bursts more visible (log scale or truncate the scale)
	* copy chime paper and list drifts in mhz/ms
	* correct for pulse width by approximating tau_0 = b/cos(theta-pi/2), make that figure
	* find central frequency of all bursts with gaussian fit. See bottom right panel of Chime figure: Fit gaussian to time integrated spectrum
	* JPL has 2 GHz observations, decide if we can include those

apr 25
====
* wip in gajjar. Fit looks good. I had to clip the spectrum because there were many negative values, possibly from the way I removed the error.
	* (may have removed the background two different ways: with victor's loop and then my thing. just pick one (mine since it removes noise as a function of freq.))

apr 26
====
* if i clip before autocorrelation i lose the gaussian - why?
* some confusion between np.indices and np.meshgrid... switching to np.indices for now. meshgrid doesn't make sense to me atm and it keeps fucking up my fit
* more problems with 11D..
	* work on approximating tau_0 with sigma so that we can make an actually interesting plot. should be quick and higher payoff
* https://www.desmos.com/calculator/i36rd5eyfu

apr 27
===
* ended up just converting the angle the solver spit out but I have drifts for 11A and 11D now

apr 28
===
* burst 10: solver was spitting out negative sigma_x and sigma_y (which is not a big deal) but was leading to the wrong theta. putting abs() around sigma_x and sigma_y fixed the angle
	* this burst still has two bursts so still need to window it. but its a minor correction.
* annotating points: https://stackoverflow.com/questions/15910019/annotate-data-points-while-plotting-from-pandas-dataframe/15911372#15911372
* trends are not promising. michili bursts are everywhere

may 3
===
* after discussing with martin we realized we had measured pulse duration, and not arrival time as a function of frequency.
* started working on ArrivalTimes.ipynb, which fits gaussians row by row and grabs arrival and end times for each frequency.
    * Final result of this is to have the dynamic spectrum of each burst marked with start and end times for each frequency channel.

may 6
====
* I finished the arrival time stuff but it's not useful at the moment.
* martin re did parts of his analysis:
    * There are two processes: a steep drift that is within the burst, and a much larger one that is from burst to burst (when there are multiple bursts in quick succession)
* TODO:
    * separate out the subbursts in 11A
    * fix calculation of sigma_t

may 7
===
* found autocorrelation of subbursts of 11A, stored as .npy files
* found drifts. beware shearing when your cells aren't square. the major axis can look like the minor axis and vice versa

may 8
===
* i wonder if i should just do a gaussian fit to the time profile like in Josephy 2019 to get the pulse duration instead of using sigma_t. Its numbers don't really line up with a measurement by eye
* i was fitting to some of the bursts i excluded so the fit is improved ANND adding the gajjar subbursts fits so well to the trend

may 17
===
* chris's corr2d is ridiculously fast. Also, pythonic file read is much 6x faster (30s to 5s) than the dogshit that is np.loadtxt()

may 18
===
* while working on finding the error on tw i noticed I used cos twice in the equation for tw when there's really a sin and a cos (see note).
    * small correction
* michilli bursts have full error bars

may 19
====
* redid 11A and its subbursts to get errors
* rename processgajjar to processgajjar11A lol.. will need to rewrite for 11D

may 20
====

* redo drift vs tw
* scale error by reduced chisq
    * https://stackoverflow.com/questions/52591979/how-to-obtain-the-chi-squared-value-as-an-output-of-scipy-optimize-curve-fit
may 23
====
* drift errors are kinda wack. very small.. makes the fit innacurate when including errors. try:
    * lmfit package to get a gaussian
    * getting the drift using arrival times and fitting a line.
    * figure out this line in the documentation for `absolute_sigma`: `pcov(absolute_sigma=False) = pcov(absolute_sigma=True) * chisq(popt)/(M-N)`

may 25
===
* before dicking around with the errors maybe just fix the bursts (M9, M10, M13, etc.) that are clearly multiple bursts. and anyway scaling the errors didn't really make the fit better so
* New angle flipper calculator: https://www.desmos.com/calculator/f1x2pyfdix

may 26
===
* Meeting TODO:
    * fix 9
    * frequency correct the gajjar bursts and add them in a different color
* I found drifts for M10's subbursts. I used the autocorr sigma from the whole correlation instead of the individual ones, which is probably not right
* found m9 subburst drifts

may 27
===
* found weighted center frequency of all gajjar and michilli subbursts. this is for correcting the drifts of the bursts

may 28
===
* added chime burst, did a bunch of log/log fits, settled on a fit
* 11D is missing errors

may 30
===
* made figs 3 and 4

may 31
===
* TIL don't use plt.tight_layout() with plt.subplots_adjust()

june 1
===
* made figure 5
* changed the font

june 2
===
* made all figure fonts serif
* made some cartooooons for fig 1 and 2
* correcting the bursts by the center frequency has some error associated with it, need to account for that

* The font on the figures is one of these (in order of what it looks for):
['DejaVu Serif',
 'Bitstream Vera Serif',
 'Computer Modern Roman',
 'New Century Schoolbook',
 'Century Schoolbook L',
 'Utopia',
 'ITC Bookman',
 'Bookman',
 'Nimbus Roman No9 L',
 'Times New Roman',
 'Times',
 'Palatino',
 'Charter',
 'serif']
