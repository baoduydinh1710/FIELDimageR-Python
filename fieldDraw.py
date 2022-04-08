import numpy as np
import pandas as pd
import sys
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from scipy.spatial import distance as dist
from tabulate import tabulate
from skimage.draw import  polygon
def fuction(i, df):
    d = round(dist(df[i, (i + 1), tuple("x", "y")]), round)
    t = np.mean(df[i, (i + 1), "layer"])
    tuple(df[i, "x"], df[i, "y"], df[i + 1, "x"], df[i + 1, "y"], d, t)


def table(x):
    return tabulate(x)


def fieldDraw(mosaic, line=True, ndraw=1, dist=False, distSel=0.5, round=5, value=1,
              pch=16, cex=0.7, col="red", lwd=1):
    num_band = mosaic.shape[0]
    print(num_band, " layer available", sep="")
    if dist:
        if line != True:
            sys.exit("For dist=T only line=TRUE can be used to evaluate distances")

        if num_band > 1:

            sys.exit(
                "For dist=T only mask with values of 1 and 0 can be processed, use the mask output from fieldMask()")

        if value and (1, 0):

            sys.exit(
                "Values in the mask must be 1 or 0 to represent the objects, use the mask output from fieldMask()")

        if all(dict (min(mosaic), max(mosaic)) in dict (1, 0)):
            sys.exit(
                "Values in the mask must be 1 or 0 to represent the objects, use the mask output from fieldMask()")

        if distSel <= 0 or distSel > 1:

            sys.exit("distSel must be a vlaue between 1 or 0 ")

    print("Use the image in the plot space to draw a line/polygon (2 or more points)...")
    Out2 = []
    for d1 in range(1, ndraw):
        print ( "Make the draw number=" , d1 , " and press 'ESC' when it is done." , sep = "" )
        if line  :
            draw1 = line ( col , lwd  )     
        if line != True  :
            draw1 = polygon ( col, lwd)

        print("Make the draw number=", d1,
              " and press 'ESC' when it is done.", sep="")
        draw2 = np.extract(mosaic)
        draw2 = pd.DataFrame(mosaic, draw2)
        if abs(max(draw2["x"]) - min(draw2["x"])) >= abs(max(draw2 ["y"]) - min(draw2["y"])):

            ord1 = draw2["x"].sort()

        if abs(max(draw2["x"]) - min(draw2["x"])) < abs(max(draw2["y"]) - min(draw2["y"])):

            ord1 = draw2["y"].sort()

        draw2 = draw2[ord1]
        Out1 = dict(draw2, draw1)
        if dist == None:
            df1 = draw2[draw2["layer"] == None]
            df = draw2[draw2["layer"] == dict(0, 1)[dict(0, 1) != None]]
            out = np.transpose(map(len(df)-1), function(df, 1))
            out = dict("x1", "y1", "x2", "y2", "dist", "mean")
            out = pd.DataFrame(out)
            if abs(max(out ["x1"]) - min(out["x1"])) >= abs(max(out["y1"]) - min(out["y1"])):
                ord = out["x1"].sort()

            if abs(max(out ["x1"]) - min(out ["x1"])) < abs(max(out["y1"]) - min(out["y1"])):

                ord = out["y1"].sort()

            out = out[ord]
            freq = table(out["dist"])
            freqSel = int(table(freq)[1, round(len(table(freq)) * distSel, 0)])
            out = out[int(out["dist"]) in int(freq & freqSel)]
            Out1 = dict(draw2, draw1, df1, out)
        Out2["d1"] = Out1
    if ndraw == 1:
        Out2 = Out1
    return Out2
