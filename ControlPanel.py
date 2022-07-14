import json
import threading
import os

from tkinter import *
from constants import *
from InstaLocker import InstaLocker


class ControlPanel:
    def __init__(self):
        self.main_window = Tk()  # Root window

        # Setup label for background image
        background_label = Label(self.main_window)

        self.agent_canvas = Canvas(self.main_window, height=200, width=600)  # Grid of agents
        self.settings_canvas = Canvas(self.main_window, height=100, width=600)  # Canvas for settings and settings button
        self.internal_settings_canvas = Canvas(self.settings_canvas)  # Canvas that toggles with settings

        self.settings = get_settings(f"{CURRENT_DIR}\\settings.json")
        self.show_settings = False  # Whether the settings panel is shown

        self.IL = None  # Object of instalocker class, for instalocking
        self.IL_thread = None  # Thread for running actual instalocker

        self.agent_button_list = []  # Contains button objects for all agents

        # All miscellaneous buttons and labels
        self.UI_elements = {
            "background_label": background_label,
        }

        # All buttons in the settings panel
        self.settings_buttons = {}

    def start(self):
        """
        Start the program
        """
        self.setup_main_window()
        self.setup_agent_grid()

        self.setup_settings_panel()

        self.main_window.mainloop()

    def setup_main_window(self) -> None:
        """
        Set up the main window, including title and size
        """
        self.main_window.title("Valorant Instalocker")
        self.main_window.minsize(850, 500)
        self.main_window.maxsize(960, 540)
        self.main_window.geometry("960x540")  # Default size
        self.main_window.iconbitmap(f"{CURRENT_DIR}\\img\\logo.ico")

        # Setup background image
        background_image = PhotoImage(file=f"{CURRENT_DIR}\\img\\iceboxBackground.png")
        background_label = self.UI_elements["background_label"]
        background_label.configure(
            image=background_image
        )
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image  # Fixes issue with lost reference for image

        title = Label(self.main_window, text="Valorant Instalocker", fg="#ff4b50", font="Rockwell 30", bg="#000000")
        title.pack(pady=10)

    def setup_agent_grid(self) -> None:
        """
        Set up the agent grid
        """
        self.agent_canvas.configure(
            bg="white"
        )

        locked_agents = get_locked_agents(self.settings["unlocked_agents"])

        i = 0
        for y in range(2):
            # Account for extra agent on top row, when there is and odd agent count
            odd_offset = int(len(AGENT_LIST) % 2 == 1 and y == 0)
            for x in range((len(AGENT_LIST) // 2) + odd_offset):
                if i < len(self.settings["unlocked_agents"]):  # All unlocked agents first
                    self.agent_button_list.append(
                        Button(
                            self.agent_canvas,
                            text=self.settings["unlocked_agents"][i],
                            height=3,
                            width=8,
                            background="white",
                            foreground="#ff4b50",
                            font="Rockwell 12",
                            command=lambda num=i: self.select_agent(num),
                        )
                    )
                else:  # Locked agents last
                    self.agent_button_list.append(
                        Button(
                            self.agent_canvas,
                            text=locked_agents[i - len(self.settings["unlocked_agents"])],
                            height=3,
                            width=8,
                            background="white",
                            foreground="#ff4b50",
                            font="Rockwell 12",
                            command=lambda num=i: self.unlock_agent(num),
                        )
                    )
                    self.agent_button_list[i]["state"] = "disabled"

                self.agent_button_list[i].grid(column=x, row=y, padx=1, pady=1)
                i += 1

        self.agent_canvas.pack(pady=25)

        # Select default agent
        try:
            self.agent_button_list[self.settings["unlocked_agents"].index(self.settings["selected_agent"])].configure(bg="black")
        except ValueError:
            self.agent_button_list[0].configure(bg="black")

    def setup_settings_panel(self) -> None:
        """
        Set up the settings panel
        """
        self.settings_canvas.pack()

        self.internal_settings_canvas.configure(
            height=49,
            width=575,
            bg="black"
        )
        self.internal_settings_canvas.pack()

        img = PhotoImage(file=f"{CURRENT_DIR}\\img\\redcog.png")
        cog_img = img.subsample(3, 3)  # Make the image small enough to fit

        settings_cog = Button(self.main_window, image=cog_img, command=lambda: self.toggle_settings())
        settings_cog.image = cog_img
        settings_cog.pack(pady=10)
        self.UI_elements["settings_cog"] = settings_cog

        selected_agents_button = Button(self.internal_settings_canvas, text="Default Agents", command=lambda: self.set_agent_list(0))
        all_agents_button = Button(self.internal_settings_canvas, text="All Agents", command=lambda: self.set_agent_list(1))

        auto_restart_toggle = Button(self.internal_settings_canvas, text="Auto Restart", command=lambda: self.toggle_auto_restart())
        auto_restart_toggle.configure(bg=("#79c7c0" if self.settings["auto_restart"] else "#ff4b50"))

        delay_entry_label = Label(self.internal_settings_canvas, text="Check Delay [s]:", bg="black", fg="white")
        validation = self.main_window.register(float_validation)  # Only allow float characters

        img_delay_entry = Entry(
            self.internal_settings_canvas,
            validate="key",
            validatecommand=(validation, "%S"),
            width=5,
        )
        img_delay_entry.insert(0, str(self.settings["img_delay_time"]))

        selected_agents_button.grid(column=0, row=0, padx=10, pady=10)
        all_agents_button.grid(column=1, row=0, padx=10, pady=10)
        auto_restart_toggle.grid(column=2, row=0, padx=10, pady=10)
        delay_entry_label.grid(column=3, row=0, padx=2, pady=10)
        img_delay_entry.grid(column=4, row=0, padx=10, pady=10)

        self.settings_buttons = {
            "selected_agents_button": selected_agents_button,
            "all_agents_button": all_agents_button,
            "auto_restart_toggle": auto_restart_toggle,
            "delay_entry_label": delay_entry_label,
            "img_delay_entry": img_delay_entry,
        }

        for key in self.settings_buttons:
            self.settings_buttons[key].configure(font="Rockwell 12")
            self.settings_buttons[key].grid_remove()  # Hide all buttons by default

        status_label = Label(self.main_window,
                             text="Waiting for start",
                             fg="lightgreen",
                             bg="black",
                             font="Rockwell 20")
        status_label.pack()

        run_button = Button(
            self.main_window,
            text="Run",
            font="Rockwell 15",
            command=lambda: self.start_instalocker(),
            height=2,
            width=12,
            bg="#79c7c0",
            fg="#000000",
        )
        run_button.pack(side=BOTTOM, pady=25)
        self.UI_elements["run_button"] = run_button
        self.UI_elements["status_label"] = status_label

    def update_settings_file(self) -> None:
        """
        Update settings file with current settings
        """
        self.settings["unlocked_agents"] = sorted(self.settings["unlocked_agents"])

        json_object = json.dumps(self.settings, indent=4)
        with open(f"{CURRENT_DIR}\\settings.json", "w") as settings_file:
            settings_file.write(json_object)

    def select_agent(self, agent_num: int) -> None:
        """
        Selects which agent should be instalocked by the program
        :param agent_num: Integer representing the index of the agent in the unlocked_agents list
        """
        self.settings["selected_agent"] = self.settings["unlocked_agents"][agent_num]

        # Set agent num for currently running instalocker, if there is one
        try:
            self.IL.agent_num = agent_num
        except AttributeError:
            pass

        for but in self.agent_button_list[:len(self.settings["unlocked_agents"])]:
            but.configure(
                bg="white"
            )
        self.agent_button_list[agent_num].configure(
            bg="black"
        )

    def unlock_agent(self, agent_num: int):
        """
        Unlocks an agent to be selected by the user.
        :param agent_num: Integer representing the index of the agent in the agent_buttons list
        """
        button_texts = get_button_texts(self.agent_button_list)

        self.settings["unlocked_agents"].append(button_texts[agent_num])
        self.settings["unlocked_agents"] = sorted(self.settings["unlocked_agents"])
        self.agent_button_list[agent_num].configure(
            bg="lightgray",
            command=lambda num=agent_num: self.lock_agent(num)
        )

    def lock_agent(self, agent_num: int):
        """
        Locks an agent from being selected by the user.
        :param agent_num: Integer representing the index of the agent in the agent_buttons list
        """
        agent_name = self.agent_button_list[agent_num].cget("text")
        if agent_name in DEFAULT_AGENTS:
            return
        self.settings["unlocked_agents"].remove(agent_name)

        self.agent_button_list[agent_num].configure(
            bg="gray",
            command=lambda num=agent_num: self.unlock_agent(num)
        )

    def toggle_settings(self) -> None:
        """
        Toggle settings panel on/off
        """
        try:
            self.settings["img_delay_time"] = float(self.settings_buttons["img_delay_entry"].get())
        except ValueError:
            self.settings["img_delay_time"] = DEFAULT_SETTINGS["img_delay_time"]

        settings_cog = self.UI_elements["settings_cog"]
        if self.show_settings:
            settings_cog.configure(bg="white")
            self.show_settings = False
            for key in self.settings_buttons:
                self.settings_buttons[key].grid_remove()
        else:
            settings_cog.configure(bg="black")
            self.show_settings = True
            for key in self.settings_buttons:
                self.settings_buttons[key].grid()
        self.change_agents(self.show_settings)

    def change_agents(self, enable_change: bool) -> None:
        """
        Toggle whether the user can change which agents are unlocked.
        :param enable_change: True if the user can change which agents are unlocked, False otherwise.
        """
        if enable_change:
            for i in range(len(self.settings["unlocked_agents"])):
                self.agent_button_list[i].configure(
                    background="lightgray",
                    command=lambda num=i: self.lock_agent(num),
                )
            for i in range(len(self.settings["unlocked_agents"]), len(AGENT_LIST)):
                self.agent_button_list[i]["state"] = "normal"
                self.agent_button_list[i].configure(
                    background="gray",
                )
        else:
            for but in self.agent_button_list:
                but.destroy()
            self.agent_button_list = []
            self.setup_agent_grid()

    def set_agent_list(self, list_mode: int) -> None:
        """
        Set the unlocked_agents list to either the default or all agents and reset the agent grid.
        :param list_mode: 0 for default agents, 1 for all agents
        """
        match list_mode:
            case 0:
                self.settings["unlocked_agents"] = list(DEFAULT_AGENTS)  # Convert to list, to prevent using same reference
            case 1:
                self.settings["unlocked_agents"] = list(AGENT_LIST)  # Convert to list, to prevent using same reference

        self.toggle_settings()
        for but in self.agent_button_list:
            but.destroy()
        self.agent_button_list = []
        self.setup_agent_grid()

    def toggle_auto_restart(self) -> None:
        """
        Toggle whether the program auto restarts for the next game
        """
        if self.settings["auto_restart"]:
            self.settings["auto_restart"] = False
            self.settings_buttons["auto_restart_toggle"].configure(
                bg="#ff4b50",
            )
        else:
            self.settings["auto_restart"] = True
            self.settings_buttons["auto_restart_toggle"].configure(
                bg="#79c7c0",
            )

    def start_instalocker(self) -> None:
        """
        Run the instalocker program
        """
        try:
            self.settings["img_delay_time"] = float(self.settings_buttons["img_delay_entry"].get())
        except ValueError:
            self.settings["img_delay_time"] = DEFAULT_SETTINGS["img_delay_time"]
        agent_num = self.settings["unlocked_agents"].index(self.settings["selected_agent"])
        self.IL_thread = threading.Thread(target=self.run_instalocker, args=(
            agent_num,
            self.settings["img_delay_time"],
            self.settings["play_screen_delay_time"]
        )
                                          )
        self.IL_thread.start()
        run_button = self.UI_elements["run_button"]
        run_button.configure(
            text="Stop",
            command=lambda: self.stop_instalocker(),
        )

    def stop_instalocker(self) -> None:
        """
        Stop the instalocker program
        """
        try:
            self.IL.is_active = False
        except AttributeError:
            # If the instalocker thread has not been started yet, do nothing.
            pass

        run_button = self.UI_elements["run_button"]
        run_button.configure(
            text="Run",
            command=lambda: self.start_instalocker(),
        )
        status_label = self.UI_elements["status_label"]
        status_label.configure(
            text="Waiting for start",
            fg="lightgreen"
        )

    def run_instalocker(self, agent_num: int, img_delay_time: float, play_screen_delay_time: float) -> None:
        """
        Run the instalocker program as a separate thread
        :param agent_num: Integer representing the index of the agent in the users' agent lock screen
        :param img_delay_time: Float representing the time between grabbing images in seconds
        :param play_screen_delay_time: Float representing the time between grabbing images while in game in seconds
        """
        self.IL = InstaLocker(agent_num, img_delay_time, play_screen_delay_time)
        self.IL.is_active = True

        while self.IL.is_active:
            status_label = self.UI_elements["status_label"]
            status_label.configure(
                text="Waiting for agent select",
                fg="yellow"
            )

            self.IL.run()

            if not self.settings["auto_restart"]:
                self.IL.is_active = False

            status_label = self.UI_elements["status_label"]
            status_label.configure(
                text="Waiting for main menu",
                fg="yellow"
            )
            if not self.IL.wait_for_play_screen():
                self.IL.is_active = False

        self.stop_instalocker()


def get_settings(path: str):
    """
    Get the settings from the settings file, or create a new settings file if it doesn't exist.
    :param path: Path to the settings file
    :return: Dictionary containing the settings
    """
    if not os.path.exists(path):
        with open(path, "w") as settings_file:
            settings_file.write(json.dumps(DEFAULT_SETTINGS, indent=4))
    with open(path, "r") as settings_file:
        settings = json.load(settings_file)

    new_settings = {}
    # Remove unused settings
    for setting in settings.keys():
        if setting in DEFAULT_SETTINGS.keys():
            new_settings[setting] = settings[setting]

    # Add missing settings
    for setting in DEFAULT_SETTINGS.keys():
        if setting not in settings:
            new_settings[setting] = DEFAULT_SETTINGS[setting]

    return new_settings


def get_locked_agents(unlocked_agents: list) -> list[str]:
    """
    Get a list of all locked agents based on the unlocked_agents list and the global AGENT_LIST
    :param unlocked_agents: List of unlocked agents
    """
    locked_agents = []
    for agent in AGENT_LIST:
        if agent not in unlocked_agents:
            locked_agents.append(agent)
    return locked_agents


def get_button_texts(button_list: list) -> list[str]:
    """
    Get the text of all buttons from a list of buttons
    :param button_list: List of buttons with text
    """
    texts = []
    for but in button_list:
        texts.append(but.cget("text"))
    return texts


def float_validation(text: str) -> bool:
    """
    Validate that a char is a valid float character
    :param text: String to validate
    :return: True if the string is a valid float, False otherwise
    """
    if text == ".":
        return True
    try:
        float(text)
        return True
    except ValueError:
        return False
