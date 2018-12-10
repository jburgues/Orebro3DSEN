#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 12:56:58 2018

@author: root
"""
import pandas as pd
import numpy as np

def compute_bouts(sd, sd_thr=0.0):
    """
    Internal method to compute the "bouts" in the EWMA-filtered time-derivative (sd) of the smoothed signal. 
    The argument sd_thr is the threshold that determines the positive part of the derivative.
    """
    sd_pos = sd >=sd_thr # positive part of the derivative
    signchange = np.diff(np.array(sd_pos, dtype=int)) #Change neg->pos=1, pos->neg=-1.
    pos_changes = np.nonzero(signchange > 0)[0]
    neg_changes = np.nonzero(signchange < 0)[0]
    # have to ensure that first change is positive, and every pos. change is complemented by a neg. change
    if pos_changes[0] > neg_changes[0]: #first change is negative
        #discard first negative change
        neg_changes = neg_changes[1:]
    if len(pos_changes) > len(neg_changes): # lengths must be equal
        difference = len(pos_changes) - len(neg_changes)
        pos_changes = pos_changes[:-difference]
    posneg = np.zeros((2,len(pos_changes)))
    posneg[0,:] = pos_changes
    posneg[1,:] = neg_changes
    return posneg

def compute_bouts_RT(raw_signal, fs=10, hl=0.3, ampthresh=0.0, sd_thr=0.0): 
    """
    Real-time bout computation.
    The Gaussian smoothing filter of Schmuker's algorithm is replaced by an EWMA filter.
    The argument "raw_signal" is the unsmoothed sensor response, "fs" is the sampling frequency (Hz), 
    "hl" is the half-life time (s) and "sd_thr" is the threshold to determine when the derivative is positive.
    """
    s = pd.ewma(raw_signal, halflife=hl*fs, adjust=False, ignore_na=True)
    sd = fs * np.diff(s)
    hl = 0.3
    sds = pd.ewma(sd, halflife=hl*fs, adjust=False, ignore_na=True)
    bouts = compute_bouts(sds, sd_thr)
    bouts = bouts.astype(int).T
    amps = np.hstack((np.diff(sds[bouts]).flat))
    bouts_filt = bouts[amps>ampthresh,:]
    amps_filt = amps[amps>ampthresh]
    return bouts_filt, amps_filt