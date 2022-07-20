from _tkinter import TclError

from ControlPanel import ControlPanel

if __name__ == '__main__':
    print("Initializing start sequence...")
    CP = ControlPanel()

    print("Starting control panel...")
    CP.start()

    print("Terminating program...")
    print("Closing instalocker thread...")
    try:
        CP.stop_instalocker()
    except TclError:  # Fix issue with crash while closing, due to deleted objects
        print("Closed instalocker thread...")

    print("Updating settings...")
    CP.update_settings_file()

    print("Closing program...")
