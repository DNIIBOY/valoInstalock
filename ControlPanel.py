from tkinter import *
from time import sleep
import json
import threading

from constants import *
from helpers import get_settings, get_button_texts

from AgentGrid import AgentGrid
from SpikeTimerWindow import SpikeTimerWindow
from BuyMenu import BuyMenu
from SettingsPanel import SettingsPanel
from StatusField import StatusField

from AutoBuyer import AutoBuyer
from InstaLocker import InstaLocker
from SpikeTimer import SpikeTimer


class ControlPanel(Tk):
    """
    The main controlpanel for all features of the program
    """

    def __init__(self):
        super().__init__()

        # Setup label for background image
        self.background_label = Label(self)

        self.settings_canvas = Canvas(self)  # Canvas that toggles with settings
        self.StatusField = StatusField(self)  # Status field with run button and status label

        self.settings = get_settings(f"{CURRENT_DIR}\\settings.json")

        self.AB = None  # Object of autobuyer class, for autobuying
        self.IL = None  # Object of instalocker class, for instalocking
        self.ST = None  # Object of spike timer class, for spike timer

        self.main_thread = None  # Thread for running instalocker and other functions
        self.spike_timer_thread = None  # Thread for running spike timer

        self.agent_grid = AgentGrid(self)
        self.settings_panel = SettingsPanel(self)
        self.buy_menu = BuyMenu(self)
        self.spike_timer_window = SpikeTimerWindow(self)

    def start(self):
        """
        Start the program
        """
        print("Setting up main window...")
        self.setup_main_window()
        print("Setting up agent grid...")
        self.agent_grid.setup()
        print("Setting up settings panel...")
        self.settings_panel.setup()
        print("Setting up status field...")
        self.StatusField.setup()
        print("Setting up buy menu...")
        self.buy_menu.setup()
        print("Setting up spike timer...")
        self.spike_timer_window.setup()
        print("Running program...")
        self.mainloop()

    def setup_main_window(self) -> None:
        """
        Set up the main window, including title and size
        """
        self.title("Valorant Instalocker")
        self.minsize(962, 549)
        self.maxsize(976, 549)  # Rez of background img
        self.geometry("976x549")  # Default size
        # self.resizable(False, False)
        self.iconbitmap(f"{CURRENT_DIR}\\img\\logo.ico")

        # Setup background image
        background_image = PhotoImage(file=f"{CURRENT_DIR}\\img\\iceboxBackground.png")
        self.background_label.configure(
            image=background_image
        )
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.image = background_image  # Fixes issue with lost reference for image

        title = Label(self, text="Valorant Instalocker", fg="#ff4b50", font="Rockwell 30", bg="#000000")
        title.pack(pady=10)

    def update_settings_file(self) -> None:
        """
        Update settings file with current settings
        """
        json_object = json.dumps(self.settings, indent=4)
        with open(f"{CURRENT_DIR}\\settings.json", "w") as settings_file:
            settings_file.write(json_object)

    def update_img_delay(self, new_delay: str):
        """
        Update the img_delay setting
        :param new_delay: New delay value to read the value from
        """
        if new_delay:
            self.settings["img_delay"] = float(new_delay)
        else:
            self.settings["img_delay"] = DEFAULT_SETTINGS["img_delay"]

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

        # Make all agents, that aren't picked, white
        for but in self.agent_grid.buttons[:len(self.settings["unlocked_agents"])]:
            but.configure(
                bg="white"
            )
        # Make the selected agent black
        self.agent_grid.buttons[agent_num].configure(
            bg="black"
        )

    def unlock_agent(self, agent_num: int):
        """
        Unlocks an agent to be selected by the user.
        :param agent_num: Integer representing the index of the agent in the agent_buttons list
        """
        button_texts = get_button_texts(self.agent_grid.buttons)  # Get the exact order of agents, from the agent grid

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
        if agent_name in DEFAULT_AGENTS:  # Don't allow locking of default agents
            return

        self.settings["unlocked_agents"].remove(agent_name)
        self.agent_grid.buttons[agent_num].configure(
            bg="gray",
            command=lambda num=agent_num: self.unlock_agent(num)
        )

    def change_agents(self, enable_change: bool) -> None:
        """
        Toggle whether the user can change which agents are unlocked.
        :param enable_change: True if the user can change which agents are unlocked, False otherwise.
        """
        agent_buttons = self.agent_grid.buttons
        if enable_change:  # Toggle on
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
        else:  # Toggle off
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
        agent_num = self.settings["unlocked_agents"].index(self.settings["selected_agent"])
        self.main_thread = threading.Thread(target=self.main_function, args=(
            agent_num,
            self.settings["img_delay"],
            self.settings["play_screen_delay_time"]
        )
                                            )
        self.main_thread.start()

        if self.settings["show_spike_timer"]:
            self.spike_timer_thread = threading.Thread(target=self.spike_timer_function)
            self.spike_timer_thread.start()

        self.StatusField.run_button.configure(
            text="Stop",
            command=lambda: self.stop_instalocker(),
        )

    def stop_instalocker(self) -> None:
        """
        Stop the instalocker program
        """
        for module in [self.AB, self.IL, self.ST]:
            try:
                module.is_active = False
            except AttributeError:
                pass

        self.StatusField.run_button.configure(
            text="Run",
            command=lambda: self.start_instalocker(),
        )
        self.StatusField.status_label.configure(
            text="Waiting for start",
            fg="lightgreen"
        )

    def main_function(self, agent_num: int, img_delay: float, play_screen_delay_time: float) -> None:
        """
        Run the instalocker program as a separate thread
        :param agent_num: Integer representing the index of the agent in the users' agent lock screen
        :param img_delay: Float representing the time between grabbing images in seconds
        :param play_screen_delay_time: Float representing the time between grabbing images while in game in seconds
        """
        self.IL = InstaLocker(agent_num, img_delay, play_screen_delay_time)
        self.IL.is_active = True

        while self.IL.is_active:
            self.StatusField.status_label.configure(
                text="Waiting for agent select",
                fg="yellow"
            )

            self.IL.run()

            if self.settings["auto_buy"] and self.IL.is_active:
                self.AB = AutoBuyer(img_delay, self.settings["shop_settings"])
                self.StatusField.status_label.configure(
                    text="Waiting for game load",
                    fg="yellow"
                )
                self.AB.run()

            if not self.settings["auto_restart"] or not self.IL.is_active:
                # If not set to auto restart, or if the instalocker has been stopped, break
                self.IL.is_active = False
                break

            self.StatusField.status_label.configure(
                text=("Checking for spike plants" if self.settings["show_spike_timer"] else "Waiting for main menu"),
                fg="yellow"
            )

            if not self.IL.wait_for_play_screen():
                self.IL.is_active = False

        if self.settings["show_spike_timer"] and self.ST.is_active:
            self.StatusField.status_label.configure(
                text="Checking for spike plants",
                fg="yellow"
            )
        else:
            try:
                self.stop_instalocker()
            except RuntimeError:
                # If the main window has been closed, do nothing.
                pass

    def spike_timer_function(self) -> None:
        """
        Function to run the spike timer
        """
        self.ST = SpikeTimer(self.settings["img_delay"])
        self.ST.is_active = True
        ST_was_active = False
        diffusing = False
        while self.ST.is_active:
            spike_status = self.ST.run()
            match spike_status:
                case -1:
                    diffusing = False
                    if not ST_was_active:
                        continue
                    sleep(3)
                    self.spike_timer_window.hide()
                    ST_was_active = False

                case 0:
                    self.spike_timer_window.update_time(self.ST.time)

                    if not ST_was_active:
                        self.spike_timer_window.show()
                        ST_was_active = True

                    if diffusing:
                        diffusing = False
                        self.spike_timer_window.hide_finish_time()

                case 1:
                    self.spike_timer_window.update_time(self.ST.time)
                    if not diffusing:
                        diffusing = True
                        self.spike_timer_window.update_finish_time(round(self.ST.time - 7, 1))

                case 2:
                    self.spike_timer_window.update_time(self.ST.time)
                    if not diffusing:
                        diffusing = True
                        self.spike_timer_window.update_finish_time(round(self.ST.time - 3.5, 1))
