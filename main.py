import _tkinter

from ControlPanel import ControlPanel

if __name__ == '__main__':
    CP = ControlPanel()
    # CP.unlocked_agents = DEFAULT_AGENTS
    CP.start()
    try:
        CP.stop_instalocker()
    except _tkinter.TclError:  # Fix issue with crash while closing
        pass
    CP.update_settings_file()
