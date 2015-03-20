'''
Created on Mar 3, 2015

Author: Converted to Python by Esko Nuutila from Scala original by Teemu Lehtinen
'''
import numpy as np

class ColorTuple(object):
    '''
    Provides methods to handle colors as tuples.
    '''
    def __init__(self):
        pass
    
    def HSLtoRGB(self, hsl):
        '''
        Converts HSL color tuple (float, float, float) to RGB color tuple.
        http://www.niwa.nu/2013/05/math-behind-colorspace-conversions-rgb-hsl
        '''
        def Int255(amount): return int(max(0.0, min(1.0, amount)) * 255)
        
        def RGB255(rgb): return (Int255(rgb[0]), Int255(rgb[1]), Int255(rgb[2]))
        
        if hsl[1] == 0.0:
            RGB255((hsl[2], hsl[2], hsl[2]))
        t1 = (hsl[2] * (1.0 + hsl[1])) if (hsl[2] < 0.5) else hsl[2] + hsl[1] - hsl[2] * hsl[1]
        t2 = 2.0 * hsl[2] - t1
        t12 = (t1 - t2) * 6.0
        tR = (hsl[0] + 0.333) % 1.0
        tG = hsl[0]
        tB = (hsl[0] - 0.333 + 1.0) if (hsl[0] < 0.333) else hsl[0] - 0.333
        
        def chTest(t1, t2, t12, tC):
            if 6.0 * tC < 1.0: return t2 + t12 * tC
            elif 2.0 * tC < 1.0: return t1
            elif 3.0 * tC < 2.0: return t2 + t12 * (0.666 - tC)
            else: return t2
          
        return RGB255((chTest(t1, t2, t12, tR), chTest(t1, t2, t12, tG), chTest(t1, t2, t12, tB)))

    def palette(self, size, *points):
        '''
        Creates an indexed color palette by sliding colors between the fixed color points.
        @param size the size of a palette
        @param points the fixed colors (distance, hue, saturation, lightness)
        @return sequence of colors (red, green, blue)
        '''
        palette = []
        if len(points) > 1:
            first = points[0]
            last = points[-1]
            points=[(0,first[1],first[2],first[3])]+list(points)+[(size, last[1], last[2], last[3])]
            def piece(p1, p2):
                d = p2[0]-p1[0]
                return [self.HSLtoRGB((i, j, k)) for i,j,k in zip(np.linspace(p1[1],p2[1],d,endpoint=False),
                                                                  np.linspace(p1[2],p2[2],d,endpoint=False),
                                                                  np.linspace(p1[3],p2[3],d,endpoint=False))]
            for i in range(len(points)-1):
                palette += piece(points[i], points[i+1])
        return np.array(palette)
