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
* [`driftrate.py`](https://github.com/mef51/sadtrombone/blob/master/example/driftrate.py) and [`driftlaw.py`](https://github.com/mef51/sadtrombone/blob/master/example/driftlaw.py) are extracted libraries that can do all the processing in the above notebooks. These may be extracted into their own package eventually. See the example usage below 

Please open an issue for any specific help or questions you might have or email me mchamma at uwo (dot) ca

Example Usage
===
[`Example.ipynb`](https://github.com/mef51/sadtrombone/blob/master/example/Example.ipynb) contains a minimal example of processing a burst and computing the dynamical model quantities.

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import driftrate, driftlaw

burst = np.load('frb180916_burst18.npy')

# CHIME spectral parameters
params = {
    'dt_s'            : 0.00098304,
    'df_mhz'          : 400/1024,
    'nchan'           : 1024,
    'freq_bottom_mhz' : 400.1953125,
    'freq_top_mhz'    : 800.1953125,
    'dm'              : 348.82
}

targetDM = 348.82
ddm = targetDM - params['dm']
burstid = 'CHIME1'
burst = driftrate.dedisperse(burst, ddm, params['freq_bottom_mhz'], params['df_mhz'], params['dt_s']*1000)    
drift, drift_error, popt, perr, theta, red_chisq, center_f = driftrate.processBurst(burst, burstid, params['df_mhz'], params['dt_s']*1000, params['freq_bottom_mhz'], p0=[])
# plt.savefig('{}corr.png'.format(burstid))

# Export to csv using pandas
outputdata = pd.DataFrame(index=[burstid], 
                          columns=['amplitude', 'xo', 'yo', 'sigmax', 'sigmay', 'theta', 'amp_error', 'xo_error', 'yo_error', 'sigmax_error', 'sigmay_error', 'angle_error',
                                  'drift (mhz/ms)', 'drift error (mhz/ms)', 'angle', 'center_f', 'red_chisq', 'time_res', 'freq_res'])

outputdata.loc['CHIME1'] = [*popt, *perr, drift, drift_error, theta, center_f, red_chisq, params['dt_s'], params['df_mhz']]
outfile = 'outputexample.csv'
outputdata.to_csv(outfile, index_label="name")
outputdata
```



Related publications:
===
 * [A simple relationship for the spectro-temporal structure of bursts from FRB 121102](https://academic.oup.com/mnras/article-abstract/498/4/4936/5903289), also on [arxiv](https://arxiv.org/abs/2008.02395)    
 Fereshteh Rajabi, Mohammed A. Chamma, Christopher M. Wyenberg, Abhilash Mathews, Martin Houde

 * [A shared law between sources of repeating fast radio bursts](https://arxiv.org/abs/2010.14041)    
 Mohammed A. Chamma, Fereshteh Rajabi, Christopher M. Wyenberg, Abhilash Mathews, Martin Houde


