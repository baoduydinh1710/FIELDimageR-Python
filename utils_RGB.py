import numpy as np

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))*255

def RGB_rescale(mosaic, num_band):
  for i in range( 1 , num_band ) :
        NormalizeData(mosaic[i])
  return mosaic 