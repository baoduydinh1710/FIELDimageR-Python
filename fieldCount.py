import numpy as np
import pandas as pd
import sys
import statistics
import multiprocessing as mp
from skimage.segmentation import watershed
from tabulate import tabulate
from fieldCrop import crop


def fieldCount(mosaic, fieldShape, value=0, minSize=0.01, n_core=None, pch=16,
               cex=0.7, col="red", na_rm=False):
    num_band = mosaic.shape[0]
    if num_band > 1:
        sys.exit(
            "Only mask with values of 1 and 0 can be processed, use the mask output from fieldMask()")
    mosaic = crop(fieldShape)
    print("Identifying objects... ")
    print("You can speed up this step using n.core=",
            mp.cpu_count(), " or less.", sep="")
    mask = np.array(mosaic.mask)
    dd = mask
    mosaic.watershed = watershed(dd)
    if n_core == None:
        extM = np.extract(watershed, fieldShape)

    def table(x):
        return tabulate(x)

    def function(x):
        if len(x) == 0:
            return None
        pos = None
        for i in range(1, len(x)):
            pos = pos.append(watershed == x[i])

        return ord, pos

    objects = table(list(map(statistics(extM))))
    cent = int(list(map(statistics(objects))))
    objectsPosition = function(list(map(statistics(cent))))
    objectSel = []
    objectReject = []
    for j in range(1, len(cent)):
        x1 = objects[j]
        y = objectsPosition[j]
        x = None
        PS = None
        PR = None

        for i in range(2, len(x1)):
            x = tuple(x, round(100 * (x1[i] / sum(x1, na_rm=na_rm)), 3))
            x = x[y["seqName"]]
            if np.dim(np.array(y["Position"]))[2] == 1:

                PS = pd.DataFrame(
                    objectArea=x[x >= minSize], x=y[" Position"][1][x >= minSize], y=y["Position"][2][x >= minSize])
                PR = pd.DataFrame(
                    objectArea=x[x < minSize], x=y[" Position"][1][x < minSize], y=y["Position"][2][x < minSize])

            if np.dim(np.array(y["Position"]))[2] != 1:

                PS = pd.DataFrame(
                    objectArea=x[x >= minSize], x=y["Position"][x >= minSize, 1], y=y["Position"][x >= minSize, 2])
                PR = pd.DataFrame(
                    objectArea=x[x < minSize], x=y["Position"][x < minSize, 1], y=y["Position"][x < minSize, 2])
            PS = None
            PR = None
            objectSel[j] = PS
            objectReject[j] = PR
    if len(objectSel) != len(cent):
        objectSel[len(cent) + 1] = None
        objectReject[len(cent) + 1] = None
        objectSel[len(cent) + 1] = None
        objectReject[len(cent) + 1] = None

    def lenobject(x):
        return len(x["objectArea"])
    field = lenobject(list(map))
    fieldShape.data.fieldCount = field
    print("Number of objects: ", sum(field), sep="")
    pd.DataFrame(objectSel)
    Out = [field, fieldShape, mosaic, objectSel, objectReject]
    return Out
