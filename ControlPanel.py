import json
import threading
import os

from tkinter import *
from constants import *
from InstaLocker import InstaLocker


class ControlPanel:
    def __init__(self):
        self.main_window = Tk()  # Root window

        # Setup background image
        background_image = PhotoImage(file="img/iceboxBackground.png")
        background_label = Label(self.main_window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image  # Fixes issue with lost reference for image

        self.agent_canvas = Canvas(self.main_window, height=200, width=600)  # Grid of agents
        self.settings_canvas = Canvas(self.main_window, height=100, width=600)  # Canvas for settings and settings button
        self.settings_frame = Frame(self.settings_canvas, bg="#000000")  # Frame hidden settings

        try:
            # Load settings from json file
            with open("settings.json", "r") as settings_file:
                self.settings = json.load(settings_file)
        except FileNotFoundError:
            # Use default settings if no settings file exists
            self.settings = {
                "unlocked_agents": ["Brimstone", "Jett", "Phoenix", "Sage", "Sova"],
                "default_agent": "Brimstone"
            }
        self.show_settings = False  # Whether the settings panel is shown

        self.is_running = False
        self.IL = None  # Object of instalocker class, for instalocking
        self.IL_thread = None  # Thread for running actual instalocker

        self.unlocked_agents = self.settings["unlocked_agents"]
        self.selected_agent = self.settings["default_agent"]

        self.agent_button_list = []  # Contains button objects for all agents

    def start(self):
        """
        Start the program
        """
        self.setup_main_window()
        self.setup_agent_grid()
        self.agent_canvas.pack(pady=25)

        self.setup_settings_panel()

        self.main_window.mainloop()

    def setup_main_window(self) -> None:
        """
        Set up the main window, including title and size
        """
        self.main_window.title("Valorant Instalocker")
        self.main_window.minsize(480, 270)
        self.main_window.maxsize(960, 540)
        self.main_window.geometry("768x432")  # Default size

        title = Label(self.main_window, text="Valorant Instalocker", fg="#ff4b50", font="Georgia 30", bg="#000000")
        title.pack(pady=10)

    def setup_agent_grid(self) -> None:
        """
        Set up the agent grid
        """
        self.agent_canvas.configure(
            bg="white"
        )

        locked_agents = get_locked_agents(self.unlocked_agents)

        i = 0
        for y in range(2):
            # Account for extra agent on top row, when there is and odd agent count
            odd_offset = int(len(AGENT_LIST) % 2 == 1 and y == 0)
            for x in range((len(AGENT_LIST) // 2) + odd_offset):
                if i < len(self.unlocked_agents):  # All unlocked agents first
                    self.agent_button_list.append(
                        Button(
                            self.agent_canvas,
                            text=self.unlocked_agents[i],
                            height=3,
                            width=7,
                            background="white",
                            foreground="#ff4b50",
                            command=lambda num=i: self.select_agent(num),
                        )
                    )
                else:  # Locked agents last
                    self.agent_button_list.append(
                        Button(
                            self.agent_canvas,
                            text=locked_agents[i - len(self.unlocked_agents)],
                            height=3,
                            width=7,
                            background="white",
                            foreground="#ff4b50",
                            command=lambda num=i: self.unlock_agent(num),
                        )
                    )
                    self.agent_button_list[i]["state"] = "disabled"

                self.agent_button_list[i].grid(column=x, row=y, padx=1, pady=1)
                i += 1

        try:
            self.agent_button_list[self.unlocked_agents.index(self.selected_agent)].configure(bg="black")
        except ValueError:
            self.agent_button_list[0].configure(bg="black")

    def setup_settings_panel(self) -> None:
        """
        Set up the settings panel
        """
        self.settings_frame.pack()
        self.settings_canvas.pack()
        img = PhotoImage(file="img/redcog.png")
        cog_img = img.subsample(3, 3)

        cog = Button(self.main_window, image=cog_img, command=lambda: self.toggle_settings(cog))
        cog.image = cog_img
        cog.pack()

        default_agents_button = Button(self.settings_frame, text="Default Agents", command=lambda: self.set_agent_list(0))
        all_agents_button = Button(self.settings_frame, text="All Agents", command=lambda: self.set_agent_list(1))

        default_agents_button.pack(side=LEFT, padx=10)
        all_agents_button.pack(side=RIGHT, padx=10)

        run_button = Button(self.main_window, text="Run", command=lambda: self.start_instalocker())
        run_button.pack(side=BOTTOM)

    def update_settings_file(self) -> None:
        """
        Update settings file with current settings
        """
        self.unlocked_agents = sorted(self.unlocked_agents)
        self.settings["unlocked_agents"] = self.unlocked_agents
        self.settings["default_agent"] = self.selected_agent

        json_object = json.dumps(self.settings, indent=4)
        with open("settings.json", "w") as settings_file:
            settings_file.write(json_object)

    def select_agent(self, agent_num: int) -> None:
        """
        Selects which agent should be instalocked by the program
        :param agent_num: Integer representing the index of the agent in the unlocked_agents list
        """
        self.selected_agent = self.unlocked_agents[agent_num]
        for but in self.agent_button_list[:len(self.unlocked_agents)]:
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

        self.unlocked_agents.append(button_texts[agent_num])
        self.unlocked_agents = sorted(self.unlocked_agents)
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
        self.unlocked_agents.remove(agent_name)

        self.agent_button_list[agent_num].configure(
            bg="gray",
            command=lambda num=agent_num: self.unlock_agent(num)
        )

    def toggle_settings(self, btn: Button) -> None:
        """
        Toggle settings panel on/off
        :param btn: Button object that will change color when setting are toggled
        """
        if self.show_settings:
            btn.configure(bg="white")
            self.show_settings = False
        else:
            btn.configure(bg="black")
            self.show_settings = True
        self.change_agents(self.show_settings)

    def change_agents(self, enable_change: bool) -> None:
        """
        Toggle whether the user can change which agents are unlocked.
        :param enable_change: True if the user can change which agents are unlocked, False otherwise.
        """
        if enable_change:
            for i in range(len(self.unlocked_agents)):
                self.agent_button_list[i].configure(
                    background="lightgray",
                    command=lambda num=i: self.lock_agent(num),
                )
            for i in range(len(self.unlocked_agents), len(AGENT_LIST)):
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
                self.unlocked_agents = list(DEFAULT_AGENTS)  # Convert to list, to prevent using same reference
            case 1:
                self.unlocked_agents = list(AGENT_LIST)  # Convert to list, to prevent using same reference

        for but in self.agent_button_list:
            but.destroy()
        self.agent_button_list = []
        self.setup_agent_grid()

    def start_instalocker(self) -> None:
        """
        Run the instalocker program
        """
        self.is_running = True
        agent_num = self.unlocked_agents.index(self.selected_agent)
        self.IL_thread = threading.Thread(target=self.run_instalocker, args=(agent_num,))
        self.IL_thread.start()

    def run_instalocker(self, agent_num: int):
        """
        Run the instalocker program as a separate thread
        :param agent_num: Integer representing the index of the agent in the users' agent lock screen
        """
        self.IL = InstaLocker(agent_num)
        self.IL.run()

    def stop_instalocker(self) -> None:
        try:
            self.IL.is_active = False
        except AttributeError:
            # If the instalocker thread has not been started yet, do nothing.
            pass


def get_settings():
    """
    Get the settings from the settings file, or create a new settings file if it doesn't exist.
    :return: Dictionary containing the settings
    """
    if not os.path.exists("settings.json"):
        with open("settings.json", "w") as settings_file:
            settings_file.write(json.dumps(DEFAULT_SETTINGS, indent=4))
    with open("settings.json", "r") as settings_file:
        return json.load(settings_file)


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


if __name__ == '__main__':
    CP = ControlPanel()
    # CP.unlocked_agents = DEFAULT_AGENTS
    CP.start()
    CP.stop_instalocker()
    CP.update_settings_file()
