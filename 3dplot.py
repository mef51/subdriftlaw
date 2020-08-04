import numpy as np
import scipy.stats
import scipy.odr
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.cm as cm
import matplotlib as mpl
from tqdm import tqdm
import functools
print = functools.partial(print, flush=True) # print doesn't happen til script ends so force it to flush... windows thing?
import pandas as pd


datafile = '3dplotdata.csv'
include = ['M1','M2','M3','M4','M5','M6','M7','M8','M9','M10','M11','M12','M13','M14','M15','M16','M9a','M9b','M10a','M10b','G11A','G11D','G11A1a','G11A1b','G11A2','G11A3']
driftdata = pd.read_csv(datafile, index_col=0)
driftdata = driftdata.loc[include]

print(driftdata)

xs = driftdata['tau_w_ms']
ys = driftdata['center_f']
zs = driftdata['drift (mhz/ms)']
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(xs, ys, zs, marker='o')


ax.set_xlabel('tau_w_ms')
ax.set_ylabel('center_f')
ax.set_zlabel('drift (mhz/ms)')

plt.show()
