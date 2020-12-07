# Sad Trombone

This repository contains code for 

* computing autocorrelations of dynamic spectra of fast radio bursts
* fitting rotatable 2d gaussians to said autocorrelations
* producing a fit to the trend between the sub-burst drift rate and the duration
* supplemental and diagnostic figures. For figures of every burst and the corresponding fit used in the first paper see [`figures/with_drift/`](https://github.com/mef51/sadtrombone/tree/master/figures/with_drift). The second paper already includes every autocorrelation.
* The [`universal`](https://github.com/mef51/sadtrombone/tree/master/universal) folder contains the analysis done for the second paper.

Key files
===
Many of the scripts and notebooks included in the repo are my rough work and experiments.
The following files are what ended up published and are probably the ones you would want to look at:

* [`ProcessBursts.ipynb`](https://github.com/mef51/sadtrombone/blob/master/ProcessBursts.ipynb): Processes bursts from FRB121102
* [`Process180814.py`](https://github.com/mef51/sadtrombone/blob/master/universal/Process180814.py): Processes bursts from FRB180814.J0422+73
* [`CHIME180916_RemixedDM.ipynb`](https://github.com/mef51/sadtrombone/blob/master/universal/CHIME180916_RemixedDM.ipynb): Processes bursts from FRB180916.J0158+65, and allows for small DM variations in the bursts. 
* [`DriftvsDuration_universal.ipynb`](https://github.com/mef51/sadtrombone/blob/master/universal/DriftvsDuration_universal.ipynb): Computes the dynamical model's details and produces the key plot of sub-burst drift rate vs. sub-burst duration. 

Please open an issue for any specific help or questions you might have.

Example Usage
===
(wip)

Related publications:
===
 * [A simple relationship for the spectro-temporal structure of bursts from FRB 121102](https://arxiv.org/abs/2008.02395)    
Fereshteh Rajabi, Mohammed A. Chamma, Christopher M. Wyenberg, Abhilash Mathews, Martin Houde

 * [A shared law between sources of repeating fast radio bursts](https://arxiv.org/abs/2010.14041)    
Mohammed A. Chamma, Fereshteh Rajabi, Christopher M. Wyenberg, Abhilash Mathews, Martin Houde
