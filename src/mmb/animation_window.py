'''
Created on Mar 14, 2015

Author: Esko Nuutila
'''
from PyQt4.QtGui import QLabel, QImage, QMainWindow, QSizePolicy, QAction, QColor, QPixmap
from PyQt4.QtCore import pyqtSignal, Qt

class AnimationWindow(QMainWindow):
    '''
    A window that shows the animation. It does not control the animation; it just accepts
    new frames to the animation and shows a frame when asked.
    When a new frame is added in emits signal setFrameCount
    '''
    setFrameCount = pyqtSignal(int)

    def __init__(self, title, width, height):
        super(AnimationWindow, self).__init__()
        self.frames = []
        
        self.initUI(title, width, height)
    
    def initUI(self, title, width, height):               
        self.width = width
        self.height = height
        self.label = QLabel(self)
        self.label.setMinimumSize(width, height)
        self.image = QImage(width, height, QImage.Format_RGB32)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed))
        self.setCentralWidget(self.label)

        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle(title)    
        self.show()
        
    def addFrame(self, frame):
        '''
        Adds a new frame to the animation.
        
        frame is a numpy array [M, N, 3], where the pixel values are red, green, blue 0...255
        '''
        #print('Adding frame {} in thread {}'.format(len(self.frames), threading.current_thread()))
        self.statusBar().showMessage('Adding frame {}'.format(len(self.frames)))
        
        height = self.height
        width = self.width
        for y in range(height):
            for x in range(width):
                r,g,b = frame[y,x]
                self.image.setPixel(x, y, QColor(r,g,b).rgb())
        self.frames.append(QPixmap.fromImage(self.image))
        self.showFrame(len(self.frames)-1)
        self.setFrameCount.emit(len(self.frames))
        
    def showFrame(self, index):
        if len(self.frames) > index:
            frame = self.frames[index]
            self.frameIndex = index + 1 if index < len(self.frames) - 1 else 0
            #print('Showing frame {} in {}'.format(index, threading.current_thread()))
            self.label.setPixmap(frame)    
            self.label.update()
    

