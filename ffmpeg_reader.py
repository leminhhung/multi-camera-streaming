import subprocess as sp
import numpy as np

class ffmpegVideoOnvif:

    def __init__(self, url='rtsp://192.168.100.2:554/onvif1', w=460, h=320, depth=3, pix_format='rgb24', bufsize=5,
                 frame_per_second='8'):
        self.frame_size = str(w) + 'x' + str(h)
        self.nbytes = w * h * depth
        self.pipe = None
        self.w = w
        self.h = h
        self.depth = depth
        self.pix_format = pix_format
        self.bufsize = bufsize
        self.frame_per_second = frame_per_second
        self.url = url
        self.lastFrame = None
        self.getFrame()
        self.openConnectOnvif()
        self.flg_run = True

    def openConnectOnvif(self):
        self.command = ['ffmpeg',
                        '-i', self.url,
                        '-f', 'image2pipe',
                        '-s', self.frame_size,  # size of one frame
                        '-pix_fmt', self.pix_format,
                        '-r', self.frame_per_second,  # frames per second
                        '-vcodec', 'rawvideo', '-']
        self.pipe = sp.Popen(self.command, bufsize=self.bufsize, stdout=sp.PIPE)

    def close_pipe(self):
        if self.pipe:
            self.pipe.stdout.flush()
            self.pipe.terminate()
            self.pipe.stdout.close()
            # self.pipe.stderr.close()
            self.pipe.wait()
            self.pipe = None

    def getFrame(self):
        try:
            if self.pipe:
                self.raw_image = self.pipe.stdout.read(self.nbytes)
                self.lastFrame = np.frombuffer(self.raw_image, dtype='uint8')
                if len(self.lastFrame) == self.nbytes:
                    self.lastFrame = self.lastFrame.reshape((self.h, self.w, self.depth))[:, :, ::-1]
                    self.pipe.stdout.flush()
                else:
                    self.close_pipe()
                    self.openConnectOnvif()
            else:
                self.close_pipe()
                self.openConnectOnvif()
        except:
            raise IOError('Disconnect ......')

    def runGetStream(self):
        try:
            while self.flg_run == True:
                self.getFrame()
            self.close_pipe()
        except:
            raise IOError('Disconnect ......')
