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
        self.close_button = None
        self.gun_buttons = []
        self.ability_buttons = []
        self.shield_button = None
        self.toggle_button = None

    def setup(self):
        self.configure(
            bg="#454d59",
            highlightbackground="black"
        )
        self.close_button = Button(self, text="X", fg="red", command=self.toggle_visibility)
        self.close_button.place(relx=0.93, rely=0, relwidth=0.07, relheight=0.1)

        self.setup_guns()
        self.setup_abilities()
        self.shield_button = ShieldButton(self)
        self.shield_button.grid(column=5, row=0, padx=1, pady=1, rowspan=2, sticky="sew")
        self.toggle_button = Button(self, text="Toggle Auto-Buy", font="Rockwell 12", command=lambda: self.toggle_auto_buy())
        self.toggle_button.configure(
            bg=("#79c7c0" if self.parent.settings["auto_buy"] else "#ff4b50"),   # Set button color based on auto_buy setting
        )
        self.toggle_button.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)

    def setup_guns(self) -> None:
        """
        Set up the guns in the buy menu
        """
        for i, gun_name in enumerate(AVAILABLE_GUNS):
            gun_button = GunButton(self, gun_name)

            # Select pistol from settings
            if gun_name == self.parent.settings["shop_settings"]["pistol"]:
                gun_button.configure(bg="#2abd8a")

            gun_button.grid(column=i, row=0, padx=8, pady=60)
            self.gun_buttons.append(gun_button)

    def setup_abilities(self) -> None:
        """
        Set up the abilities in the buy menu
        """
        for i in range(4):
            ability_button = AbilityButton(self, i)
            ability_button.grid(column=i, row=1, padx=1, pady=1)
            self.ability_buttons.append(ability_button)

    def toggle_visibility(self):
        """
        Toggle the visibility of the buy menu
        """
        if self.is_visible:
            self.place_forget()
            self.is_visible = False
        else:
            self.place(relx=0.15, rely=0.2, relwidth=0.7, relheight=0.7)
            self.is_visible = True

    def toggle_auto_buy(self):
        """
        Toggle the auto-buyer on/off
        """
        if self.parent.settings["auto_buy"]:
            self.parent.settings["auto_buy"] = False
            self.toggle_button.configure(bg="#ff4b50")
        else:
            self.parent.settings["auto_buy"] = True
            self.toggle_button.configure(bg="#79c7c0")


class GunButton(Button):
    def __init__(self, parent: BuyMenu, gun_name: str):
        super().__init__(parent)
        self.parent = parent
        self.gun_name = gun_name
        self.configure(
            text=gun_name,
            font="Rockwell 12",
            height=3,
            width=10,
            background="gray",
            foreground="white",
            command=self.select,
        )

    def select(self):
        """
        Select the gun
        """
        self.configure(bg="#2abd8a")

        for gun_button in self.parent.gun_buttons:
            if gun_button is not self:
                gun_button.configure(bg="gray")

        self.parent.parent.settings["shop_settings"]["pistol"] = self.gun_name


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
            width=10,
            background="gray",
            foreground="white",
            command=self.increase_count
        )
        self.bind("<Button-3>", lambda _: self.decrease_count())

    def increase_count(self) -> None:
        if self.count >= 9:
            return
        self.count += 1
        self.configure(text=f"Ability {self.ability_number + 1}: {self.count}")
        self.parent.parent.settings["shop_settings"]["ability_counts"][self.ability_number] = self.count

    def decrease_count(self) -> None:
        if self.count <= 0:
            return
        self.count -= 1
        self.configure(text=f"Ability {self.ability_number + 1}: {self.count}")
        self.parent.parent.settings["shop_settings"]["ability_counts"][self.ability_number] = self.count


class ShieldButton(Button):
    def __init__(self, parent: BuyMenu):
        super().__init__(parent)
        self.parent = parent
        self.is_active = False
        self.configure(
            text="Light Shield",
            font="Rockwell 12",
            height=10,
            width=10,
            foreground="white",
            command=self.toggle
        )
        self.configure(
            bg=("#2abd8a" if self.parent.parent.settings["shop_settings"]["buy_armor"] else "gray"),
        )
        self.bind("<Button-3>", lambda _: self.toggle())

    def toggle(self):
        if self.is_active:
            self.configure(bg="gray")
            self.is_active = False
            self.parent.parent.settings["shop_settings"]["buy_armor"] = False
        else:
            self.configure(bg="#2abd8a")
            self.is_active = True
            self.parent.parent.settings["shop_settings"]["buy_armor"] = True
