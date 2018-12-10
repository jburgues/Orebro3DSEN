# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 11:54:39 2017

@author: jburgues
"""
from __future__ import division
import numpy as np   
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import log_wsn  
from bouts import compute_bouts_RT
try:
    from windrose import WindroseAxes
    windrose_installed = True
except ImportError:
    windrose_installed = False
    print('Warning: Windrose package not detected (to install it: pip install windrose). Windrose plot will not be shown')
    pass # module doesn't exist, deal with it.
  
class wsn:

    def __init__(self, log_name):
        L=log_wsn.LogWsn(log_name)
        L.parseLog()
        
        self.t_s = L.t_s
        self.c_ppm = L.c_ppm
        self.temp_deg = L.temp_deg
        self.humi_rh = L.humi_rh
        self.wdir_deg = L.wdir_deg
        self.wspd_ms = L.wspd_ms
        self.coords = L.coords
        self.nr_of_samples, self.nr_of_sensors = L.c_ppm.shape
        self.nr_of_nodes = L.temp_deg.shape[1]
        self.fs = 1/np.mean(np.diff(self.t_s))
        self.T = self.t_s[[0,-1]]
      
    # def _getTimeIndex(self, T, t_tol=None):  
    # Extract temporal indices corresponding to a time frame.
    # T: 1x2 vector specifying the start and end times (minutes) of the time 
    # frame (e.g. T=[5, 10]). 
    def _getTimeIndex(self, timeframe=None): 
        """
        Internal method to obtain the sample index from a time vector.
        """         
        t_min = self.t_s / 60.0
        
        if timeframe is None:
            timeframe = t_min[[0, -1]].flatten()
            
        t_idx = (t_min > timeframe[0]) & (t_min < timeframe[1]) 
            
        return t_idx.flatten()
    
    def _smooth_signal(signal, winsize, plot=False):
        """
        Internal method to smooth a signal using a Gaussian filter
        """
        
        df = pd.DataFrame(signal)
        signal_smooth = df.rolling(winsize, win_type='gaussian', min_periods=1, center=True)
        signal_smooth = signal_smooth.mean(std=winsize).values[:,0]
        
        return signal_smooth
    
    # def plotTempAndHumi(self, ax=None, smooth=False):
    # Plot temperature and humidity versus time
    # ax: axes of the figure (if empty, a new figure is created)
    # smooth: boolean value indicating if the signals should be smoothed (by
    # defult it is False). 
    def plotTempAndHumi(self, ax=None, timeframe = None, smooth=False):
        if ax is None:
            fig, ax = plt.subplots(2, 1)
        else:
            fig = plt.gcf()
            
        tidx = self._getTimeIndex(timeframe)
        temp = self.temp_deg[tidx,:]
        humi = self.humi_rh[tidx,:]
        t_s = self.t_s[tidx]
        
        if smooth: # smooth signals
            winsize_s = 20
            winsize = int(round(winsize_s * self.fs))
            temp_deg = np.zeros_like(temp)
            humi_rh = np.zeros_like(humi)
            
            for i in range(self.nr_of_nodes):
                temp_deg[:,i] = self._smooth_signal(temp[:,i], winsize)
                humi_rh[:,i] = self._smooth_signal(humi[:,i], winsize)
        else:
            temp_deg = temp
            humi_rh = humi
            
        plt.suptitle('Environmental conditions')
        ax[0].plot(t_s/60, temp_deg)
        ax[0].set_xlim(t_s[[0, -1]]/60 + 0.5*np.array([-1,1]))
        ax[0].set_ylabel('Temperature (deg)')
        
        ax[1].plot(t_s/60, humi_rh)
        ax[1].set_xlim(t_s[[0, -1]]/60 + 0.5*np.array([-1,1]))
        ax[1].set_xlabel('Time (min)')
        ax[1].set_ylabel('Humidity (%r.h.)')
        
        # Fine-tune figure; make subplots closer to each other and hide x-ticks 
        # for all but the bottom plot.
        fig.subplots_adjust(hspace=0.1)
        plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)
        node_leg = ['Node' + str(i+1) for i in range(self.nr_of_nodes)]
        lg = ax[0].legend(node_leg, bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                   ncol=4, mode="expand", borderaxespad=0.)
        return lg
    
    # def plotWind(self, tmax=None, bins = 6, ax=None):
    # Plot wind direction and speed versus time, optionally using a wind rose.
    # ax: axes of the figure (if empty, a new figure is created)
    # smooth: boolean value indicating if the signals should be smoothed (by
    # defult it is False).
    def plotWind(self, ax=None, timeframe=None, windrose = True, bins = 6):
        if ax is None:
            fig, ax = plt.subplots(2, 1)
        else:
            fig = plt.gcf()
            
        plt.suptitle('Wind')
        tidx = self._getTimeIndex(timeframe)
        wspd_ms = self.wspd_ms[tidx]
        wdir_deg = self.wdir_deg[tidx]
        t_s = self.t_s[tidx]
        lod_ms = 0.01 # limit of detection WindSonic anemmometer (m/s)
        
        #wdir = wdir - 90
        ax[0].plot(t_s/60, wspd_ms)
        ax[0].set_ylabel('Speed (m/s)')
        ax[0].set_xlabel('Time (min)')
        ax[0].axhline(lod_ms, c='r', ls='--')

        ax[1].plot(t_s/60, wdir_deg)
        ax[1].set_xlabel('Time (min)')
        ax[1].set_ylabel('Direction (deg)')
        
        # Wind rose
        figrose = plt.figure(figsize=(4,4))
        ws = wspd_ms[wspd_ms>lod_ms]
        wd = wdir_deg[wspd_ms>lod_ms]
        ax_rose = WindroseAxes.from_ax(fig=figrose)
        ax_rose.bar(wd, ws, normed=True, opening=0.8, edgecolor='white', 
                    blowto=False, bins=bins)
        ax_rose.set_legend()
        ax_rose.tick_params(axis='x', labelsize=12)
        ax_rose.tick_params(axis='y', labelsize=12)
        ax_rose.legend(fontsize=12, loc='best')
        
        return fig, figrose
    
    def plotMoxConcentration(self, ax=None, sensor='all', timeframe=None, smooth=False):
        if not ax or ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
        else:
            fig = plt.gcf()
            
        tidx = self._getTimeIndex(timeframe)
        c_ppm = self.c_ppm[tidx,:]
        t_s = self.t_s[tidx]
            
        if smooth: # smooth signals
            winsize_s = 20
            winsize = int(round(winsize_s * self.fs))
            c_ppm_smooth = np.zeros_like(c_ppm)            
            for i in range(self.nr_of_sensors):
                c_ppm_smooth[:,i] = self._smooth_signal(c_ppm[:,i], winsize)
                c_ppm = c_ppm_smooth
        
        plt1 = ax.plot(t_s/60, c_ppm)
        ax.set_ylabel('Instantenous concentration (ppm)')
        ax.set_xlabel('Time (min)')
        plt.xlim([-1, self.t_s[-1]/60 + 1])
 
        return fig, ax, plt1

    def _computeGasMap(self, mapType, timeframe, hl=0.25, bout_ampl=0):   
        t_idx = self._getTimeIndex(timeframe)
        t_s = self.t_s[t_idx]
        c_ppm = self.c_ppm[t_idx, :]
            
        # Build grid of mean concentration
        nx = 3
        ny = 3
        nz = 3
        gridmap = np.zeros([nz, ny, nx], dtype=float)
        for i in range(self.nr_of_sensors):
            if mapType is 'mean':
                val = np.mean(c_ppm[:,i])
            elif mapType is 'median':
                val = np.median(c_ppm[:,i])
            elif mapType is 'max':
                val = np.max(c_ppm[:,i])
            elif mapType is 'var':
                val = np.var(c_ppm[:,i])
            elif mapType.startswith('bouts'):
                # bout count    
                filtered_bouts, amps = compute_bouts_RT(c_ppm[:,i], self.fs, hl, ampthresh=bout_ampl)
                pbc = filtered_bouts.shape[0]
                if mapType.endswith('freq'):
                    t_diff = (t_s[-1]-t_s[0])/60 # minutes
                    val = pbc/t_diff # bout frequency (bouts/minute)
                elif mapType.endswith('ampl'):
                    val = np.mean(amps)
            
            x,y,z = self.coords[i,:]
            gridmap[z,ny-y-1,x] = val
         
        return gridmap
    
    
    def _plotGasMapSlice(self, fig, ax, gmap_slice, xlbl = True, ylbl = True, 
                         interp='spline36', cm = 'YlOrRd', cb_lbl = 'ppm', 
                         norm=None, clims=None):
        if clims is None:
            clims = [0, np.max(gmap_slice)]
        if norm is None:
            norm=mpl.colors.Normalize(clims[0],clims[1],True)
            
        im_map = ax.imshow(gmap_slice, extent=[0,6,0,6], aspect='equal', 
                        norm=norm, origin='upper',interpolation = interp, cmap=cm)
            
        ax.invert_xaxis()
        ax.invert_yaxis() 
        ax.tick_params(labelsize=9)
        #ax.xaxis.tick_top()
        plt.setp(ax, xticks=[0, 2, 4, 6], yticks=[0, 2, 4, 6])
        if ylbl:
            ax.set_ylabel('Y (m)', fontsize=9)
        else:
            plt.setp(ax.get_yticklabels(), visible=False)
        if xlbl:
            ax.set_xlabel('X(m)', fontsize=9)    
        else:
            plt.setp(ax.get_xticklabels(), visible=False)
        #ax_z.xaxis.set_label_position('top')

        # color bar 
        if cb_lbl is not None:
            cax = fig.add_axes([0.95, 0.1, 0.03, 0.79])
            cb = fig.colorbar(im_map, cax=cax) 
            cb.set_label(cb_lbl)
            
        return im_map
    
    def plotGasMap(self, ax=None, map_type='mean', timeframe=None, bouts_hl=0.25, 
                   bouts_ampthresh=0.1, interp='spline36', cm = 'YlOrRd', 
                   norm=None, clims=None):
        """
        Plots one of the following maps: mean, median, max, var, bouts-freq or bouts-ampl
        in the timeframe specified. The bouts parameters are "bouts_hl" (half-life time (s))
        and "bouts_ampthresh" (amplitude threshold (ppm/s)).
        """
        
        gmap = self._computeGasMap(map_type, timeframe, bouts_hl, bouts_ampthresh) 
        
        cb_lbl='None'
        if map_type == 'mean':
            cb_lbl = 'Mean response (ppm)'
        elif map_type == 'median':
            cb_lbl = 'Median response (ppm)'
        elif map_type == 'max':
            cb_lbl = 'Max response (ppm)'
        elif map_type == 'var':
            cb_lbl = 'Variance of response (ppm^2)'
        elif map_type == 'bouts-freq':
            cb_lbl = 'Bout frequency (bouts/min)'
        elif map_type == 'bouts-ampl':
            cb_lbl = 'Mean bout amplitude (ppm/s)'
                
        if not ax or ax is None:
            fig,ax = plt.subplots(3,1, figsize=(4.0, 10.0), dpi=150)
        else:
            fig = plt.gcf()
        
        if clims is None:
            clims = [0, np.max(gmap)]
            
        z_real = [0.45, 1.2, 2.23]
        
        for z in range(3):            
            im = self._plotGasMapSlice(fig, ax[z], gmap[z,:,:], 
                                       clims=clims, cm=cm, norm=norm, cb_lbl=cb_lbl)
            ax[z].text(-0.5, 2.0, 'Z = {0:.2f} m'.format(z_real[z]), 
                       rotation=90) 
        
        
 
        return ax, im


