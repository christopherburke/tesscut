#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 19:05:23 2018

@author: Christopher J. Burke
Demo a way to prestage ETE-6 FFIs into
subarray data cubes for efficient retrieval of cut out TPF generation
"""

import numpy as np
from astropy.io import fits
from astropy.stats import mad_std
import matplotlib.pyplot as plt
import h5py
import glob
import os
import math

def make_data_dirs(prefix, sector, camera, detector):
    secDir = 'S{0:02d}'.format(sector)
    localDir = os.path.join(prefix,secDir)
    if not os.path.exists(localDir):
        os.mkdir(localDir)
    camDir = os.path.join(localDir,'C{:1d}'.format(camera))
    if not os.path.exists(camDir):
        os.mkdir(camDir)
    detDir = os.path.join(camDir, 'D{:1d}'.format(detector))
    if not os.path.exists(detDir):
        os.mkdir(detDir)

    return detDir



if __name__ == "__main__":

# Hard code directories for ffi folder and output
    dirInputs = '<dir>'
    dirOutputs = '<dir>'
# subarrays are SUBSZxSUBSZ in size
    SUBSZ = 5
# work on a single camera and detector
    Camera = 1
    Detector = 1
# Sector assumed for the simulated ETE-6 data
    Sector = 14

# Get the list of all FFIs for the camera and detector combination
    fileList = sorted(glob.glob(os.path.join(dirInputs, '*{:1d}-{:1d}-0016-s_ffic.fits.gz'.format(Camera,Detector))))
    dataLen = len(fileList)
    cnt = 0
    # Get shape of ffi
    hdulist = fits.open(fileList[0])
    arr = np.array(hdulist[1].data)
    hdulist.close()
    shp = arr.shape
    nx = shp[0]
    ny = shp[1]
    
    # Make full storage array
    # Ran into memory problems trying to read in all three of the 
    #  Calibrated FFI cube, raw cube, and uncertainty cube
    # One will probably need to 
    cal = np.zeros((nx, ny, dataLen), dtype=np.float)
#    uncert = np.zeros_like(cal)
#    raw = np.zeros((nx, ny, dataLen), dtype=np.int)
    for i in range(len(fileList)-1300):
        if np.mod(i,10)==0:
            print('read ',i)
        hdulistcal = fits.open(fileList[i])
        cal[:,:,i] = np.array(hdulistcal[1].data, dtype=np.float)
#        uncert[:,:,i] = np.array(hdulistcal[i].data, dtype=np.float)
#        hdulistraw = fits.open(fileList[i].split('_')[0]+'_ffir.fits.gz')
#        raw[:,:,i] = np.array(hdulistraw[i].data, dtype=np.int32)
        hdulistcal.close()
        

    # now write out  subarrays  Does not handle cases
    #  where SUBSZ is not evenly divisible into image size
    cnt = 0
    prefix = make_data_dirs(dirOutputs, Sector, Camera, Detector)
    for curx in np.arange(0,nx, SUBSZ):
        for cury in np.arange(0,ny, SUBSZ):
            cnt = cnt + 1
            if (np.mod(cnt, 20))==0:
                print(cnt)
            xId = int(np.floor(curx/SUBSZ))
            yId = int(np.floor(cury/SUBSZ))
            calCube = cal[curx:curx+SUBSZ, cury:cury+SUBSZ,:]
#            uncertCube = uncert[curx:curx+SUBSZ, cury:cury+SUBSZ, :]
#            rawCube = raw[curx:curx+SUBSZ, cury:cury+SUBSZ,:]
            fileout = os.path.join(prefix, 'S{:2d}_C{:1d}_D{:1d}_{:04d}_{:04d}'.format(Sector, Camera, Detector, xId, yId))
#            np.savez_compressed(fileout, cal=calCube, uncert=uncertCube, raw=rawCube)
# save as compressed numpy storage.  Googling seems to indicate that numpy loads outputperform h5d loads.  But one should probably test whether loading from saved numpy saves is faster than saving and loading from h5d.
            np.savez_compressed(fileout, cal=calCube)

    print('hellow')        
