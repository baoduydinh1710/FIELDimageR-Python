import numpy as np
import pandas as pd
import sys
import rasterio
import matplotlib.pyplot as plt
from skimage.draw import line, polygon
from fieldCrop import crop


def fieldPolygon(mosaic, nPolygon=1, nPoint=4, polygonID=None, polygonData=None, ID=None,
                 cropPolygon=False, remove=False, plot=True, fast_plot=False, extent=False):
    num_band = mosaic.shape[0]
    print(num_band, " layers available", sep="")
    if nPoint < 4 | nPoint > 50:

        sys.exit("nPoint must be >= 4 and <= 50")
    for np in range(1, nPolygon):

        print("Select ", nPoint, " points around of polygon (",
              np, ") in the plots space.", sep="")
        c1 = []
        for i in range(1, nPoint):

            c1_1 = crop(mosaic)
            c1.append(c1_1["x"])
            c1.append(c1_1["y"])

        c1.append(c1[1])
        c1 = (dict("x", "y"))
        line(c1, (255, 0, 0), 3)
        p1 = pd.Polygons(dict(polygon(c1)), "x")
        f1 = pd.SpatialPolygons(dict(p1)), pd.DataFrame(
            z=1, row_names=tuple("x"))
        f1 = rasterio.warp.reproject(mosaic)
        if np == 1:
            fieldShape = f1
        if np != 1:
            fieldShape.append(f1)

    if cropPolygon:

        print("This step takes time, please wait ... cropping")
        r = pd.DataFrame.mask(mosaic, fieldShape, remove)

    if cropPolygon != True:

        r = crop(mosaic, fieldShape)

    fieldShape["data"] = pd.DataFrame(polygonID=chr(1, nPolygon))
    if polygonID != None:

        if len(polygonID) != nPolygon:

            sys.exit("Number of polygonID is different than nPolygon")

        fieldShape["data"] = pd.DataFrame(polygonID=chr(tuple(polygonID)))

    polygonData = pd.DataFrame(polygonData)
    if ID != None:

        sys.exit("Choose one ID (column) to combine polygonData with fiedShape")

    if len(ID) > 1:

        sys.exit("Choose only one ID")

    if polygonID != True:

        sys.exit("polygonID is necessary")

    if chr(ID) in chr(polygonData):

        sys.exit("ID: ", ID, " is not valid.")

    polygonData["polygonID"] = chr(polygonData[polygonData == ID])
    fieldShape["data"] = fieldShape["data"], polygonData
    fieldShape = rasterio.warp.reproject(r)
    Out = dict(fieldShape, r)
    if extent:

        fieldShape = extent(r), 'SpatialPolygons'
        fieldShape = pd.SpatialPolygonsDataFrame(fieldShape, pd.DataFrame(z=1))
        fieldShape = rasterio.warp.reproject(r)
        Out = dict(fieldShape)
    return Out
