#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 12:56:58 2018

@author: root
"""

import wsn_lite

W = wsn_lite.wsn('2017-10-13 Exp1')
W.plotWind()
W.plotTempAndHumi()
W.plotMoxConcentration()
W.plotGasMap(map_type='mean', timeframe=[15, 20])