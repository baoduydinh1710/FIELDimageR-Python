import sys
import numpy as np
import pandas as pd
def fieldMap(fieldPlot, fieldColumn, fieldRow):
  if len ( fieldPlot ) != len ( fieldRow ) or len ( fieldPlot ) != len ( fieldColumn ) or len ( fieldColumn ) != len ( fieldRow )  :
    sys.exit ( "Plot, Column and Row vectors must have the same length." ) 
      
  map = []
  for i in range(1 , len( fieldRow ) ):
      
      r1 = chr ( fieldPlot [ fieldRow == i ] [  ( int ( fieldColumn [ fieldRow == i ] )).sort() ] ) 
      map.append(r1)
      
  return map