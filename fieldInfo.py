import sys
import numpy as np
import multiprocessing as mp
from fieldCrop import crop


def fieldInfo(mosaic, fieldShape, fun="mean", plot=False, buffer=None,
              n_core=None, projection=True):
    if projection:
        if projection(fieldShape) != projection(mosaic):
            sys.exit(
                "fieldShape and mosaic must have the same projection CRS. Use fieldRotate() for both files.")
    num_band = len(mosaic[0])
    print("Extracting: ", num_band, " layers.", sep="")
    print("You can speed up this step using n.core=",
          mp.cpu_count(), " or less.", sep="")
    CropPlot = crop(x=mosaic, y=fieldShape)
    if n_core == None:

        plotValue = np.extract(x=CropPlot, y=fieldShape,
                               fun=eval(text=fun), buffer=buffer)
    if n_core > mp.cpu_count():
        sys.exit(" 'n.core' must be less than ", mp.cpu_count(), sep="")
    fieldShape.append(fieldShape["data"])
    fieldShape.append(plotValue)
    Out = dict(fieldShape, plotValue, CropPlot)
    return Out
