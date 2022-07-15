import os
import json
from constants import *


def get_settings(path: str):
    """
    Get the settings from the settings file, or create a new settings file if it doesn't exist.
    :param path: Path to the settings file
    :return: Dictionary containing the settings
    """
    if not os.path.exists(path):
        with open(path, "w") as settings_file:
            settings_file.write(json.dumps(DEFAULT_SETTINGS, indent=4))
    with open(path, "r") as settings_file:
        settings = json.load(settings_file)

    new_settings = {}
    # Remove unused settings
    for setting in settings.keys():
        if setting in DEFAULT_SETTINGS.keys():
            new_settings[setting] = settings[setting]

    # Add missing settings
    for setting in DEFAULT_SETTINGS.keys():
        if setting not in settings:
            new_settings[setting] = DEFAULT_SETTINGS[setting]

    return new_settings


def get_locked_agents(unlocked_agents: list) -> list[str]:
    """
    Get a list of all locked agents based on the unlocked_agents list and the global AGENT_LIST
    :param unlocked_agents: List of unlocked agents
    """
    locked_agents = []
    for agent in AGENT_LIST:
        if agent not in unlocked_agents:
            locked_agents.append(agent)
    return locked_agents


def get_button_texts(button_list: list) -> list[str]:
    """
    Get the text of all buttons from a list of buttons
    :param button_list: List of buttons with text
    """
    texts = []
    for but in button_list:
        texts.append(but.cget("text"))
    return texts


def float_validation(text: str) -> bool:
    """
    Validate that a char is a valid float character
    :param text: String to validate
    :return: True if the string is a valid float, False otherwise
    """
    if text == ".":
        return True
    try:
        float(text)
        return True
    except ValueError:
        return False
