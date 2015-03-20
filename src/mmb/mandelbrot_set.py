'''
Created on Mar 15, 2015

Author: Esko Nuutila
'''
import numpy as np

class MandelbrotSet(object):
    '''
    Mandelbrot sets are the complex numbers c that do not escape
    '''
    def __init__(self, widthInPixels, heightInPixels, maxIterations):
        '''
        Constructor
        '''
        self.widthInPixels = widthInPixels
        self.heightInPixels = heightInPixels
        self.maxIterations = maxIterations
        
        
    def calculate(self, cx, cy, wd):
        n=self.widthInPixels
        m=self.heightInPixels
        d=wd/n
        ymin=cy-d*(m/2)
        ymax=ymin+m*d
        xmin=cx-wd/2
        xmax=xmin+n*d
        return self.mandelbrot(xmin, xmax, n, ymin, ymax, m, self.maxIterations)
        
    
    def mandelbrot(self, xmin, xmax, n, ymin, ymax, m, maxit):
        '''
        Adapted from http://wiki.scipy.org/Tentative_NumPy_Tutorial/Mandelbrot_Set_Example
        '''
        y,x = np.ogrid[ ymin:ymax:m*1j, xmin:xmax:n*1j]
        c = x+y*1j
        z = c.copy()
        divtime = maxit + np.zeros(z.shape, dtype=int)

        for i in range(maxit):
                z  = z**2 + c
                diverge = z*np.conj(z) > 2**2         # who is diverging
                div_now = diverge & (divtime==maxit)  # who is diverging now
                divtime[div_now] = i                  # note when
                z[diverge] = 2                        # avoid diverging too much

        return divtime
