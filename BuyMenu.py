from tkinter import *
from constants import *


class BuyMenu(Canvas):
    """
    A menu for the user to select which weapons will be bought by the auto-buyer
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.is_visible = False
        self.gun_buttons = []
        self.ability_buttons = []
        self.shield_button = None

        self.configure(
            width=600,
            height=700,
            bg="#ccc783"
        )

    def setup(self):
        self.setup_guns()
        self.place(relx=0.2, rely=0.2, relwidth=0.7, relheight=0.7)
        # self.place_forget()  # Hide the menu by default

    def setup_guns(self) -> None:
        """
        Set up the guns in the buy menu
        """
        for i, gun_name in enumerate(AVAILABLE_GUNS):
            gun_button = GunButton(self, gun_name)
            gun_button.grid(column=i, row=0, padx=1, pady=1)
            self.gun_buttons.append(gun_button)


class GunButton(Button):
    def __init__(self, parent, gun_name):
        super().__init__(parent)
        self.parent = parent
        self.configure(
            text=gun_name,
            font="Rockwell 12",
            height=3,
            width=8,
            background="white",
            foreground="#ff4b50",
        )
