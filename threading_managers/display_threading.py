import cv2
import numpy as np
import os
import Queue
import threading
from copy import deepcopy



class displayFrameThread(threading.Thread):
    def __init__(self, frame, x, y, w, h):
        threading.Thread.__init__(self)
        self._frame = deepcopy(frame)
    def run(self):
        threadLock.acquire()
        self.draw_found_objects()
        self.cv2.imshow('Face Detector', self._frame)
        threadLock.release()

    def display_frame(self):
        cv2.imshow('Face Detector', self._frame)

    def draw_found_objects(self):
        cv2.rectangle(self._frame, (int(x), int(y)),
                             (int(x+w), int(y+w)),
                             (0,255,0), 5)
