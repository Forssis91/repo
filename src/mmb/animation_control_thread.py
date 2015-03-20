'''
Created on Mar 15, 2015

@author: Esko Nuutila
'''

from PyQt4.QtCore import QThread,pyqtSignal
import time

class AnimationControlThread(QThread):
    '''
    A thread that controls the animation. It does not know anything about the actual images
    in the animation, just the number of frames and the expected frame rate of the animation.
    It is prepared for the change of the number of frames.
    
    Whenever it is time to show the next frame it emits he signal showFrame.
    Connect this to a slot that does the actual showing of the animation.
    '''

    showFrame = pyqtSignal(int)
        
    def __init__(self, frameRate, maxFrameCount):
        super(AnimationControlThread, self).__init__()
        self.frameRate = frameRate
        self.maxFrameCount = maxFrameCount
        self.running = False
        
    def setFrameCount(self, newFrameCount):
        self.maxFrameCount = newFrameCount
        
    def run(self):
        currentFrame = 0
        self.running = True
        while self.running:
            time.sleep(1/self.frameRate)
            if self.maxFrameCount > currentFrame:
                self.showFrame.emit(currentFrame)
                currentFrame = (currentFrame+1) % self.maxFrameCount
                