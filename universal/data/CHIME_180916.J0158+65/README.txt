# Code

Code for chi-square test and H test:
https://github.com/fleaf5/R3_periodicity

Code for DFT search:
https://github.com/scottransom/event_DFT

Code for multinomial distribution:
https://github.com/dstndstn/chime-r3

Code for measuring the DM:
https://github.com/danielemichilli/DM_phase

Effelsberg data are searched and processed with PRESTO and SpS, which can be
found here:

https://github.com/scottransom/presto
https://github.com/danielemichilli/SpS


# Data

## TOA: R3_CHIME_TOA_20Feb4.txt

TOAs of all the chime bursts detected until Feb. 4th 2020 are listed in this
file.

## Exposure of CHIME: "R3_CHIME_exposure.npz"

The exposure of CHIME on FRB180916.J0158+65 from August 28th, 2018 to
September 30th, 2019 in 2s step. It can be folded in the same way as the TOAs
of bursts.  The way to load it is as follows:

    import numpy as np
    from astropy.time import Time
    a=np.load('R3_CHIME_exposure.npz')
    expo=a['expo_unit_day_1s_step']
    expoStart=a['tStart']
    expoStart=Time('2018-08-28T11:31:22.194')
    expo=expo+expoStart.mjd

## Effelsberg raw data are available by contacting the corresponding author.

## CHIME/FRB intensity and baseband waterfalls.

The former have file names "burst_*_16k_wfall.npz" and are stored at a
resolution of 16,384 frequency channels over 400 MHz with a 0.00098304-s time
resolution, dedispersed to 348.82 pc cm-3.

The latter have file names "burst_*_bb_1k_wfall.npz" and are stored at a
resolution of 1,024 frequency channels over 400 MHz with time resolution and
dedispersed to the DM as in Extended Data Figure 1 of the paper:
{40.96, 40.96, 20.48, 81.92} us and {348.78, 348.82, 348.82, 348.86} pc cm-3.
In all cases zapped channels due to RFI are replaced by `np.nan`. Data can be
accessed and displayed in Python as, e.g.:

    import matplotlib.pyplot as plt
    import numpy as np
    fname = "burst_9_bb_1k_wfall.npz"
    data = np.load(fname)
    wfall = data["wfall"]
    dt_s = data["dt_s"]
    center_freq_mhz = data["center_freq_mhz"]
    df_mhz = center_freq_mhz[1] - center_freq_mhz[0]
    plt.imshow(wfall, origin="lower", aspect="auto", interpolation="nearest",
               extent=(0, dt_s*wfall.shape[0], center_freq_mhz[0]-df/2.,
               center_freq_mhz[-1]+df/2.))
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [MHz]")


