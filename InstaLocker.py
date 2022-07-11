import pyautogui
from PIL import ImageGrab
from time import sleep

from constants import PIXEL_LOCATIONS, RGB_VALUES, CLICK_LOCATIONS


class InstaLocker:
    def __init__(self, agent_num: int):
        """
        The class that will lock agent based on number, and keep track of loading screens
        :param agent_num: The number of the agent, left to right, top to bottom, on the users' agent select screen
        """
        self.agent_num = agent_num

        # Coordinates for agent select
        self.agent_x = 0
        self.agent_y = 0

        self.is_active = False

    def run(self) -> bool:
        """
        Run the instalocker program
        :return: Boolean, of whether the program successfully locked the agent or not
        """
        self.is_active = True

        # Prepare agent select coordinates
        self.calculate_agent_location()

        # Wait for agent select screen
        if not self.wait_for_agent_select():
            # Return false if search was interrupted
            return False

        self.instalock()

        return True

    def calculate_agent_location(self) -> None:
        """
        Calculate the coordinates for agent select
        """
        pass

    def wait_for_agent_select(self) -> bool:
        """
        Wait for the valorant agent select
        :return: Boolean, returns true if agent select is found, returns false if interrupted
        """
        while self.is_active:
            # Get pixel locations from constants file
            box0 = PIXEL_LOCATIONS["select_screen_0"]
            box1 = PIXEL_LOCATIONS["select_screen_1"]

            # Grab two images, to make sure that the user is on the correct screen
            select_screen_0 = ImageGrab.grab(bbox=(box0[0], box0[1], box0[0] + 1, box0[1] + 1))
            select_screen_1 = ImageGrab.grab(bbox=(box1[0], box1[1], box1[0] + 1, box1[1] + 1))

            # Get RGB values of images
            rgb_value_0 = select_screen_0.getpixel((0, 0))
            rgb_value_1 = select_screen_1.getpixel((0, 0))

            # Compare captured RGB values to reference RGB values
            if rgb_value_0 == RGB_VALUES["select_screen_0"] and rgb_value_1 == RGB_VALUES["select_screen_1"]:
                return True
        return False

    def instalock(self) -> None:
        """
        Lock the agent, referencing agent_x and agent_y
        """
        pyautogui.click(self.agent_x, self.agent_y)  # Click selected agent
        pyautogui.click(clicks=1)  # Click again, just to be sure
        sleep(0.02)
        pyautogui.moveTo(CLICK_LOCATIONS["agent_lock_btn"])
        pyautogui.drag(-15, 0, duration=0.02)  # Drag cursor slightly, to fix noreg issue
        pyautogui.click(clicks=2)  # Click twice to guarantee lock
