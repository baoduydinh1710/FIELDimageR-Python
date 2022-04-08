import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import rasterio
from joblib import Parallel, delayed
import multiprocessing as mp


def pc(x, p):
    return pd.DataFrame(objArea=(len(x[x == p]) / len(x[pd.Series(x).isna()])), objNumCell=len(x[x == p]), naNumCell=len(x[pd.Series(x).isna()]))


def x():
    return pc(int(x[1]))


def fieldArea(mosaic, areaValue=0, fieldShape=None, buffer=None, core=None, plot=True, narm=False):
    num_band = mosaic.shape[0]
    print(num_band, " layer available", sep="")
    print("You can speed up this step using n.core=",
          os.cpu_count(), " or less.", sep="")
    if num_band > 1:
        sys.exit(
            "Only mask mosaic with values of 1 and 0 can be evaluated, please use the mask output from fieldMask()")
    if fieldShape == None:
        print("Evaluating the object area percentage for the whole image...")
        porarea = pc(x=mosaic, p=areaValue)
        print("The percentage of object area is ", 100 *
              (round(porarea . objArea, 2)), "%", sep="")
        Out = porarea
    if fieldShape == None:
        print("Evaluating the object area percetage per plot...")
        if core == None:
            extM = pd.Series.str.extract(x=mosaic, y=fieldShape, buffer=buffer)
            extM = set(1, len(fieldShape))
            porarea = pd.DataFrame(extM.append(pc))
        if core != None:
            if core > os.cpu_count():
                sys.exit(" 'n.core' must be less than ",
                         os.cpu_count(), sep="")
            num_cores = mp.cpu_count()
            Parallel(n_jobs=num_cores)
            for i in range(1, len(fieldShape)):
                single = fieldShape[i]
                CropPlot = i[mosaic, single]
                pd.Series.str.extract(x=CropPlot, y=single, buffer=buffer)
            extM.set(1, len(fieldShape))
            porarea = pd.DataFrame(
                extM.append(pc(int(x[1]))))
        fieldShape["data"] = fieldShape["data"].append(porarea)
        Out.append(porarea)
        Out.append(fieldShape)
    return Out
