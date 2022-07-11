from PIL import ImageGrab


class InstaLocker:
    def __init__(self, agent_num: int):
        """
        The class that will lock agent based on number, and keep track of loading screens
        :param agent_num: The number of the agent, left to right, top to bottom, on the users' agent select screen
        """
        self.agent_num = agent_num

    def run(self) -> bool:
        """
        Run the instalocker program
        :return: Boolean, of whether the program was successfully locked the agent or not
        """
        try:
            self.wait_for_loading_screen()
            self.instalock()

            return True

        except:
            return False

    @staticmethod
    def wait_for_loading_screen():
        while True:
            print("shee")
            img = ImageGrab.grab(bbox=(841, 784, 842, 785))
            img2 = ImageGrab.grab(bbox=(950, 866, 951, 867))

            rgb_pixel_value = img.getpixel((0, 0))
            rgb_pixel_value2 = img2.getpixel((0, 0))

            if rgb_pixel_value == (255, 255, 255) and rgb_pixel_value2 == (234, 238, 178):
                return

    def instalock(self):
        pass
