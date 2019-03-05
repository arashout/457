import cv2
import sys
import csv
import time
import os
import numpy as np
import pickle

from common import TrackResult, VIDEO_FRAMERATE, DATA_DIR, getBasename

def track(video_path: str) -> TrackResult:
    tracker = cv2.TrackerCSRT_create()
    video_path = sys.argv[1]
    video = cv2.VideoCapture(video_path)
    video.open(video_path)
    
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()

    bbox = cv2.selectROI(frame, False)
    bbox_width = bbox[2]
    bbox_height = bbox[3]

    ok = tracker.init(frame, bbox)

    x = []
    y = []
    t = []

    start_time = time.time()
    elapsed_time = 0
    
    while True:
        ok, frame = video.read()
        if not ok:
            break

        timer = cv2.getTickCount()
        ok, bbox = tracker.update(frame)

        # Calculate actual time taken in video
        deltaTick = (cv2.getTickCount() - timer)
        fps = cv2.getTickFrequency() / deltaTick
        elapsed_time += fps/VIDEO_FRAMERATE * deltaTick / cv2.getTickFrequency()

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox_width), int(bbox[1] + bbox_height))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

            # Store bounding box center as it moves
            x.append(int(bbox[0] + bbox_width/2))
            y.append(int(bbox[1] + bbox_height/2))
            t.append(elapsed_time)
            
            cv2.imshow("Tracking", frame)
            # Exit if ESC pressed
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                cv2.destroyWindow("Tracking")

        else:
            print("WARNING: could not update tracker at {0}".format(elapsed_time))
            cv2.destroyAllWindows()
    
    cv2.destroyAllWindows()
    
    tr = TrackResult(
        np.asarray(x, dtype=np.int), 
        np.asarray(y, dtype=np.int),
        np.asarray(t)
        )
    basename = getBasename(video_path)
    with open(os.path.join(DATA_DIR, basename) + 'tr', 'wb') as f:
        pickle.dump(tr, f)


    return tr 