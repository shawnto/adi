import cv2
import numpy as np
import pyautogui
import PIL
import sys
import random

class MinionClicker(object):
    def __init__(self, red_minion=True, minion_type='Melee'):
        self._red_minion = red_minion
        self._minion_type = minion_type
        self._random_easing = [pyautogui.easeInQuad, pyautogui.easeOutQuad,
        pyautogui.easeInOutQuad, pyautogui.easeInBounce,
        pyautogui.easeInElastic]
        self._damage_block = False

    def right_click_minion(self, x, y, w, h):
        if not self._damage_block:
            ease = random.choice(self._random_easing)
            x_click = x + (w/2)
            y_click = y + (h/2)
            pyautogui.moveTo(x_click, y_click)
            pyautogui.rightClick()
            return 1
        else:
            print 'CAN\'T ATTACK, TAKING DAMAGE'
            return 0

    def left_click_minion(self, x, y, w, h):
        x_click = x + (w/2)
        y_click = y + (h/2)
        pyautogui.click(x_click, y_click)


    def is_minion(self, found_objs):
        pass

    def draw_rectangle(self, frame, x, y, w, h):
        cv2.rectangle(frame, (int(x), int(y)),
                             (int(x+w), int(y+w)),
                             (0,255,0), 5)

    def check_health(self, frame):
        health_area = frame[ 40: 50,  100: 180]
        return health_area

    def clear_click(self):
        pyautogui.mouseUp(button='right')
