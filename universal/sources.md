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

july 6
===
* in FRB2020 talks
    * http://chime-frb.ca/repeaters
* frb171019 is in beams 20, 21, 27, 28
* there's an implementation of dedispersion here: https://github.com/danielemichilli/DM_phase/blob/master/DM_phase.py#L553
    * the key line is `shift = (k_DM * DM * (reference_frequency**-2 - freq**-2) / dt).round().astype(int)`
* The published DM doesn't give me what is shown in Kumar et al. 2019, i have to use a larger value, like the other burst. Not sure why

july 7
===
* add 180916 bursts to 121102 bursts
* Tried to use DM_phase to get a DM for 171019 but eeets not woooorkinggggg. Best value it gives is 380, which is worse than what I could do by eye
    * ok it works if you use a large range and fine grid kinda

july 8
===
* read hessels
* do 180814
* no matter the DM the relationship is just shifted (duration order is preserved)

july 11
===
* shri from FRB2020 gave a good talk about DM
* different DM's preserve "steepness" order but I don't think it will affect durations. So different DMs should only affect which A/tw curve the points land on (by only affecting A)
* kinda fix my banding problem by using np.nanmean instead of np.mean when downsampling
* 180814.J0442+73 data looks like shit, no bursts, noisy...

july 15-16
===
* opened another chime issue, gonna process the 180916 data properly in the meantime (ie. not from images)

july 17
===
* i found fits using the proper 180916 data and it mostly finds the same fits as the image technique did

july 20
===
* calculate drifts wip

july 23
===
* ive calculated the drifts from the data itself and it very closely matches what i got from the images, which validates that method. sometimes the quick and dirty way is also the correct way.

july 25
===
* using parameter guesses to get better fits on some bursts
    * tried a shotgun blast (every fit starts the search with the same ellipse. i chose the ellipse for burst 14 cuz it looked reasonable) --> doesn't work
    * can fit some bursts when i feed it a good initial start as well as bounds on the amplitude.
    * I noticed the initial guess from moments() is often very bad which might be why some fits are not found
    * clipping the autocorrelation also works
* finalized 180916 fits and drifts, 16 points in total

july 26
===
* stacked and dedispered the 180814 bursts, but having trouble finding them in the 16 second cutouts.
    * needed to use the ubuntu subsystem to get around the memory error thing

july 27
===
* finalized 180916 and updated the figures, just 180814 is left

july 28
===
* fit for 180916:15 can be tweaked a little. its too wide for the autocorrelation it seems

aug 3
===
* did 180814 via images
    * pixelxscale is ~348px/129units, y is ~650/64units
* there is an inconsistency in burst181028: i get a different duration than the chime paper

* I was accidentally plotting the raw drift instead of the drift corrected to the Michilli frequency... The fit is MUCH BETTER!! All three sources fall very close to the fit

aug 5
===
* plotting drift/nu_obs as chris suggested (to isolate the fit parameter to properties of the source) still shows good fit, and separation between sources that shows the fit is valid over distinct regions of the domain
* redshifts:
    frb121102: z = 0.19273 (josephy et al. 2019, frbcat.org)
    frb180814.J0422+73: z < 0.1 (amiri et al. 2019)
    frb1801916.J0158+65: z = 0.0337 (chime 2020b et al.)
* added redshift corrected plots

aug 6
===
* fix redshift corrected plots, redshift makes slight difference

aug 7
===
* added extra dedispersion to 180916 data to see how it affects the trend
    * there is a definite shift in the data, however, as we argued in our referee report, i think the existence of a relationship is still there regardless of the DM. Now I was a bit limited in the DMs I could pick because of the width of the data set (which I could have worked around by zero-padding) but more importantly because the bursts would very quickly become positive outside of this delta DM range. I think this is a consequence of how the DM is found: it is an optimization process, so moving away from the found DM in either direction by any significant steps will be obviously incorrect. This is in fact a good thing: it means the DMs that are published are not as terrible as we've been assuming, even when the burst drifts come out slightly positive like in the case of frb180814: the DM can certainly be tweaked a little bit to get a negative slope, but any significant changes to the DM can be safely ruled out.
    * I think this means that (a) having the right DM is important in obtaining a good fit between sources and (b) the fact that we have a good fit isn't coincidence, but a consequence of well-selected DMs on the part of CHIME and other authors. I want to therefore cautiously suggest that, if indeed there is a shared fit between sources, you can dedisperse bursts from other repeaters by picking a DM that lines that source's bursts with our fit

aug 8
===
* tried splitting onto 100ms windows but the 180814 burst still doesn't show up. Maybe the dispersion is bad? Maybe I'll try the other bursts? will need to remove the noise for those bursts..

aug 14
===
* Ziggy replied with some suggestions about checking the true error of the drift measurement, and said he'll help with 180814 eventually. He also pointed out that the DM for repeaters changes.. We need to understand how this affects the trend and probably do a proper error analysis for the paper
* FRB121102 DM Ranges
    * In the data we've used:
        * FRB121102 Gajjar (11A and 11D): 565 pc/cm^3,
        * FRB121102 Michilli            : 559.7 pc/cm^3
        * FRB180916.J0158+65            : 348.82 pc/cm^3
        * FRB180814.J0455+73            : 189.4 pc/cm^3
    * FRB121102 Spitler 2014 553-569 pc/cm^3
    * FRB121102 Gajjar 2018 562-636 pc/cm^3 (583-601 pc/cm^3 for the bursts we've used)
    * FRB121102 Michilli 2018 <= 1% of 559.7 = ~6 pc/cm^3
    * FRB180916 CHIME 2020: 348-350
    * FRB180814.J0455+74 Amiri 2019 188.9-190 pc/cm^3

aug 15
===
* If I had read gajjar et al. 2018 more carefully I would have seen packages and data releases for all their bursts:
    * http://seti.berkeley.edu/frb121102/technical.html
    * https://github.com/mtlam/PyPulse
    * perhaps we can add more 121102 bursts to our plot
* Something we should say "we choose the structure-optimizing DM over the S/N-maximizing DM whenever possible"
* There are several orders of magnitude between the drift rates of pulsar pulses and FRBs (e.g. Hewish 1980)
* In order to incorporate the error on the DM into the drift measurement, find what the drift is at each end of DM range? But this doesn't take into account the variation of DM between bursts..
* DM can also be frequency dependant (Lam et al. 2020) (at least based on pulsar observations, but DM is a value related to the ISM not the source so presumable this can also be true for FRBs)
* A careful discussion of the DM and its influence on the validity of our result will be essential for convincing radio astronomers
* I should be able to relate the delta t from the dedispersion equation to the observed slope. With that, I can just calculate directly what the drift error should be from the DM error

aug 17
===
* paper notes:
    * main text should include brief discussion of DM if possible, but the full argument can live in the "Materials and Methods"
    * I can write the entier supplementary info section which includes the Materials and Methods
        * I'd like to include every burst and autocorrelation if possible, labeled with the inferred drift measurement
        * a description of the error analysis (esp. the crazy equation for tw) should be given
        * Essentially summarize the document that processes the drifts and creates the trend figure; describe how the trend is found as well
        * Detail how we control for DM
* The heart of our problem is this:
    * We are telling people "if you dedisperse all the bursts from a repeater source to the same DM then you will see this trend between the drift rate and duration.", which is a true statement.
    * However, the first question is "Why should I dedisperse to the same DM given that the DM can vary per burst, and sometimes, like in FRB121102, vary in time?"
    * What is our answer to this? We can say that for some sources (like 180916 and 180814) the range of DMs is very narrow. We can also say it is reasonable to assume that the DM is a property of the medium and not the source.

aug 19
===
* met with fereshte and chris: proceed with plan regarding error bars

aug 20
===
* wip on refactoring for multi-dm error analysis

aug 27
===
* got data for dm vs. drift for frb121102 with ten trial DMs within the error range cited by Michilli.
* As a way of making our paper more convincing Martin suggested plotting angle vs duration instead of drift vs duration
    * this has the advantage of avoiding the discontinuity the drift experiences
    * shifting the DM on the angle vs duration plot will show that the DM just shifts the plot
    * I will also plot drift vs. DM and angle vs. DM
* drift range is huge and arbitrary due to discontinuity. get the range of angles, then use that as the angle error and calculate the drift error from that

aug 29
===
* for 180916 plot angle vs duration and angle vs trial dm. you already have the data for this

sept 4
===
* 1. get relationship of angle to tw from model, and add fits to angle plot
    1.2 how does tw change
* 2. start writing methods
* 3. process 180814 asap

sept 7
===
* burst 32 has an extremely long burst duration and small angle for ddm -1/2
    * the solver paramters make no sense (negative amplitude, etc.) so either exclude it or fix it
* the angle vs tw model is -atan(A/tw)

sept 9
===
* the angle vs tw model is actually atan(tw/A)

sept 11
===
* lol i missed a lot
    * fix the points on angle vs tw that have bad fits
    * check martin's deldta dm derivation and figure out delta theta
    * chris needs data for his idea
    * check martin's determination of beta nu_0 stuff
* ~burst 32 is still fucky on ddm = -0.5~ fixed

sept 14
===
* i have delta_DM, i need to know what delta theta is given that (which is presumably what Martin derived)
* found offset fits for angle vs duration
* wip on calculating deltatheta.. need to read the doc more

sept 15
===
* chris reproduced my results and showed that fit is optimal at a certain DM
* my dedispersion has an extra minus sign so when I dedispersed to -1/2, 1, and 2 pc/cm^3 what I actually did was dedisperse to 1/2, -1, and -2 pc/cm^3
    * fixed