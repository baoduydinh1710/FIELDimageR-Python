import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import rasterio
from skimage.transform import rescale
import cv2
import geopandas as gpd
from rasterio.crs import CRS
import multiprocessing as mp
import matplotlib.pyplot as plt
from scipy.spatial import distance as dist
from skimage.segmentation import watershed
import os
from tabulate import tabulate
from fieldCrop import crop


def fieldMask(mosaic, Red=1, Green=2, Blue=3, RedEdge=None, NIR=None, mask=None, index="HUE",
              myIndex=None, cropValue=0, cropAbove=True, projection=True, DSMmosaic=None,
              DSMcropAbove=True, DSMcropValue=0, plot=True):
    Out = []
    num_band = mosaic.shape[0]
    print(num_band, " layer available", sep="")
    if mask == None:
        if num_band < 3:
            sys.exit(
                "At least 3 bands (RGB) are necessary to calculate indices available in FIELDimageR")
        if RedEdge == None:
            if num_band < 4:
                sys.exit("RedEdge and/or NIR is/are not available in your mosaic")
        B = mosaic[Red]
        G = mosaic[Green]
        R = mosaic[Blue]
        if RedEdge != None:
            RE = mosaic[3]

        if NIR != None:

            NIR1 = mosaic[3]

        if myIndex == None:

            print("Mask equation myIndex = ", myIndex, sep="")
            Blue = B
            Green = G
            Red = R
            if NIR != None:
                NIR = NIR1
            if RedEdge != None:
                RedEdge = RE
        mr = np.arctan(2*(B-G-R)/30.5*(G-R))
    if mask != None:
        mask = []
        if len(mask[0]) > 1:
            sys.exit("Mask must have only one band.")
        mr = mask
        mosaic = crop(mosaic)
        if projection:

            mosaic = rasterio.warp.reproject(mosaic, mr, method="ngb")

    if cropAbove:

        m = mr > cropValue

    if cropAbove != None:

        m = mr < cropValue
    Out.append(mosaic)
    Out.append(m)
    if DSMmosaic != None:

        DSMmosaic = crop(DSMmosaic)
        if DSMcropAbove:

            mDEM = m > DSMcropValue

        if DSMcropAbove != None:

            mDEM = m < DSMcropValue

        if projection:

            DSMmosaic = rasterio.warp.reproject(DSMmosaic, mDEM, method='ngb')
        DSMmosaic = mask(DSMmosaic, mDEM, maskvalue=True)
        Out = dict(newMosaic=mosaic, mask=m, DSM=DSMmosaic)
    return Out
