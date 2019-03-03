from pystray import *
from PIL import Image
from subprocess import Popen
from tkinter import Tk, filedialog, Message, mainloop
import os
import pyautogui
import time
from pynput.keyboard import Key, Listener, Controller
import pickle
import threading


class ScreenShotter:
    def __init__(self, screenshots_folder=None):
        print("Awwww yeah!")
        # *** Attributes ***
        self.icon_path = "icon.png"
        self.screenshots_folder = screenshots_folder
        self.folder_path = "folder_path.p"

        # *** Setup Menu ***
        self.menu_items = [
            MenuItem("Activate Listener", lambda: self.init_thread(target=self.sc)),
            MenuItem("?", lambda: self.init_thread(target=self.instructions)),
            MenuItem("Select Folder", lambda: self.init_thread(target=self.select_folder)),
            MenuItem("Open Folder", lambda: Popen("explorer %s" % os.path.normpath(self.screenshots_folder))),
            MenuItem("Exit", self.exit),
        ]
        self.menu = Menu(*self.menu_items)

        # *** Get or create screenshot folder path ***
        self.get_folder_path()

        # *** Create System Tray Icon ***
        self.icon = Icon("Test Name", menu=self.menu)
        self.icon.icon = Image.open(self.icon_path)
        self.icon.run()

    def get_folder_path(self, *args):
        try:
            self.screenshots_folder = pickle.load(open(self.folder_path, "rb"))
        except FileNotFoundError:
            pickle.dump(self.select_folder(), open(self.folder_path, "wb"))

    def init_thread(self, target, *args):
        new_thread = threading.Thread(target=target)
        new_thread.start()

    def sc(self, *args):
        def on_press(key):
            print('{0} pressed'.format(key))

            if key == Key.print_screen:
                # Enhanced Screenshot
                screenshot = pyautogui.screenshot()
                sc_time = time.asctime().replace(" ", "").replace(":", "-")
                screenshot.save(os.path.join(self.screenshots_folder, "%s.png" % sc_time))

        def on_release(key):
            print('{0} released'.format(key))

            if key == Key.esc:
                # Stop listener
                return False

        # Collect events until released
        with Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()

    def select_folder(self, *args):
        root = Tk()
        # Hide the auto-generated Tk window immediately.
        root.wm_withdraw()
        self.screenshots_folder = filedialog.askdirectory(initialdir="/", title="Select Screenshots Folder")
        return self.screenshots_folder

    def instructions(self, *args):
        instructions = \
            '''
Click "Activate Listener", then press Print Screen on your keyboard to take and save a screenshot.

Press Esc to deactivate the keyboard listener listener.

Click "Select Folder" to choose where your screenshots are saved.

Click "Open Folder" to go where your screenshots are saved in Explorer.

            '''

        root = Tk()
        root.title("Help")

        m = Message(root, text=instructions)
        m.pack()

        mainloop()

    def exit(self, *args):
        self.icon.stop()
        keyboard = Controller()
        # This terminates the listener and allows the thread to stop. I'll find a better solution later.
        keyboard.release(Key.esc)


app = ScreenShotter()
