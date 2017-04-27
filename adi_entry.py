from managers.video_input_managers import VideoIn, ObjectFinder, FrameProcesser
from minion_clicker import MinionClicker
from action_verification.damage_verifier import DamageVerifier
from managers.gui_input_manager import ClickNormalizer
from input_managers.movement_manager import GeneralMovement
#from threading_managers.display_threading import displayFrameThread
import cv2
import os
import random
import time
import numpy as np
import threading
from copy import deepcopy

class displayFrameThread(threading.Thread):
    def __init__(self, frame, t_lock, x=None, y=None, w=None, h=None):
        threading.Thread.__init__(self)
        self._frame = frame
        self._lock = t_lock
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def run(self):
        self._lock.acquire()
        if self._x is not None and self._y is not None:
            self.draw_found_objects()
        self.display_frame()
        self._lock.release()

    def display_frame(self):
        cv2.imshow('ADI', self._frame)

    def draw_found_objects(self):
        cv2.rectangle(self._frame, (int(self._x), int(self._y)),
                             (int(self._x+self._w), int(self._y+self._w)),
                             (0,255,0), 5)

class minionClickingThread(threading.Thread):
    def __init__(self, min_click, t_lock, x, y, w, h):
        threading.Thread.__init__(self)
        self._min_click = min_click
        self._lock = t_lock
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def run(self):
        self._lock.acquire()
        self._min_click.right_click_minion(self._x, self._y, self._w, self._h)
        self._lock.release()


if __name__ == '__main__':
    cas_path = 'C:\Users\Shawn\Documents\\redMinionTraining\melee_minion_cas\cascade.xml'
    vid_in = VideoIn(cas_path, cap_slot=1)
    obj_find = ObjectFinder(cas_path, k_val=1.25, nearest_neighbor=20)
    min_click = MinionClicker()
    click_man = ClickNormalizer(click_difference=0.5)
    dam_ver = DamageVerifier()
    move_man = GeneralMovement()
    display_thread_lock = threading.Lock()
    minion_click_thread_lock = threading.Lock()
    red_lower_bound, red_upper_bound = [10, 10, 80], [60, 60, 254]#[0, 0, 150], [85, 73, 255]
    frame_proc_red = FrameProcesser(red_lower_bound, red_upper_bound)
    still_index = 0
    cv2.namedWindow('ADI', cv2.WINDOW_NORMAL)
    while True:
        ret, frame = vid_in.get_frame()
        red_processed_full = frame_proc_red.color_filter(frame)

        found_objs = obj_find(frame)
        valid_finds = list()
        if dam_ver.taking_damage(frame):
            min_click._damage_block = True
            move_man.go_home()
            print 'TAKING DAMAGE'

        else:
            min_click._damage_block = False
        for (x, y, w, h) in found_objs:
            if red_processed_full[y:y+h, x:x+w].max() > 200:
                valid_finds.append(list([x, y, w, h]))

        if len(valid_finds) > 0 and click_man.validate_click():
            x, y, w, h = [x for x in random.choice(valid_finds)]
            display_thread = displayFrameThread(frame, display_thread_lock,
                                                x=x, y=y, w=w, h=h)
            display_thread.start()
            click_thread = minionClickingThread(min_click, minion_click_thread_lock,
                                                x, y, w, h)
            click_thread.start()

        else:
            display_thread = displayFrameThread(frame, display_thread_lock)
            display_thread.start()

        k = cv2.waitKey(1)
        if k == 27:
            break
        elif k in [ord('r'), ord('g'), ord('b'), ord('h'), ord('t'), ord('n')]:
            frame_proc_red.change_current_bound(k)
        elif k == 2490368 or k == 2621440:
            frame_proc_red.tune_color_bounds(k)
        min_click.clear_click()

    print 'RAN'
    vid_in.release_capture()
    cv2.destroyAllWindows()
