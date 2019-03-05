from scipy import optimize, empty, newaxis, signal
import numpy as np
import math

import common

RAD_PER_SECOND_TO_RPM = 60/(2*math.pi)
DEG_PER_SECOND_TO_RPM = 60/360

def fit_circle(x: np.ndarray, y: np.ndarray) -> common.CircleFitResult:
    def calc_R(xc, yc):
        """ calculate the distance of each data points from the center (xc, yc) """
        return np.sqrt((x-xc)**2 + (y-yc)**2)

    def f_2b(c):
        """ calculate the algebraic distance between the 2D points and the mean circle centered at c=(xc, yc) """
        Ri = calc_R(*c)
        return Ri - Ri.mean()

    def Df_2b(c):
        """ Jacobian of f_2b
        The axis corresponding to derivatives must be coherent with the col_deriv option of leastsq"""
        xc, yc     = c
        df2b_dc    = empty((len(c), x.size))

        Ri = calc_R(xc, yc)
        df2b_dc[0] = (xc - x)/Ri                   # dR/dxc
        df2b_dc[1] = (yc - y)/Ri                   # dR/dyc
        df2b_dc    = df2b_dc - df2b_dc.mean(axis=1)[:, newaxis]

        return df2b_dc

    x_m = x.mean()
    y_m = y.mean()
    center_estimate = x_m, y_m
    center_2b, _ = optimize.leastsq(f_2b, center_estimate, Dfun=Df_2b, col_deriv=True)

    xc_2b, yc_2b = center_2b
    Ri_2b        = calc_R(*center_2b)
    R_2b         = Ri_2b.mean()
    
    return common.CircleFitResult(int(xc_2b), int(yc_2b), int(R_2b))

def compute_angles(x: np.ndarray, y: np.ndarray):
    """
    NOTE: Require normalized x and y by subtracting center of circle
    """
    degrees = np.degrees(np.arctan2(y, x))
    return (degrees + 360) % 360

def reject_outliers(data, m=3):
    return data[abs(data - np.mean(data)) < m * np.std(data)]


def compute_velocity(p: np.ndarray, t: np.ndarray) -> np.ndarray:
    dp = np.diff(p)
    dt = np.diff(t)
    return dp*(1/dt)

def compute_rpms(tr: common.TrackResult, r: int) -> np.ndarray:
    vx = compute_velocity(tr.x, tr.t)
    vy = compute_velocity(tr.y, tr.t)
    v = np.sqrt((vx)**2 + (vy)**2)
    v = np.append(v, 0)
    av = v/r
    return av * RAD_PER_SECOND_TO_RPM

def compute_rpms2(tr: common.TrackResult, cfr: common.CircleFitResult) -> np.ndarray:
    angles = compute_angles(tr.x - cfr.c_x, tr.y - cfr.c_y)
    da = np.diff(angles)
    dt = np.diff(tr.t)
    rpms = np.divide(da, dt) * DEG_PER_SECOND_TO_RPM
    rpms = np.append(rpms, 0)
    return rpms