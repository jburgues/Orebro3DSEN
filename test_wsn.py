#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 12:56:58 2018

@author: root
"""

import wsn_lite

W = wsn_lite.wsn('Exp01')
W.plotWind()
W.plotTempAndHumi()
W.plotMoxConcentration()
W.plotGasMap(map_type='mean', timeframe=[40, 45])
W.plotGasMap(map_type='bouts-freq', timeframe=[40, 45], bouts_hl=0.25, bouts_ampthresh=0.13)