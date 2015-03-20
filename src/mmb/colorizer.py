'''
Created on Mar 15, 2015

@author: enu
'''

from mmb.color_tuple import ColorTuple
import numpy as np

class Colorizer(object):
    '''
    Converts an image array[ydim,xdim] of int(0..maxValue)
    to an image array[ydim,xdim] of [r, g, b] using an extrapolated
    color palette of a given size.
    '''
    
    def __init__(self, paletteSize=100):
        self.palette = ColorTuple().palette(paletteSize, (0, 300.0 / 360, 1.0, 0.0), (int(0.15*paletteSize), 250.0 / 360, 1.0, 0.5), (paletteSize-1, 300.0 / 360, 1.0, 1.0))

    def colorize(self, frame):
        '''
        Uses numpy histogram, cumulative sum, array multiplication and division operations
        as well as indexing of arrays by other arrays for colorizing the frame.
        See http://docs.scipy.org/doc/numpy/user/basics.indexing.html#indexing-multi-dimensional-arrays 
        '''
        maxValue = frame.max()
        histogram,_ = np.histogram(frame, bins=maxValue+1)
        cumulative = np.cumsum(histogram, dtype=float)
        colorlookup = np.array(cumulative / frame.size * (len(self.palette) - 1), dtype=int)
        return self.palette[colorlookup[frame]]
