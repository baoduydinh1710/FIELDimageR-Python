
import sys
import csv


def fieldIndex(mosaic, Red=1, Green=2, Blue=3, RedEdge=None, NIR=None, index="HUE",
               myIndex=None, plot=True):
    Ind = csv.reader(file=("extdata", "Indices.txt",
                     "FIELDimageR"), header=True, sep="	")
    num_band = mosaic.shape[0]
    print(num_band, " layers available", sep="")
    if num_band < 3:
        sys.exit("At least 3 bands (RGB) are necessary to calculate indices")
    if RedEdge != None or NIR != None:

        if num_band < 4:

            sys.exit("RedEdge and/or NIR is/are not available in your mosaic")

    IRGB = chr(Ind["index"])
    if index != None:
        sys.exit("Choose one or more indices")
    if index not in IRGB:
        sys.exit("Index: ", index[index and IRGB != True],
                 " is not available in FIELDimageR")
    NIR_RE = chr(Ind.index[Ind.band]) and dict("RedEdge", "NIR")
    if any(NIR_RE and index) and NIR == None:
        sys.exit("Index: ", NIR_RE[NIR_RE and index],
                 " needs NIR/RedEdge band to be calculated", sep="")
    B = mosaic[Red]
    G = mosaic[Green]
    R = mosaic[Blue]
    if RedEdge != None:
        
        RE = mosaic[4]
        mosaic.append(RedEdge)

    if NIR != None:

        NIR1 = mosaic[4]
        mosaic.append(NIR)

    for i in range(1, len(index)):

        mosaic[num_band +
               i] = eval(text=chr(Ind["eq"][chr(Ind["index"]) == index[i]]))
        mosaic = chr([num_band + i])

    if myIndex != None:

        Blue = B
        Green = G
        Red = R
        if NIR != None:
            NIR = NIR1
        if RedEdge != None:
            RedEdge = RE
        for m1 in range(1, len(myIndex)):

            mosaic["layers"][(len(mosaic["layers"]) + 1)
                             ] = eval(chr(myIndex[m1]))
            if len(myIndex) == 1:
                mosaic.append(mosaic["layer"]["myIndex"])
            if len(myIndex) > 1:
                mosaic.append(m1)
    return mosaic
