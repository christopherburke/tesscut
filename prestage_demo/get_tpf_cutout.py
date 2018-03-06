#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 19:05:23 2018

@author: Christopher J. Burke
recall a TPF based on prestaged FFI cutouts.

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

    dirStaged = '/pdo/users/cjburke/ete6/tpfcustom'

    SUBSZ = 5
    Camera = 1
    Detector = 1
    Sector = 14

    XSTRT = 100
    XWID = 10
    YSTRT = 120
    YWID = 10    
    xIds = int(math.floor(XSTRT/SUBSZ))
    xIde = int(math.floor((XSTRT+XWID)/SUBSZ))
    yIds = int(math.floor(YSTRT/SUBSZ))
    yIde = int(math.floor((YSTRT+YWID)/SUBSZ))
    
# Only demonstrate loading a single sub array too lazy to do the bookeeping to read in an arbitrary array based on the subarrays.    
    prefix = make_data_dirs(dirStaged, Sector, Camera, Detector)
    filetmp = os.path.join(prefix, 'S{:2d}_C{:1d}_D{:1d}_{:04d}_{:04d}.npz'.format(Sector, Camera, Detector, xIds, yIds))
    fin = np.load(filetmp)
    dataCube = fin['cal']
    shape = dataCube.shape

    output_filename = 'temp_foo.fits'
    # Package data into fits file
    # Make nearly empty primary data
    hdu = fits.PrimaryHDU([0.0])
    hdulist = fits.HDUList([hdu])
    # Add parameters to primary header
    prihdr = hdulist[0].header
    prihdr.set('TESTTPF','testing')
    prihdr.set('SECTOR',Sector)
    prihdr.set('CAMERA',Camera)
    prihdr.set('CCD',Detector)
    # Now add the data cube

    # This doesn't quite seem to be in the same format as what TPF uses
    #  TPF does use the second extension, but somehow the data cubes are sublists in the extension.
    tbhdu = fits.ImageHDU(data=dataCube, name='calibrated', do_not_scale_image_data=True)
    hdulist.append(tbhdu)

    hdulist.writeto('testfoo.fits')
    
    print('hellow')        
