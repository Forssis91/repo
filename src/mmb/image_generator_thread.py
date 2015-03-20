'''
Created on Mar 15, 2015

Author: Esko Nuutila based on a Scala program by Teemu Lehtinen
'''

from mmb.mandelbrot_set import MandelbrotSet
from mmb.colorizer import Colorizer
from PyQt4.QtCore import pyqtSignal,QThread
import numpy as np

class ImageGeneratorThread(QThread):
    '''
    Generates a sequence of mandelbrot images
    
    step: number of images to generate
    width, height: the dimensions of the images
    maxit: maximum amount of iterations
    '''
    newImage = pyqtSignal(object)

    def __init__(self, width, height, maxit, steps):
        super(ImageGeneratorThread, self).__init__()
        self.width = width
        self.height = height
        self.maxit = maxit
        self.steps = steps
        
    def run(self):
            # Some interesting targets.
        # Animation parameters.
        steps = self.steps
        
        def easing(begin, end, steps):
            return np.fromfunction(lambda step: begin-((step/(steps-1)-1.0)**4-1.0)*(end - begin), (steps,), dtype=float)
        
        x = easing(-0.5, -0.1638, steps)
        y = easing(0.0, 1.0353, steps)
        w = easing(3, 0.0005, steps)
        mandelbrot = MandelbrotSet(self.width, self.height, self.maxit)
        colorizer = Colorizer(self.maxit)
        for i in range(steps):
            frame = mandelbrot.calculate(x[i], y[i], w[i])
            frame = colorizer.colorize(frame)
            self.newImage.emit(frame)

    
