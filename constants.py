from os.path import dirname, realpath
import sys

VERSION_NUMBER = "v1.3.2"

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

# The default settings for the auto-buyer
DEFAULT_BUY = {
    "pistol": "Ghost",
    "ability_counts": [0, 0, 0, 0],
    "buy_armor": False
}

# Default settings file contents
DEFAULT_SETTINGS = {
    "unlocked_agents": DEFAULT_AGENTS,
    "selected_agent": "Brimstone",
    "img_delay": 0.5,
    "play_screen_delay_time": 3.0,
    "auto_restart": False,
    "show_spike_timer": False,
    "auto_buy": False,
    "shop_settings": DEFAULT_BUY,
}

# Pixel locations for detection pictures
PIXEL_LOCATIONS = {
    "select_screen_0": (841, 784),  # Top left corner of "lock in" button
    "select_screen_1": (950, 866),  # Yellow arrow above agents
    "play_screen_0": (758, 0),  # White line left of play button
    "play_screen_1": (16, 10),  # Top left corner Valorant logo
    "in_game_0": (643, 1027),  # 0 in the 100 hp indicator
    "in_game_1": (1115, 279),  # Bottom right corner of buy phase indicator
    "spike_plant": (957, 25),  # Spike plant indicator on top of screen
    "spike_diffuse_full": (833, 183),  # Left side of diffuse indicator
    "spike_diffuse_half": (961, 183),  # Center of diffuse indicator
}

# RGB values for detection pictures
RGB_VALUES = {
    "select_screen_0": (255, 255, 255),
    "select_screen_1": (234, 238, 178),
    "play_screen_0": (255, 255, 255),
    "play_screen_1": (254, 254, 254),
    "in_game_0": (255, 255, 255),
    "in_game_1": (246, 246, 246),
    "spike_plant_0": (230, 0, 0),
    "spike_plant_1": (170, 0, 0),
    "spike_plant_2": (169, 0, 0),
    "spike_plant_3": (124, 0, 0),
    "spike_diffuse": (235, 238, 178)
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

# Available guns in the shop
AVAILABLE_GUNS = [
    "Classic",
    "Shorty",
    "Frenzy",
    "Ghost",
    "Sheriff"
]
