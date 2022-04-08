import numpy as np
import sys
import rasterio
import cv2
import multiprocessing as mp
import math
import imutils


def onClick_rotate(event, x, y, flags, param):
    global cnt_1
    global l_1
    global count_1
    global image_1
    if event == cv2.EVENT_LBUTTONDOWN:
        l_1.append((x, y))
        cnt_1 += 1
        cv2.circle(image_1, (x, y), 5, (0, 0, 255), -1)
        count_1 = count_1 + 1
        if cnt_1 > 1:
            cv2.line(image_1, l_1[0], l_1[1], (0, 255, 0), 2, 20)


def point_from_mouse_rotate(mosaic, Point):
    global cnt_1
    global l_1
    global count_1
    global image_1
    cnt_1 = 0
    l_1 = []
    count_1 = 0
    image_1 = mosaic

    cv2.namedWindow("Rotate")
    cv2.setMouseCallback("Rotate", onClick_rotate)

    while count_1 < Point:
        cv2.imshow("Rotate", image_1)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    return l_1[:Point]


def fieldRotate(mosaic, theta=None, clockwise=True, h=False, n_core=None,
                DSMmosaic=None):
    num_band = mosaic.shape[2]
    print(num_band, " layer available", sep=" ")

    if DSMmosaic != None:
        if rasterio.warp.reproject(DSMmosaic) != rasterio.warp.reproject(mosaic):
            sys.exit("DSMmosaic and RGBmosaic must have the same projection CRS")
    if theta == None:
        print("Select 2 points from left to right on image in the plots space. Use any horizontal line in the field trial of interest as a reference.")
        c1 = point_from_mouse_rotate(mosaic, 2)
        if (c1[0][1] >= c1[1][1]) and (c1[1][0] >= c1[0][0]):
            theta = (math.atan2((c1[0][1] - c1[1][1]),
                     (c1[1][0] - c1[0][0]))) * (180 / 3.14)
        if (c1[1][1] >= c1[0][1]) and (c1[1][0] >= c1[0][0]):
            theta = (math.atan2((c1[1][1] - c1[0][1]),
                     (c1[1][0] - c1[0][0]))) * (180 / 3.14)
        if (c1[0][1] >= c1[1][1]) and (c1[0][0] >= c1[1][0]):
            theta = (math.atan2((c1[0][1] - c1[1][1]),
                     (c1[0][0] - c1[1][0]))) * (180 / 3.14)
        if (c1[1][1] >= c1[0][1]) and (c1[0][0] >= c1[1][0]):
            theta = (math.atan2((c1[1][1] - c1[0][1]),
                     (c1[0][0] - c1[1][0]))) * (180 / 3.14)
        if h != True:
            theta = 90 - theta
        if clockwise:
            theta = - theta
        theta = round(theta, 3)
        print("Theta rotation: ", theta, sep="")

    if n_core == None:
    
        #r = cv2.rotate ( mosaic , angle = theta )
        r = imutils.rotate_bound(mosaic, theta)
        cv2.imshow("rotate", r)
        cv2.waitKey(1)
        cv2.destroyAllWindows()
    return r
