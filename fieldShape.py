import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import rasterio
from skimage.transform import rescale
import cv2 
from shapely.geometry import Polygon
import geopandas as gpd
from rasterio.crs import CRS
from fieldCrop import crop, point_from_mouse
from osgeo import gdal
def onClick(event,x,y,flags,param):  
    global cnt_shape
    global l_shape
    global count_shape
    global image_shape
    if event == cv2.EVENT_LBUTTONDOWN:
        l_shape.append((x,y))
        cnt_shape += 1  
        cv2.circle(image_shape,(x,y),5,(0,0,255),-1) 
        count_shape = count_shape + 1 
        if cnt_shape % 4 == 0: 
            cv2.line(image_shape, l_shape[0], l_shape[1], (0,255,0),2, 20)
            cv2.line(image_shape, l_shape[1], l_shape[2], (0,255,0),2, 20) 
            cv2.line(image_shape, l_shape[2], l_shape[3], (0,255,0),2, 20) 
            cv2.line(image_shape, l_shape[3], l_shape[0], (0,255,0),2, 20) 

def point_from_mouse_shape(mosaic, Point):
    global cnt_shape
    global l_shape
    global count_shape 
    global image_shape
    global resized_shape
    cnt_shape = 0 
    l_shape = [] 
    count_shape = 0
    image_shape = mosaic
    # scale_percent = 30 # percent of original size
    # width = int(image_shape.shape[1] * scale_percent / 100)
    # height = int(image_shape.shape[0] * scale_percent / 100)
    # dim = (width, height)
    # resized = cv2.resize(image_shape, dim, interpolation = cv2.INTER_AREA)
    cv2.namedWindow("Crop") 
    cv2.setMouseCallback("Crop", onClick)

    while count_shape <= Point: 
        cv2.imshow("Crop", image_shape)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    return l_shape[:Point]
def crop_shape(img, c1):
    x1,y1 = c1[0]
    x2,y2 = c1[1]
    x3,y3 = c1[2]
    x4,y4 = c1[3]
    top_left_x = min([x1,x2,x3,x4])
    top_left_y = min([y1,y2,y3,y4])
    bot_right_x = max([x1,x2,x3,x4])
    bot_right_y = max([y1,y2,y3,y4])
    image = img[top_left_y:bot_right_y, top_left_x:bot_right_x]
    return image
class data_linewidth_plot():
    def __init__(self, x, y, **kwargs):
        self.ax = kwargs.pop("ax", plt.gca())
        self.fig = self.ax.get_figure()
        self.lw_data = kwargs.pop("linewidth", 1)
        self.lw = 1
        self.fig.canvas.draw()

        self.ppd = 72./self.fig.dpi
        self.trans = self.ax.transData.transform
        self.linehandle, = self.ax.plot([],[],**kwargs)
        if "label" in kwargs: kwargs.pop("label")
        self.line, = self.ax.plot(x, y, **kwargs)
        self.line.set_color(self.linehandle.get_color())
        self._resize()
        self.cid = self.fig.canvas.mpl_connect('draw_event', self._resize)

    def _resize(self, event=None):
        lw =  ((self.trans((1, self.lw_data))-self.trans((0, 0)))*self.ppd)[1]
        if lw != self.lw:
            self.line.set_linewidth(lw)
            self.lw = lw
            self._redraw_later()

    def _redraw_later(self):
        self.timer = self.fig.canvas.new_timer(interval=10)
        self.timer.single_shot = True
        self.timer.add_callback(lambda : self.fig.canvas.draw_idle())
def fieldShape(mosaic, ncols = 10, nrows = 10, nPoint = 4, fieldMap = None, fieldData = None,
                       ID = None, theta = None, plot = True, fast = False, extent = False):
  num_band = mosaic.shape[0]
  print( num_band , " layer available" , sep = "" )
  if extent != True:
    if nPoint < 4 or nPoint > 50 :
      sys.exit("nPoint must be >= 4 and <= 50")
  if extent != True:
    print("Select ",nPoint," points at the corners of field of interest in the plots space.",sep = "")
    cv2.imshow("mosaic image", mosaic)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    c = point_from_mouse_shape(mosaic, nPoint)
    c1 = crop_shape(mosaic,c)
    if fieldData: 
      fieldData = pd.DataFrame( fieldData ) 
      if  ID == None  :
          sys.exit( "Choose one ID (column) to combine fieldData with fiedShape" ) 
      if len( ID ) > 1  :
          sys.exit( "Choose only one ID" ) 
      if fieldMap == None  :
          sys.exit( "fieldMap is necessary, please use function fieldMap()" ) 
      if  chr( ID ) in chr ( fieldData  )  :
        sys.exit( "ID: " , ID , " is not valid." ) 
      fieldData.PlotName = chr( fieldData [ 'fieldData' == ID ] ) 
      fieldShape.Data =  pd.concat (fieldShape.data,fieldData)
    Out = fieldShape 
    return Out