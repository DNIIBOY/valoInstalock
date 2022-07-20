import _tkinter

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
        print("Closed instalocker thread...")
    except _tkinter.TclError:  # Fix issue with crash while closing
        print("Instalocker not running, skipping step...")

    print("Updating settings...")
    CP.update_settings_file()

    print("Closing program...")
