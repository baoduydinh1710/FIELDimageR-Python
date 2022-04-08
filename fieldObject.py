import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import rasterio
from skimage.transform import rescale
import cv2
import geopandas as gpd
from osgeo import gdal
from shapely.geometry import Point, Polygon

import math
from fieldCrop import crop


def clump(arr):
    started = False
    out = []
    for item in arr:
        if item == '-':
            started = True
            out[-1] += item
        elif started:
            out[-1] += item
            started = False
        else:
            out.append(item)
    return out


def segments(poly):
    """A sequence of (x,y) numeric coordinates pairs """
    return zip(poly, poly[1:] + [poly[0]])


def area(poly):
    """A sequence of (x,y) numeric coordinates pairs """
    return 0.5 * abs(sum(x0*y1 - x1*y0
                         for ((x0, y0), (x1, y1)) in segments(poly)))


def perimeter(poly):
    """A sequence of (x,y) numeric coordinates pairs """
    return abs(sum(math.hypot(x0-x1, y0-y1) for ((x0, y0), (x1, y1)) in segments(poly)))


def fieldObject(mosaic, fieldShape=None, minArea=0.01, areaValue=0, perimeter=False):
    num_band = mosaic.shape[0]
    Objects = []
    print(num_band, " layer available", sep="")
    if num_band > 1:

        sys.exit(
            "Only mask mosaic with values of 1 and 0 can be evaluated, please use the mask output from fieldMask()")

    print("Identifying objects ... ")
    if fieldShape == None:
        r = mosaic
        fieldShape = gpd.SpatialPolygons(fieldShape)
    Out = []
    numObjects = None
    for i in range(1, np.dim(fieldShape)[1]):
        CropPlot = crop(mosaic)
        SP = Polygon(clump(CropPlot == areaValue))
        sps2 = pd.DataFrame(SP["polygons"])
        print("Taking measurements...")
        obj_extent = []
        x_position = []
        y_position = []
        single_obj = []
        Dimension = None
        Polygons = None
        xy1 = []
        xy2 = []
        for i in range(1, len(sps2)):
            sps3 = sps2[i]
            sps3 = mosaic
            P = Polygon(sps3)
            area = np.contourArea(sps3)
            if area > minArea:
                xy1.append(sps3[1], sps3[2],
                           (sum(sps3[3, 4])) / 2, sum(sps3[3, 4]) / 2)
                xy2.append(sum(sps3[1, 2]) / 2,
                           sum(sps3[1, 2]) / 2, sps3[3], sps3[4])
            obj_extent[i] = sps3
            x_position[i] = xy1
            y_position[i] = xy2
            Dimension.append((area, dict(xy1)), dict(xy2))
            single_obj[i] = sps3
            if Polygons != None:
                Polygons.append(P)
                Objects.append(sps3)
            if Polygons == None:
                Polygons = P
                Objects = sps3
        Objects_df = pd.DataFrame(Objects)
        Polygons_df = pd.DataFrame(Polygons)
        print("Number of objects on plot", i, len(Objects), sep=" ")
        if np.dim(fieldShape)[1] == 1:
            Out = dict(
                mosaic=mosaic,
                Dimension=pd.DataFrame(Dimension),
                numObjects=dict(
                    numObjects,
                    len(Objects)),
                Objects=Objects,
                Polygons=Polygons,
                single_obj=single_obj,
                obj_extent=obj_extent,
                x_position=x_position,
                y_position=y_position)
        if np.dim(fieldShape)[1] != 1:
            Out[[i]] = dict(mosaic=CropPlot,
                            Dimension=pd.DataFrame(Dimension),
                            numObjects=dict(numObjects,
                                            len(Objects)),
                            Objects=Objects,
                            Polygons=Polygons,
                            obj_extent=obj_extent,
                            x_position=x_position,
                            y_position=y_position)
    if np.dim(fieldShape)[1] != 1:
        Out = fieldShape["fieldID"]
    if np.dim(fieldShape)[1] != 1:
        if "PlotName" and chr(fieldShape):
            Out = fieldShape["PlotName"]
    if perimeter:
        perimeter1 = perimeter(Out["Objects"])
        box = perimeter(Out["Polygons"])
        Out["Dimension"].append(perimeter1)
        Out["Dimension"].append(box)

    return Out
