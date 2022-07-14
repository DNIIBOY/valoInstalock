from os.path import dirname, realpath
import sys

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    CURRENT_DIR = dirname(sys.executable)
elif __file__:
    CURRENT_DIR = dirname(realpath(__file__))


# All valorant agents
AGENT_LIST = [
    "Astra",
    "Breach",
    "Brimstone",
    "Chamber",
    "Cypher",
    "Fade",
    "Jett",
    "KAY/O",
    "Killjoy",
    "Neon",
    "Omen",
    "Phoenix",
    "Raze",
    "Reyna",
    "Sage",
    "Skye",
    "Sova",
    "Viper",
    "Yoru"
]
# The valorant agents, that are always unlocked
DEFAULT_AGENTS = ["Brimstone", "Jett", "Phoenix", "Sage", "Sova"]

# Default settings file contents
DEFAULT_SETTINGS = {
    "unlocked_agents": DEFAULT_AGENTS,
    "selected_agent": "Brimstone",
    "img_delay_time": 1.0,
    "play_screen_delay_time": 3.0
}

# Pixel locations for detection pictures
PIXEL_LOCATIONS = {
    "select_screen_0": (841, 784),  # Top left corner of "lock in" button
    "select_screen_1": (950, 866),  # Yellow arrow above agents
    "play_screen_0": (969, 25),  # Gray background on play button
    "play_screen_1": (16, 10)  # Top left corner Valorant logo
}

# RGB values for detection pictures
RGB_VALUES = {
    "select_screen_0": (255, 255, 255),
    "select_screen_1": (234, 238, 178),
    "play_screen_0": (194, 196, 201),
    "play_screen_1": (254, 254, 254)
}

# Pixel locations of buttons to click
CLICK_LOCATIONS = {
    "agent_lock_btn": (1000, 820),
    "ability_1": (665, 885),
    "ability_2": (888, 885),
    "ability_3": (1170, 885),
    "ability_4": (1300, 885),
    "light_shield": (1440, 285),
    "heavy_shield": (1440, 585),
    "classic": (475, 200),
    "shorty": (475, 325),
    "frenzy": (475, 450),
    "ghost": (475, 575),
    "sheriff": (475, 700),
}
