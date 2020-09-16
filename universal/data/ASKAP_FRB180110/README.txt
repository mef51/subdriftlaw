This collection accompanies the paper "The dispersion-brightness relation for
fast radio bursts from a wide-field survey".

It contains 3 directories:


full_scans/
-----------
ASKAP CRAFT search mode data for all beams of the entire scan in which each
FRB was found. It contains a directory for each FRB. The directory contains 36
files from the detecting antenna in SIGPROC filterbank format
(http://sigproc.sourceforge.net/sigproc.pdf). The filterbanks are 8-bit,
pseudo-stokes-I (XX+YY) with a mean near 128 and standard deviation around
18. There are 336x1 MHz channels, ordered as lower sideband with the first
(highest) frequency of 1488 MHz. The sampling interval is 1.265ms.

The filename is in the format of:
YYYY-MM-DD-HH:MM:SS_0000000000000000.000000.BB.fil

Where YYYY, MM, DD, HH, MM, SS are the year, month, day, hour, minute and
second of the start of the recording, and BB is the 0-based beam number.

Please note the start MJDs in the filterbanks are in TAI, not UTC as is the convention.

The FRB directories also contain .hdr files. They are in ASCII format and containing various
pieces of telescope metadata which accompany the scan. The meaning of most
headers should be obvious - if not, please contact the author (below).

cutouts/
--------
As for full_scans/, but only, a 20s cutout around the FRB.


positions/
----------
This directory contains maps of the uncertainty region of each FRB. The method
used to obtain the fits is described in Bannister et al. 2017, ApJL, 841,
12. For each FRB there is a file in FITS format with a world coordinate
system, so it can be easily over-plotted over normal astronomical images
using your favourite astronomical software. Each pixel in the image is the
a-posteriori probability density of the FRB arriving at the location of the pixel. To obtain
percent-containment contours, you will need to integrate down from the peak.


Keith Bannister <keith.bannister@csiro.au>- 7 August 2018



