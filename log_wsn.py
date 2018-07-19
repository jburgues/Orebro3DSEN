#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 11:09:06 2018

@author: root
"""

import csv
import numpy as np
import re
from os.path import join, dirname, realpath

class LogWsn(object):
    def __init__(self, log_name):
        self.dir_path = dirname(realpath(__file__))
        print(self.dir_path)
        self.log_name = log_name
        self.t_s = None
        self.c_ppm = None
        self.temp_deg = None
        self.humi_rh = None
        self.wdir_deg = None
        self.wspd_ms = None
        self.coords = None
     
    def parseLog(self):
        exp_folder = join(self.dir_path, 'logs', self.log_name) + '.csv'

        # Read the log and save it into a list    
        with open(exp_folder, 'r', encoding='mac_roman') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            data_with_header = list(csvreader)
        
        # Parse the header to find the coordinates of each sensor
        header = data_with_header[0]
        coords = []
        for i in range(len(header)):
            m = re.match('C_', header[i])
            if m:
                coords.append([int(header[i][2]), int(header[i][3]), int(header[i][4])])
        self.coords = np.array(coords)
        nr_of_sensors = len(coords)
        
        # Parse the rest of the data
        data = data_with_header[1:]
        nr_of_samples = len(data)
        
        self.t_s = np.zeros(nr_of_samples)  
        self.c_ppm = np.zeros((nr_of_samples, nr_of_sensors))  
        self.temp_deg = np.zeros((nr_of_samples, 4))  
        self.humi_rh = np.zeros((nr_of_samples, 4)) 
        self.wdir_deg = np.zeros(nr_of_samples)    
        self.wspd_ms = np.zeros(nr_of_samples)
        for i in range(nr_of_samples):
            self.t_s[i] = data[i][0]
            self.c_ppm[i,:] = data[i][1:28] # Concentration (ppm) [27 sensors]
            self.temp_deg[i,:] = data[i][28:32] # Temperature (deg) [4 sensors]
            self.humi_rh[i,:] = data[i][32:36] # Humidity (%r.h.) [4 sensors]
            self.wdir_deg[i] = data[i][36] # Wind direction (deg)
            self.wspd_ms[i] = data[i][37] # Wind speed (m/s)
            