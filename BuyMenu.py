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
        self.setup_abilities()
        self.place(relx=0.2, rely=0.2, relwidth=0.7, relheight=0.7)
        # self.place_forget()  # Hide the menu by default

    def setup_guns(self) -> None:
        """
        Set up the guns in the buy menu
        """
        for i, gun_name in enumerate(AVAILABLE_GUNS):
            gun_button = GunButton(self, gun_name)

            # Select pistol from settings
            if gun_name == self.parent.settings["shop_settings"]["pistol"]:
                gun_button.configure(bg="black")

            gun_button.grid(column=i, row=0, padx=1, pady=1)
            self.gun_buttons.append(gun_button)

    def setup_abilities(self) -> None:
        """
        Set up the abilities in the buy menu
        """
        for i in range(4):
            ability_button = AbilityButton(self, i)
            ability_button.grid(column=i * 2, row=1, padx=1, pady=1, columnspan=2)
            self.ability_buttons.append(ability_button)


class GunButton(Button):
    def __init__(self, parent: BuyMenu, gun_name: str):
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


class AbilityButton(Button):
    def __init__(self, parent: BuyMenu, ability_number: int):
        super().__init__(parent)

        self.parent = parent
        self.ability_number = ability_number
        self.count = parent.parent.settings["shop_settings"]["ability_counts"][ability_number]

        self.configure(
            text=f"Ability {ability_number + 1}: {self.count}",
            font="Rockwell 12",
            height=3,
            width=16,
            background="white",
            foreground="#ff4b50",
            command=self.increase_count
        )
        self.bind("<Button-3>", self.decrease_count)

    def increase_count(self) -> None:
        if self.count >= 9:
            return
        self.count += 1
        self.configure(text=f"Ability {self.ability_number + 1}: {self.count}")
        self.parent.parent.settings["shop_settings"]["ability_counts"][self.ability_number] = self.count

    def decrease_count(self, action) -> None:
        if self.count <= 0:
            return
        self.count -= 1
        self.configure(text=f"Ability {self.ability_number + 1}: {self.count}")
        self.parent.parent.settings["shop_settings"]["ability_counts"][self.ability_number] = self.count
