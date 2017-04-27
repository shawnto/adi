import cv2
import numpy as np
import os
import Queue
import threading
from copy import deepcopy


class displayFrameThread(threading.Thread):
    def __init__(self, frame, x=None, y=None, w=None, h=None, t_lock):
        threading.Thread.__init__(self)
        self._frame = deepcopy(frame)
        self._lock = t_lock
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def run(self):
        self._lock.acquire()
        if all(self._x, self._y):
            self.draw_found_objects()
        self.display_frame()
        self._lock.release()

    def display_frame(self):
        cv2.imshow('ADI', self._frame)

    def draw_found_objects(self):
        cv2.rectangle(self._frame, (int(self._x), int(self._y)),
                             (int(self._x+self._w), int(self._y+self._w)),
                             (0,255,0), 5)
