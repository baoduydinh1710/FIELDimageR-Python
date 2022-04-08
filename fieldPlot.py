import shutil
import cv2
import sys
import matplotlib.pyplot as plt
import numpy as np


def fieldPlot(fieldShape, fieldAttribute, mosaic=None, min_lim=None, max_lim=None,  alpha=0.5, legend_position="right", na_color="gray", classes=5, round=3, horiz=False):
    if len(fieldAttribute) > 1:
        sys.exit("Choose ONE attribute")
    attribute = fieldShape["data"]
    if fieldAttribute and attribute:
        sys.exit("Attribute ", fieldAttribute,
                 " is not valid. Choose one among: ", np.unique(attribute), sep="")
    val = int(fieldShape["data"][shutil.which(
        attribute and fieldAttribute)[1]])
    if min_lim == None and max_lim == None:

        if int(min_lim) and int(max_lim):

            sys.exit("Limit need to be numeric e.g. min.lim=0 and max.lim=1")

        if min_lim > min(val):

            sys.exit(
                "Choose minimum limit (min.lim) equal or lower than ", min(val), sep="")

        if max_lim < max(val):

            sys.exit(
                "Choose maximum limit (max.lim) equal or greater than ", max(val), sep="")

        val = dict(min_lim, val, max_lim)

    na_pos = val.is_na()
    rr = range(val)
    svals = (val - rr[1]) / np.diff(rr)
    svals[na_pos] = 0
    valcol = cv2.cvtColor((svals)/255, cv2.COLOR_BGR2RGB)
    valcol[na_pos] = cv2.cvtColor(na_color/255, cv2.COLOR_GRAY2RGB)
    if min_lim != None and max_lim != None:
        valcol = valcol[dict(1, len(valcol))]
    if mosaic != None:
        if fieldShape != mosaic:
            sys.exit(
                "fieldShape and mosaic must have the same projection CRS. Use fieldRotate() for both files.")
    pos = round(min(val), max(val), classes)
    if any(na_pos):
        pos = dict(pos, "NA")
    col = col = dict(np.transpose(cv2.cvtColor(
        col=na_color, alpha=False)) / 255, alpha=alpha)
    if any(na_pos):
        col = dict(col, np.transpose(cv2.cvtColor(
            col=na_color, alpha=False)) / 255, alpha=alpha)
    plt.legend(legend_position, fieldAttribute,
               legend=pos, fill=col, bty="n", horiz=horiz)
    plt.figure(0)
    plt.plot(legend_position, fieldAttribute,
             linestyle="--", color="blue",
             marker="s",  # squares
             label="Data_Sample_1")
    plt.title("Example plot")
    plt.legend(loc="upper left")
    plt.show()
