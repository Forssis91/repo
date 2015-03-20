'''
Created on Mar 3, 2015

Author: Esko Nuutila
'''
import sys

from mmb.image_generator_thread import ImageGeneratorThread
from mmb.animation_window import AnimationWindow
from mmb.animation_control_thread import AnimationControlThread

from PyQt4.QtGui import QApplication

def main(args):
    app = QApplication(args) 
    # Window dimension, maximum iteration count, and animation frame rate.
    width = 400
    height = 300
    maxit = 255
    fps = 20
    steps = 100
    
    # Create window.
    animationWindow = AnimationWindow("Mandelbrot animation", width, height)
    # Create animation controller
    animationControl = AnimationControlThread(fps, steps)
    # Animation generator
    imageGenerator = ImageGeneratorThread(width, height, maxit, steps)
    # Bind these together using signals
    imageGenerator.newImage.connect(animationWindow.addFrame)
    animationWindow.setFrameCount.connect(animationControl.setFrameCount)
    animationControl.showFrame.connect(animationWindow.showFrame)
    imageGenerator.finished.connect(animationControl.start)
    #
    animationWindow.show()
    # Calculate fractal image frames.
    imageGenerator.start()
    # When all frames are ready, the animation starts.
    sys.exit(app.exec_())

if __name__ == '__main__':
    #import cProfile
    #cProfile.run('main([])')
    main(sys.argv)