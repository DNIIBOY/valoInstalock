from tkinter import *
from constants import *
from helpers import float_validation


class SettingsPanel(Canvas):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.show_settings = False
        self.buttons = {}  # Contains the settings buttons

        self.settings_cog = Button(self.parent)

    def setup(self) -> None:
        self.configure(
            height=49,
            width=575,
            bg="black"
        )
        self.pack()

        img = PhotoImage(file=f"{CURRENT_DIR}\\img\\redcog.png")
        cog_img = img.subsample(3, 3)  # Make the image small enough to fit
        self.settings_cog.configure(
            image=cog_img,
            command=lambda: self.toggle_settings(),
        )
        self.settings_cog.image = cog_img
        self.settings_cog.pack(pady=10)

        selected_agents_button = Button(self, text="Default Agents", command=lambda: self.parent.set_agent_list(0))
        all_agents_button = Button(self, text="All Agents", command=lambda: self.parent.set_agent_list(1))

        auto_restart_toggle = Button(self, text="Auto Restart", command=lambda: self.toggle_auto_restart())
        auto_restart_toggle.configure(bg=("#79c7c0" if self.parent.settings["auto_restart"] else "#ff4b50"))

        buy_menu_toggle = Button(self, text="Buy Menu", command=lambda: self.parent.buy_menu.toggle_visibility())

        delay_entry_label = Label(self, text="Check Delay [s]:", bg="black", fg="white")

        validation = self.register(float_validation)  # Only allow float characters
        img_delay_entry = Entry(
            self,
            validate="key",
            validatecommand=(validation, "%P"),
            width=5,
        )
        img_delay_entry.insert(0, str(self.parent.settings["img_delay"]))
        img_delay_entry.bind("<KeyRelease>", lambda _: self.parent.update_img_delay(img_delay_entry.get()))

        self.buttons = {
            "selected_agents_button": selected_agents_button,
            "all_agents_button": all_agents_button,
            "auto_restart_toggle": auto_restart_toggle,
            "buy_menu_toggle": buy_menu_toggle,
            "delay_entry_label": delay_entry_label,
            "img_delay_entry": img_delay_entry,
        }

        # Grid the buttons
        for i, button in enumerate(self.buttons.values()):
            button.grid(column=i, row=1, padx=10, pady=10)

        for key in self.buttons:
            self.buttons[key].configure(font="Rockwell 12")
            self.buttons[key].grid_remove()  # Hide all buttons by default

    def toggle_settings(self) -> None:
        """
        Toggle settings panel on/off
        """
        if self.show_settings:
            self.show_settings = False
            self.settings_cog.configure(bg="white")
            for key in self.buttons:
                self.buttons[key].grid_remove()
        else:
            self.show_settings = True
            self.settings_cog.configure(bg="black")
            for key in self.buttons:
                self.buttons[key].grid()
        self.parent.change_agents(self.show_settings)

    def toggle_auto_restart(self) -> None:
        """
        Toggle whether the program auto restarts for the next game
        """
        if self.parent.settings["auto_restart"]:
            self.parent.settings["auto_restart"] = False
            self.buttons["auto_restart_toggle"].configure(
                bg="#ff4b50",
            )
        else:
            self.parent.settings["auto_restart"] = True
            self.buttons["auto_restart_toggle"].configure(
                bg="#79c7c0",
            )
