import cv2
import numpy as np



class VideoIn(object):
    def __init__(self, cap_source, cap_slot=0, scale_factor=1.0):
        self._cap_source = cv2.VideoCapture(cap_slot)
        self._cap_source.set(3, 1280)
        self._cap_source.set(4, 800)
        self._scale_factor = scale_factor

    def get_frame(self):
        '''Should be run in a loop to get video data.'''
        ret, frame = self._cap_source.read()



        if self._scale_factor != 1.0:
            frame = cv2.resize(frame, None, fx=self._scale_factor,
                               fy=self._scale_factor,
                               interpolation=cv2.INTER_AREA)

        return ret, frame

    def release_capture(self):
        self._cap_source.release()


class ObjectFinder(object):

    def __init__(self, cascade_path, nearest_neighbor=1, k_val=1):
        self._cascade = cv2.CascadeClassifier(cascade_path)
        self._nearest_neighbor = nearest_neighbor
        self._k_val = int(k_val)
        self._found_objects = None

    def __call__(self, grayed_frame):
        found_objects = self._cascade.detectMultiScale(grayed_frame,
                                                       self._nearest_neighbor,
                                                       self._k_val)
        return found_objects


class FrameProcesser(object):
    def __init__(self, lower, upper):
        self._lower = list(lower)
        self._upper =  list(upper)
        self._bound_key = {'r': ('Upper', 2),
                           'g': ('Upper', 1),
                           'b': ('Upper', 0),
                           't': ('Lower', 2),
                           'h': ('Lower', 1),
                           'n': ('Lower', 0)}
        self._current_bound = 'r'

    def color_filter(self, frame):
        lower = np.array(self._lower, dtype = "uint8")
        upper = np.array(self._upper, dtype = "uint8")

        mask = cv2.inRange(frame, lower, upper)
        output = cv2.bitwise_and(frame, frame, mask=mask)
        return output

    def tune_color_bounds(self, key):
        boundary, index = self._bound_key.get(self._current_bound)
        if boundary is 'Upper':
            if key == 2490368:
                self._upper[index] += 1
            else:
                self._upper[index] -= 1
            print self._upper
        else:
            if key == 2490368:
                self._lower[index] += 1
            else:
                self._lower[index] -= 1
            print self._lower

    def change_current_bound(self, key):
        self._current_bound = str(unichr(key))
        print self._bound_key.get(self._current_bound)


def get_gray_frame(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
