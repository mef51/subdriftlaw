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
