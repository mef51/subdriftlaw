june 8
=====

* frbcat.org
* FRB 180814.J0422+73
* FRB121102

* Andersen 2019: "repeater bursts are generally wider than those of CHIME/FRB bursts
that have not repeated, suggesting different emission mechanisms."
	* should get some non-repeaters as well as repeaters

* CHIME data is not available publicly.
    * CHIME data IS available publicly! https://chime-frb-open-data.github.io/

* ASKAP Data 50 FRBs:
    * https://data.csiro.au/collections/#collection/CIcsiro:34437v3
* Bursts with data on frbcat.org:
    * see `frbcat_frbs_with_data.txt`

june 9
===
* downloaded data for FRB180110 from ASKAP site
    * format in SIGPROC filterbank format (http://sigproc.sourceforge.net/sigproc.pdf), http://sigproc.sourceforge.net/
    * PRESTO (https://www.cv.nrao.edu/~sransom/presto/) is related
* downloaded FRB180814 (CHIME)
    * who is making these shitty archaic data repositories? Their jnlp download manager downloads empty files and I'll have to write a wget script if I don't want to click a million links

* CHIME cfod package seems to work fine... but doesn't look like a burst

june 10
===
* cant seem to see anything in the 180814 data (both of them)

june 13
===
* tried compiling SIGPROC, its filled with fortran errors. maybe I'm using a different version of fortran. they seem to use F77
	* potential alternate? https://github.com/SixByNine/sigproc
	* try PRESTO (https://www.cv.nrao.edu/~sransom/presto/) instead? which handles SIGPROC files
	* tried PSRSoft, which is like a package manager for pulsar shit but sixproc build fails http://www.pulsarastronomy.net/wiki/Software/PSRSoft

june 15
===
* Found another secret CHIME/FRB repo https://github.com/CHIMEFRB
* compiling Mike Keith's version worked immediately lol (https://github.com/SixByNine/sigproc)

june 16
===
* askap: dont do `reader *.fil > data.csv` , it only takes the last beam file
* `splice` seems to just append columns to the data
* askap frb180110 is in beam 31, 32. DM (from shannon et al.) is 715.7 pc/cm^3
* to dedisperse example:
 `dedisperse 2018-01-10-07:07:52_0000000000000000.000000.31.fil -d 715.7 -b 336 > ddbeam31.fil`
 `reader ddbeam31.fil > dd_beam31.csv`

june 17
===
* dedispersion can be a little involved, but at its core you use the DM to compute the time delay then shift the frequency observations by that time delay. See sigproc documentation, Lorimer et al. 2007, Amiri et al. 2019
* I was curious if you could get good correlations from png images of the bursts, and seems like you can, so long as you remove the noise so that there's enough snr between the burst pixels and the noise pixels. This method feels very sketchy, but maybe if you make sure the pixel grid corresponds to the data grid (ie. your image shouldn't be higher resolution than the png of the data) then you can extract correct physical parameters of the burst
* A safer route is to try PRESTO (https://www.cv.nrao.edu/~sransom/presto/), which has a dedispersion planner thing that might be good. Otherwise we can write our own dedispersion thing

june 23
===
Repeater Sources: See repeaters.csv
Prioritize 171019, 180916.J0158+65, and 180814.J0422+73

june 24
===
* new data from chime is in a better format: https://chime-frb-open-data.github.io/
    * data doesnt match paper

june 26
===
* i downloaded the pdf figure from the arxiv source for the 180916 paper, and turns out you can open it in photoshop and extract the images automatically with high fidelity! no screenshotting, no interpolation, pixel scale is an integer, very clean way to get the data from the figures. I now have 25 images that can be used for each burst

june 29
===
* rgb2gray source: https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python
* bursts 31, 32 show a burst in the same band with obviously different sub-burst drifts
* first attempt yields 12/25 good fits for 180916+J0158+65. Can probably get a few more
* y pixel scale is variable.. seems like plus or minus 1 pixel

june 30
===
* used pixel scale to place physical axes on the images. save fit parameters so its faster

july 1
==
* when finding slope from the fit angle we correct for the pixel scale as 
$$
\tan\theta	=\frac{y}{x}
\frac{y/y_{s}}{x/x_{s}}	=\frac{y}{x}\frac{x_{s}}{y_{s}}=\frac{x_{s}}{y_{s}}\tan\theta
$$

* sigmax and sigmay are in pixel space, so they must be scaled by the pixel scale

* early plot suggests that the bursts from 180916+J0158+6 are on trend with the bursts from 121102
* ~need to investigate why the t_w for bursts 19 and 21 are negative~ just make sure sigmax and sigmay are positive

july 2
===
* need to investigate differences in tw and how they correspond to the figures
* Ziggy responded to my github issue, downsampling properly now based on his suggestion. I had tried decimating the data to 'downsample' but that didn't work so I downsample via averaging now, which is what I should have tried in the first place
* downsampling produces some streaks in the burst. Will need to resolve this eventually

july 3
===
* do boxcar downsampling for chime bursts.. convolve and sample (?)

july 4
===
* did errors for chime 180916 bursts