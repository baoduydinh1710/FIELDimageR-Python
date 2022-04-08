# import numpy as np
# import sys
# import cv2 
# import pandas as pd
# def onClick(event,x,y,flags,param):  
#     global cnt_crop
#     global l_crop
#     global count_crop
#     global image_crop
#     if event == cv2.EVENT_LBUTTONDOWN:
#         l_crop.append((x,y))
#         cnt += 1  
#         cv2.circle(resized_crop,(x,y),5,(0,0,255),-1) 
#         count = count + 1 
#         if cnt % 4 == 0: 
#             cv2.line(resized_crop, l_crop[0], l_crop[1], (0,255,0),2, 20)
#             cv2.line(resized_crop, l_crop[1], l_crop[2], (0,255,0),2, 20) 
#             cv2.line(resized_crop, l_crop[2], l_crop[3], (0,255,0),2, 20) 
#             cv2.line(resized_crop, l_crop[3], l_crop[0], (0,255,0),2, 20) 

# def point_from_mouse(mosaic, Point):
#     global cnt_crop
#     global l_crop
#     global count_crop
#     global image_crop
#     global resized_crop
#     cnt_crop = 0 
#     l_crop = [] 
#     count_crop = 0
#     image_crop = mosaic
#     scale_percent = 30 # percent of original size
#     width = int(image_crop.shape[1] * scale_percent / 100)
#     height = int(image_crop.shape[0] * scale_percent / 100)
#     dim = (width, height)
#     resized_crop = cv2.resize(image_crop, dim, interpolation = cv2.INTER_AREA)
#     cv2.namedWindow("Crop") 
#     cv2.setMouseCallback("Crop", onClick)

#     while count_crop <= Point: 
#         cv2.imshow("Crop", resized_crop)
#         cv2.waitKey(1)
#     cv2.destroyAllWindows()
#     return l_crop[:Point]
# def crop(img, c1):
#     x1,y1 = c1[0]
#     x2,y2 = c1[1]
#     x3,y3 = c1[2]
#     x4,y4 = c1[3]
#     top_left_x = min([x1,x2,x3,x4])
#     top_left_y = min([y1,y2,y3,y4])
#     bot_right_x = max([x1,x2,x3,x4])
#     bot_right_y = max([y1,y2,y3,y4])
#     image = img[top_left_y:bot_right_y, top_left_x:bot_right_x]
#     return image
    
# def resize_mosaic(mosaic):
#     scale_percent = 30 # percent of original size
#     width = int(mosaic.shape[1] * scale_percent / 100)
#     height = int(mosaic.shape[0] * scale_percent / 100)
#     dim = (width, height)
#     resized = cv2.resize(mosaic, dim, interpolation = cv2.INTER_AREA)
#     # cv2.imshow("Window", resized)
#     return resized
# def fieldCrop(mosaic, path, nPoint = 4,  remove = False):
#   num_band = mosaic.shape[0]
#   print( num_band , " layers available" , sep = "" ) 
#   if nPoint < 4 | nPoint > 50  :
#       sys.exit ( "nPoint must be >= 4 and <= 50" )  
#   print ( "Select " , nPoint , " points at the corners of field of interest in the plots space." , sep = "" ) 
#   c1 = point_from_mouse(path, nPoint)
#   mosaic = cv2.imread(path)
#   mosaic = resize_mosaic(mosaic)
#   if c1 != None: 
#       if  remove != True  :
#           r = crop(mosaic, c1) 
#       if remove  :
#           r = pd.DataFrame.mask ( x = mosaic , mask = c1 , inverse = remove )             
#   return r 
import numpy as np
import sys
import cv2 
import pandas as pd

def onClick(event,x,y,flags,param):  
    global cnt_crop
    global l_crop
    global count_crop
    global image_crop
    if event == cv2.EVENT_LBUTTONDOWN:
        l_crop.append((x,y))
        cnt_crop += 1  
        cv2.circle(resized_crop,(x,y),5,(0,0,255),-1) 
        count_crop = count_crop + 1 
        if cnt_crop % 4 == 0: 
            cv2.line(resized_crop, l_crop[0], l_crop[1], (0,255,0),2, 20)
            cv2.line(resized_crop, l_crop[1], l_crop[2], (0,255,0),2, 20) 
            cv2.line(resized_crop, l_crop[2], l_crop[3], (0,255,0),2, 20) 
            cv2.line(resized_crop, l_crop[3], l_crop[0], (0,255,0),2, 20) 

def point_from_mouse(path, Point):
    global cnt_crop
    global l_crop
    global count_crop
    global image_crop
    global resized_crop
    cnt_crop = 0 
    l_crop = [] 
    count_crop = 0
    image_crop = cv2.imread(path) 
    scale_percent = 30 # percent of original size
    width = int(image_crop.shape[1] * scale_percent / 100)
    height = int(image_crop.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_crop = cv2.resize(image_crop, dim, interpolation = cv2.INTER_AREA)
    cv2.namedWindow("Crop") 
    cv2.setMouseCallback("Crop", onClick)

    while count_crop <= Point: 
        cv2.imshow("Crop", resized_crop)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    return l_crop[:Point]
def crop(img, c1):
    x1,y1 = c1[0]
    x2,y2 = c1[1]
    x3,y3 = c1[2]
    x4,y4 = c1[3]
    top_left_x = min([x1,x2,x3,x4])
    top_left_y = min([y1,y2,y3,y4])
    bot_right_x = max([x1,x2,x3,x4])
    bot_right_y = max([y1,y2,y3,y4])
    image = img[top_left_y:bot_right_y, top_left_x:bot_right_x]
    cv2.imshow("Resized image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return image
    
def resize_mosaic(mosaic):
    scale_percent = 30 # percent of original size
    width = int(mosaic.shape[1] * scale_percent / 100)
    height = int(mosaic.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(mosaic, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow("Window", resized)
    return resized
def fieldCrop(mosaic, path, nPoint = 4,  remove = False):
  num_band = mosaic.shape[0]
  print( num_band , " layers available" , sep = "" ) 
  if nPoint < 4 | nPoint > 50  :
      sys.exit ( "nPoint must be >= 4 and <= 50" )  
  print ( "Select " , nPoint , " points at the corners of field of interest in the plots space." , sep = "" ) 
  c1 = point_from_mouse(path, nPoint)
  mosaic = cv2.imread(path)
  mosaic = resize_mosaic(mosaic)
  if c1 != None: 
      if  remove != True  :
          r = crop(mosaic, c1) 
      if remove  :
          r = pd.DataFrame.mask ( x = mosaic , mask = c1 , inverse = remove )     
           
  return r 