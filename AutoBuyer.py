import keyboard
import pyautogui
from time import sleep

from constants import *
from helpers import get_settings


class AutoBuyer:
    def __init__(self, shop_settings: dict):
        self.shop_settings = shop_settings
        self.is_active = False

        self.clicks = {}  # Key is set of coordinates, value is number of clicks

    def run(self):
        self.calculate_clicks()
        self.buy_items()

    def buy_items(self):
        """
        Buy all the items in self.clicks
        """
        keyboard.press_and_release("b")
        sleep(0.1)
        for location, count in self.clicks.items():
            self.buy_item(location, count)
        keyboard.press_and_release("b")

    def calculate_clicks(self) -> None:
        """
        Calculate which buttons to click, and how many times
        """
        if not self.shop_settings["pistol"] == "Classic":
            self.clicks[CLICK_LOCATIONS[self.shop_settings["pistol"].lower()]] = 1  # Buy one pistol

        # Add all the abilities
        for i, count in enumerate(self.shop_settings["ability_counts"]):
            if count > 0:
                self.clicks[CLICK_LOCATIONS[f"ability_{i + 1}"]] = count

        # Buy armor, if selected
        if self.shop_settings["buy_armor"]:
            self.clicks[CLICK_LOCATIONS["light_shield"]] = 1

    @staticmethod
    def buy_item(coords: set, amount: int) -> None:
        """
        Buy the specified number of items at the given coordinates
        :param coords: Set of coordinates to click
        :param amount: Number of times to click
        """
        pyautogui.moveTo(*coords)
        pyautogui.click(clicks=amount, interval=0.1)


if __name__ == '__main__':
    sleep(5)
    AB = AutoBuyer(get_settings(f"{CURRENT_DIR}\\settings.json")["shop_settings"])
    AB.run()
    print(AB.clicks)
