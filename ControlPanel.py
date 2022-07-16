import json
import threading

from tkinter import *

from constants import *
from helpers import get_settings, get_button_texts, float_validation
from InstaLocker import InstaLocker
from AgentGrid import AgentGrid
from SettingsPanel import SettingsPanel


class ControlPanel(Tk):
    def __init__(self):
        super().__init__()

        self.buy_menu = Frame(self)  # Frame for first round buy menu

        # Setup label for background image
        background_label = Label(self)

        # self.agent_grid = Canvas(self, height=200, width=600)  # Grid of agents
        self.settings_canvas = Canvas(self)  # Canvas that toggles with settings

        self.settings = get_settings(f"{CURRENT_DIR}\\settings.json")
        self.show_settings = False  # Whether the settings panel is shown
        self.show_buy_menu = False  # Whether the first round buy menu is shown

        self.IL = None  # Object of instalocker class, for instalocking
        self.IL_thread = None  # Thread for running actual instalocker

        self.agent_grid = AgentGrid(self)
        self.settings_panel = SettingsPanel(self)

        # All miscellaneous buttons and labels
        self.UI_elements = {
            "background_label": background_label,
        }

    def start(self):
        """
        Start the program
        """
        self.setup_main_window()
        self.agent_grid.setup()

        self.setup_settings_panel()

        self.mainloop()

    def setup_main_window(self) -> None:
        """
        Set up the main window, including title and size
        """
        self.title("Valorant Instalocker")
        self.minsize(850, 500)
        self.maxsize(960, 540)
        self.geometry("960x540")  # Default size
        self.iconbitmap(f"{CURRENT_DIR}\\img\\logo.ico")

        # Setup background image
        background_image = PhotoImage(file=f"{CURRENT_DIR}\\img\\iceboxBackground.png")
        background_label = self.UI_elements["background_label"]
        background_label.configure(
            image=background_image
        )
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image  # Fixes issue with lost reference for image

        title = Label(self, text="Valorant Instalocker", fg="#ff4b50", font="Rockwell 30", bg="#000000")
        title.pack(pady=10)

    def setup_settings_panel(self) -> None:
        self.settings_panel.setup()

        status_label = Label(
            self,
            text="Waiting for start",
            fg="lightgreen",
            bg="black",
            font="Rockwell 20"
        )
        status_label.pack()

        run_button = Button(
            self,
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

    def setup_buy_menu(self) -> None:
        self.buy_menu.configure(
            bg="black",
            height=500,
            width=500,

        )
        Button(self.buy_menu, text="Buy").pack()
        self.buy_menu.grid(row=0, column=0, sticky="nsew")

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

        for but in self.agent_grid.buttons[:len(self.settings["unlocked_agents"])]:
            but.configure(
                bg="white"
            )
        self.agent_grid.buttons[agent_num].configure(
            bg="black"
        )

    def unlock_agent(self, agent_num: int):
        """
        Unlocks an agent to be selected by the user.
        :param agent_num: Integer representing the index of the agent in the agent_buttons list
        """
        button_texts = get_button_texts(self.agent_grid.buttons)

        self.settings["unlocked_agents"].append(button_texts[agent_num])
        self.settings["unlocked_agents"] = sorted(self.settings["unlocked_agents"])
        self.agent_grid.buttons[agent_num].configure(
            bg="lightgray",
            command=lambda num=agent_num: self.lock_agent(num)
        )

    def lock_agent(self, agent_num: int):
        """
        Locks an agent from being selected by the user.
        :param agent_num: Integer representing the index of the agent in the agent_buttons list
        """
        agent_name = self.agent_grid.buttons[agent_num].cget("text")
        if agent_name in DEFAULT_AGENTS:
            return
        self.settings["unlocked_agents"].remove(agent_name)

        self.agent_grid.buttons[agent_num].configure(
            bg="gray",
            command=lambda num=agent_num: self.unlock_agent(num)
        )

    def toggle_buy_menu(self) -> None:
        """
        Toggle the menu for selecting first round buy
        """
        pass

    def change_agents(self, enable_change: bool) -> None:
        """
        Toggle whether the user can change which agents are unlocked.
        :param enable_change: True if the user can change which agents are unlocked, False otherwise.
        """
        agent_buttons = self.agent_grid.buttons
        if enable_change:
            for i in range(len(self.settings["unlocked_agents"])):
                agent_buttons[i].configure(
                    background="lightgray",
                    command=lambda num=i: self.lock_agent(num),
                )
            for i in range(len(self.settings["unlocked_agents"]), len(AGENT_LIST)):
                agent_buttons[i]["state"] = "normal"
                agent_buttons[i].configure(
                    background="gray",
                )
        else:
            self.agent_grid.destroy_buttons()
            self.agent_grid.setup()

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

        self.settings_panel.toggle_settings()
        self.agent_grid.destroy_buttons()
        self.agent_grid.setup()

    def start_instalocker(self) -> None:
        """
        Run the instalocker program
        """
        try:
            self.settings["img_delay_time"] = float(self.settings_panel.buttons["img_delay_entry"].get())
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
