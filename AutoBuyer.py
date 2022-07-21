import keyboard
import pyautogui
from time import sleep
from PIL import ImageGrab

from constants import *
from helpers import get_settings


class AutoBuyer:
    def __init__(self, img_delay: float, shop_settings: dict):
        self.img_delay = img_delay
        self.shop_settings = shop_settings
        self.is_active = False

        self.clicks = {}  # Key is set of coordinates, value is number of clicks

    def run(self) -> bool:
        self.is_active = True
        if not self.wait_for_game():
            return False
        self.calculate_clicks()
        self.buy_items()
        return True

    def wait_for_game(self) -> bool:
        """
        Wait for the player to spawn in to the game
        :return: Boolean, returns true if the player spawns, false if interrupted
        """
        while self.is_active:
            # Get pixel locations from constants file
            box0 = PIXEL_LOCATIONS["in_game_0"]
            box1 = PIXEL_LOCATIONS["in_game_1"]

            # Grab two images, to make sure that the user is on the correct screen
            in_game_0 = ImageGrab.grab(bbox=(box0[0], box0[1], box0[0] + 1, box0[1] + 1))
            in_game_1 = ImageGrab.grab(bbox=(box1[0], box1[1], box1[0] + 1, box1[1] + 1))

            # Get RGB values of images
            rgb_value_0 = in_game_0.getpixel((0, 0))
            rgb_value_1 = in_game_1.getpixel((0, 0))

            # Compare captured RGB values to reference RGB values
            if rgb_value_0 == RGB_VALUES["in_game_0"] and rgb_value_1 == RGB_VALUES["in_game_1"]:
                return True

            # Grab images to check for main menu, in case of match cancel
            box0 = PIXEL_LOCATIONS["play_screen_0"]
            box1 = PIXEL_LOCATIONS["play_screen_1"]

            # Grab two images, to make sure that the user is on the correct screen
            play_screen_0 = ImageGrab.grab(bbox=(box0[0], box0[1], box0[0] + 1, box0[1] + 1))
            play_screen_1 = ImageGrab.grab(bbox=(box1[0], box1[1], box1[0] + 1, box1[1] + 1))

            # Get RGB values of images
            rgb_value_0 = play_screen_0.getpixel((0, 0))
            rgb_value_1 = play_screen_1.getpixel((0, 0))

            # Compare captured RGB values to reference RGB values
            if rgb_value_0 == RGB_VALUES["play_screen_0"] and rgb_value_1 == RGB_VALUES["play_screen_1"]:
                return False

            sleep(self.img_delay)

        return False

    def buy_items(self):
        """
        Buy all the items in self.clicks
        """
        keyboard.press_and_release("b")
        sleep(0.1)
        for location, count in self.clicks.items():
            self.buy_item(location, count)
            sleep(0.2)
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
    AB = AutoBuyer(0.2, get_settings(f"{CURRENT_DIR}\\settings.json")["shop_settings"])
    AB.is_active = True
    AB.wait_for_game()
    # AB.run()
    print(AB.clicks)
