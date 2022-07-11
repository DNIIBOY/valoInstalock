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
    "default_agent": "Brimstone"
}

# Pixel locations for detection pictures
PIXEL_LOCATIONS = {
    "select_screen_0": (841, 784),  # Top left corner of "lock in" button
    "select_screen_1": (950, 866),  # Yellow arrow above agents
}

# RGB values for detection pictures
RGB_VALUES = {
    "select_screen_0": (255, 255, 255),
    "select_screen_1": (234, 238, 178),
}

# Pixel locations of buttons to click
CLICK_LOCATIONS = {
    "agent_lock_btn": (1000, 820),
}
