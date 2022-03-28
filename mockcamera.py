import numpy as np
from scipy.stats import multivariate_normal
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer


class MockCamera:
    def __init__(self):
        self.properties = {
            'name': 'MockCamera',
            'image_width': 400,
            'image_height': 400,
            'update_time': 200
        }
        self._running = False
        self.imgsize = (self.properties['image_width'], self.properties['image_height'])
        self.img = np.zeros(self.imgsize)

        self.thread = QThread()
        self.worker = FrameWorker(self)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def getImage(self):
        """ Return latest frame. """
        return self.img

        
class FrameWorker(QObject):
    started = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, camera):
        QThread.__init__(self)
        self.timer = QTimer(self)
        self.camera = camera

    def generateFrame(self):
        """ Generate noisy mock camera image with gaussian spot appearing randomly. """
        img = np.zeros(self.camera.imgsize)
        peakmax = 60
        noisemean = 10
        freq = 0.8
        # add a random gaussian peak sometimes
        if np.random.rand() > freq:
            x, y = np.meshgrid(np.linspace(0,self.camera.imgsize[1],self.camera.imgsize[1]), np.linspace(0,self.camera.imgsize[0],self.camera.imgsize[0]))
            pos = np.dstack((x, y))
            xc = (np.random.rand()*2-1)*self.camera.imgsize[0]/2 + self.camera.imgsize[0]/2
            yc = (np.random.rand()*2-1)*self.camera.imgsize[1]/2 + self.camera.imgsize[1]/2
            rv = multivariate_normal([xc, yc], [[50, 0], [0, 50]])
            img = np.random.rand()*peakmax*317*rv.pdf(pos)
            img = img + 0.01*np.random.poisson(img)
        # add Poisson noise
        img = img + np.random.poisson(lam=noisemean, size=self.camera.imgsize)
        self.camera.img = img

    def run(self):
        self.timer.timeout.connect(self.generateFrame)
        self.timer.start(self.camera.properties['update_time'])