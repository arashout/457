import cv2
import sys
import csv
import time
import os
import numpy as np
import math
from typing import Optional

from common import VIDEO_FRAMERATE, CircleFitResult, TrackResult, addText 
import compute

TEXT_X = 100
TEXT_Y_START = 100
TEXT_SPACING = 80

def draw(
    video_path: str,
    tr: TrackResult,
    cfr: CircleFitResult,
    angles: np.ndarray,
    rpms: np.ndarray,
):
    fps = VIDEO_FRAMERATE
    x = tr.x
    y = tr.y
    t = tr.t

    video = cv2.VideoCapture(video_path)
    video.open(video_path)

    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()

    circle_center = (cfr.c_x, cfr.c_y)
    r = cfr.r

    i = -1
    while i < (x.shape[0] - 1):
        # Read a new frame
        ok, frame = video.read()
        i += 1
        if not ok:
            raise ValueError(
                "Could not read frame! At frame: {0} Time: {1}".format(i, t[i]))

        # Draw 0-angle reference arrow, current angle arrow and fitted circle
        cv2.arrowedLine(frame, circle_center,
                        (circle_center[0]+r, circle_center[1]), (255, 255, 255), 2)
        cv2.arrowedLine(frame, circle_center, (x[i], y[i]), (0, 255, 255), 2)
        cv2.circle(frame, circle_center, r, (0, 255, 0), 2, 3)

        # Text

        # Text Background
        cv2.rectangle(
            frame, 
            (TEXT_X - 50,0),
            (TEXT_X + 5*TEXT_SPACING, TEXT_Y_START + 4*TEXT_SPACING),
            (10,10,10),
            -1
        )
        # Angle
        addText(frame, "Angle: {0}".format(int(angles[i])), (TEXT_X, TEXT_Y_START))
        # RPM
        addText(frame, "RPMs: {0}".format(int(rpms[i])), (TEXT_X, TEXT_Y_START+TEXT_SPACING))

        # Time
        addText(frame, "Time: {0}".format(round(t[i], 2)), (TEXT_X, TEXT_Y_START+2*TEXT_SPACING))

        # Frames per second
        addText(frame, "FPS: {0}".format(fps), (TEXT_X, TEXT_Y_START+3*TEXT_SPACING))

        # Display result
        resized = cv2.resize(frame, dsize=None, fx=0.5,
                             fy=0.5, interpolation=cv2.INTER_LINEAR)
        cv2.imshow("Drawing", resized)

        time.sleep(1/fps)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
            cv2.destroyWindow("Drawing")
        elif k == 113:  # q
            fps = max(1, fps // 2)
        elif k == 119: # w
            fps = fps * 2
        elif k == -1:
            continue
    
    video.release()
    cv2.destroyAllWindows()