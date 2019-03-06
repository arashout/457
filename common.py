import math
import cv2
import numpy as np
import os
import pickle

from typing import NamedTuple, List, Tuple

DATA_DIR = 'data'
VIDS_DIR = 'vids'
VIDEO_FRAMERATE = 30

class TrackResult(NamedTuple):
    x: np.ndarray
    y: np.ndarray
    t: np.ndarray

class CircleFitResult(NamedTuple):
    c_x: int
    c_y: int
    r: int

class AllResults(NamedTuple):
    tr: TrackResult
    cfr: CircleFitResult
    angles: np.ndarray
    rpms: np.ndarray

def addText(img, text: str, position: Tuple[int, int], size = 1):
    cv2.putText(
        img,
        text,
        position,
        cv2.FONT_HERSHEY_COMPLEX,
        size,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )

def getTR(basename: str) -> TrackResult:
    with open(os.path.join(DATA_DIR, basename) + 'tr', 'rb') as f:
        return pickle.load(f)

# TODO: Implement
def getAllResults(basename: str) -> AllResults:
    raise NotImplementedError()

def getBasename(filepath: str) -> str:
    return os.path.splitext(os.path.basename(filepath))[0]
