from ControlPanel import ControlPanel

if __name__ == '__main__':
    CP = ControlPanel()
    # CP.unlocked_agents = DEFAULT_AGENTS
    CP.start()
    CP.stop_instalocker()
    CP.update_settings_file()
