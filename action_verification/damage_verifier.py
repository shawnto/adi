import cv2
import numpy as np
from copy import deepcopy
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from managers.video_input_managers import FrameProcesser


class DamageVerifier(object):
    def __init__(self):
        self.health_bar_x, self.health_bar_y = 520, 775
        self.health_bar_x_2, self.health_bar_y_2 = 700, 785
        self.frame_process = FrameProcesser([0, 0, 0], [0, 0, 254])


    def taking_damage(self, frame):
        health_bar = deepcopy(frame[self.health_bar_y:self.health_bar_y_2,
                                    self.health_bar_x:self.health_bar_x_2
                                    ])
        check_for_red = self.frame_process.color_filter(health_bar)
        if check_for_red.max() > 250:
            return True
