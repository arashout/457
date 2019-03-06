import csv
from typing import List, Tuple, NamedTuple
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import pandas as pd
import seaborn as sns

import compute
import common

sns.set()

# def smooth(y, box_pts):
#     box = np.ones(box_pts)/box_pts
#     y_smooth = np.convolve(y, box, mode='same')
#     return y_smooth
 
def graph(
    tr: common.TrackResult, 
    angles: np.ndarray, 
    rpms: np.ndarray
    ):
    plt.figure(1)
    plt.subplot(2, 1, 1)
    plt.plot(tr.t, angles, '.')
    plt.ylabel('Angle [Degree]')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(tr.t, rpms, '.')
    plt.ylabel('RPM')
    plt.xlabel('Time [s]')
    plt.grid(True)

    plt.show()
