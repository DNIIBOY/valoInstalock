from time import time, sleep
from PIL import ImageGrab

from constants import *


class SpikeTimer:
    def __init__(self, img_delay) -> None:
        """
        Class for keeping track of the spike timer and check when to run it
        """
        self.is_active = False  # Whether the class will check for planted spike
        self.img_delay = img_delay  # Delay between spike check images

        self.time = 45.0  # Time until the spike explodes
        self.spike_is_planted = False  # Whether the timer is paused
        self.spike_explosion_time = 0.0  # Epoch time when the spike explodes
        self.had_wrong_frame = True  # Variable to allow for a single frame to read the spike as not planted

    def run(self) -> int:
        """
        Check if the spike is planted and run timer.
        :return: -1 if the spike is not planted, 0 if the spike is planted and not being diffused,
        1 if the spike is planted and being diffused from the beginning, 2 if the spike is planted and being diffused from half.
        """
        if self.check_spike_plant():
            if not self.spike_is_planted:
                self.spike_explosion_time = time() + 45.0
            self.spike_is_planted = True
        else:
            self.spike_is_planted = False
            self.spike_explosion_time = 0.0

        if self.spike_is_planted:
            self.time = self.spike_explosion_time - time()
            self.time = round(self.time, 1)
            return self.check_diffuse()  # Return the diffuse status

        return -1

    def check_spike_plant(self) -> bool:
        """
        Check if the spike is planted
        :return: True if the spike is planted, False otherwise
        """
        if self.is_active:
            # Get pixel locations from constants file
            box0 = PIXEL_LOCATIONS["spike_plant"]

            # Grab two images, to make sure that the user is on the correct screen
            spike_plant = ImageGrab.grab(bbox=(box0[0], box0[1], box0[0] + 1, box0[1] + 1))

            # Get RGB values of images
            rgb_value_0 = spike_plant.getpixel((0, 0))

            # Compare captured RGB values to reference RGB values
            if rgb_value_0 in [RGB_VALUES[f"spike_plant_{i}"] for i in range(4)]:
                self.had_wrong_frame = False
                return True

            elif not self.had_wrong_frame:
                self.had_wrong_frame = True
                return True

            sleep(self.img_delay)

        return False

    def check_diffuse(self) -> int:
        """
        Check if the spike is being diffused
        :return: 0 if the spike is not being diffused, 1 if the spike is being diffused from the beginning,
        2 if the spike is being diffused from half.
        """
        if self.is_active:
            # Get pixel locations from constants file
            box0 = PIXEL_LOCATIONS["spike_diffuse_half"]
            box1 = PIXEL_LOCATIONS["spike_diffuse_full"]

            # Grab two images, to make sure that the user is on the correct screen
            half_diffuse = ImageGrab.grab(bbox=(box0[0], box0[1], box0[0] + 1, box0[1] + 1))
            full_diffuse = ImageGrab.grab(bbox=(box1[0], box1[1], box1[0] + 1, box1[1] + 1))

            # Get RGB values of images
            rgb_value_0 = half_diffuse.getpixel((0, 0))
            rgb_value_1 = full_diffuse.getpixel((0, 0))

            # Compare captured RGB values to reference RGB values
            if rgb_value_0 == RGB_VALUES["spike_diffuse"]:
                return 2

            if rgb_value_1 == RGB_VALUES["spike_diffuse"]:
                return 1

            return 0
        return 0
