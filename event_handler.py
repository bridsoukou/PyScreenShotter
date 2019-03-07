from pynput.keyboard import Key, Listener
import pyautogui
import time
import os


class ScreenShotter:
    def __init__(self, screenshots_folder):
        self.screenshots_folder = screenshots_folder

    def on_press(self, key):
        if key == Key.print_screen:
            # Enhanced Screenshot
            screenshot = pyautogui.screenshot()
            sc_time = time.asctime().replace(" ", "").replace(":", "-")
            screenshot.save(os.path.join(self.screenshots_folder, "%s.png" % sc_time))

    def on_release(self, key):
        if key == Key.esc:
            # Stop listener
            return False

    def start_listener(self):
        # Collect events until released
        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()
