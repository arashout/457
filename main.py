import cv2
import sys
import csv
import time
import os

import numpy as np
import pandas as pd

import common
import compute
from draw import draw
from track import track
from graph import graph

VIDEO_FRAMERATE = 30

if __name__ == '__main__':
    if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
        raise ValueError("Need to pass a video file")
    flipped = len(sys.argv) > 2
    video_path = sys.argv[1]
    # 1. TRACKING
    try:
        tr = common.getTR(common.getBasename(video_path))
    except FileNotFoundError:
        tr = track(video_path, flipped)

    # 2. Fit Circle (Find center of rotation and radius)
    cfr = compute.fit_circle(tr.x, tr.y)
    # 3. Compute angles and rpms needed for drawing and graphs
    angles = compute.compute_angles(tr.x - cfr.c_x, tr.y - cfr.c_y)
    rpms = compute.compute_rpms(tr, cfr.r)

    df = pd.DataFrame({
        'x': tr.x,
        'y': tr.y,
        't': tr.t,
        'theta': angles,
        'rpms': rpms
    })
    df.to_csv(os.path.join(common.DATA_DIR, common.getBasename(video_path)) + '.csv')
    # 4: Draw on video
    if input("Enter 's' to skip:\n") != 's':
        draw(sys.argv[1], tr, cfr, angles, rpms, flipped)

    # 4. Output graphs
    graph(tr, angles, rpms)
