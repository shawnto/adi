'''The method by which we identify objects returns large datasets rapidly.
This module is to normalize that input to prevent excessive clicking and
keyboard input. '''
import time

class ClickNormalizer(object):
    def __init__(self, click_difference=1.0):
        self._last_click_time = 0.0
        self._last_click_location = None
        self._click_difference = click_difference

    def validate_click(self):
        click_time = time.time()
        time_dif = click_time - self._last_click_time

        if time_dif >= self._click_difference:
            self._last_click_time = click_time
            return True
        return False
