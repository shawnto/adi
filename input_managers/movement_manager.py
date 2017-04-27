import sys
import os
import pyautogui
import random

class GeneralMovement(object):
    def __init__(self):
        self._home_base_x = 1090
        self._home_base_y = 810
        self._random_easing = [pyautogui.easeInQuad, pyautogui.easeOutQuad,
        pyautogui.easeInOutQuad, pyautogui.easeInBounce,
        pyautogui.easeInElastic]

    def go_home(self):
        ease = random.choice(self._random_easing)
        x_click = self._home_base_x
        y_click = self._home_base_y
        pyautogui.moveTo(x_click, y_click)
        pyautogui.rightClick()
