import numpy as np
import pandas as pd
from sklearn import metrics
def fieldAUC(data, x,y, trait, keep, method = "trapezoid" , frame = "long"):
  DataAUC = [] 
  for i in range(1 , len (trait)):
    trait1 = trait [ i ] 
    print( "Evaluating AUC for " , trait1 , sep = "" ) 
    Plot = chr ( np.unique ( data["PlotName"] ) ) 
    DataAUC_1 = None
    for a1 in range(1, len(Plot)):
      D1 = data[chr(data["PlotName"])==Plot[a1]]
      x1 = dict ( x["start"] , int( D1.DAP ))
      y1 = dict ( y["start"] , int ( D1 [ trait1 ] ))
      if frame == "long":
        DataAUC.append(np.array(D1 [ 1 ,dict( keep.columns)] ), 
                            TRAIT=trait1, AUC = metrics.AUC (x = x1[pd.Series(y1).isna()], 
                                                             y = y1[pd.Series(y1).isna()],
                                                             method = method))
      if frame == "wide":
        if i==1:
          DataAUC = DataAUC.append(pd.matrix(D1 [ 1 ,dict( keep.columns)] ), 
                             metrics.AUC (x = x1[pd.Series(y1).isna()], 
                                                             y = y1[pd.Series(y1).isna()],
                                                             method = method))
        if i != 1:
          DataAUC_1 = DataAUC_1.append(metrics.AUC( x = x1[pd.Series(y1).isna()], 
                                                             y = y1[pd.Series(y1).isna()],
                                                             method = method)) 
      if frame == "wide": 
        DataAUC =  DataAUC.append(DataAUC_1 ) 
        DataAUC.columns.values[np.dim(DataAUC)[2]] = trait1.split("AUC", sep = " ")
  namesAUC = DataAUC.columns.values()
  namesAUC [ 1 , len(keep.columns)] = dict(keep.columns)
  DataAUC = pd.DataFrame( np.array ( dict( DataAUC ) , ncol = np.dim ( DataAUC ) [ 2 ] , nrow = np.dim (DataAUC) [1]))
  DataAUC.columns.values = namesAUC
  return DataAUC