from tkinter import *
from PIL import ImageTk, Image, ImageGrab
import json

AGENT_LIST = [
    "Astra",
    "Breach",
    "Brimstone",
    "Chamber",
    "Cypher",
    "Fade",
    "Jett",
    "KAY/O",
    "Killjoy",
    "Neon",
    "Omen",
    "Phoenix",
    "Raze",
    "Reyna",
    "Sage",
    "Skye",
    "Sova",
    "Viper",
    "Yoru"
]
DEFAULT_AGENTS = ["Brimstone", "Jett", "Phoenix", "Sage", "Sova"]


class InstaLocker:
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
        self.show_settings = False

        self.unlocked_agents = self.settings["unlocked_agents"]
        self.selected_agent = self.settings["default_agent"]

        self.agent_button_list = []  # Contains button objects for all agents

    def start(self):
        self.setup_main_window()
        self.setup_agent_grid()
        self.agent_canvas.pack(pady=25)

        self.setup_settings_panel()

        self.main_window.mainloop()

    def setup_main_window(self):
        self.main_window.title("Valorant Instalocker")
        self.main_window.minsize(480, 270)
        self.main_window.geometry("640x360")  # Default size

        title = Label(self.main_window, text="Valorant Instalocker", fg="#ff4b50", font="Georgia 30", bg="#000000")
        title.pack(pady=10)

    def setup_agent_grid(self):
        self.agent_canvas.configure(
            bg="white"
        )

        locked_agents = []
        for agent in AGENT_LIST:
            if agent not in self.unlocked_agents:
                locked_agents.append(agent)

        print("Locked", locked_agents)

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

    def setup_settings_panel(self):
        self.settings_frame.pack()
        self.settings_canvas.pack()
        img = PhotoImage(file="img/redcog.png")
        cog_img = img.subsample(3, 3)

        cog = Button(self.main_window, image=cog_img, command=lambda: self.toggle_settings(cog))
        cog.image = cog_img
        cog.pack()

    def update_settings_file(self):
        self.unlocked_agents = sorted(self.unlocked_agents)
        self.settings["unlocked_agents"] = self.unlocked_agents
        self.settings["default_agent"] = self.selected_agent

        json_object = json.dumps(self.settings, indent=4)
        with open("settings.json", "w") as settings_file:
            settings_file.write(json_object)

    def select_agent(self, agent_num: int):
        self.selected_agent = self.unlocked_agents[agent_num]
        print(self.selected_agent)
        for but in self.agent_button_list[:len(self.unlocked_agents)]:
            but.configure(
                bg="white"
            )
        self.agent_button_list[agent_num].configure(
            bg="black"
        )

    def unlock_agent(self, agent_num: int):
        locked_agents = []
        for agent in AGENT_LIST:
            if agent not in self.unlocked_agents:
                locked_agents.append(agent)

        self.unlocked_agents.append(locked_agents[agent_num - len(self.unlocked_agents)])
        self.unlocked_agents = sorted(self.unlocked_agents)
        print(self.unlocked_agents)
        self.agent_button_list[agent_num].configure(
            bg="lightgray"
        )

    def lock_agent(self, agent_num: int):
        self.unlocked_agents.pop(agent_num)
        self.agent_button_list[agent_num].configure(
            bg="gray"
        )

    def toggle_settings(self, btn: Button):
        if self.show_settings:
            btn.configure(bg="white")
            self.show_settings = False
        else:
            btn.configure(bg="black")
            self.show_settings = True
        self.change_agents(self.show_settings)

    def change_agents(self, enable_change: bool):
        if enable_change:
            for i in range(len(self.unlocked_agents)):
                self.agent_button_list[i].configure(
                    background="lightgray",
                    command=""
                )
            for i in range(len(self.unlocked_agents), len(AGENT_LIST)):
                self.agent_button_list[i]["state"] = "normal"
                self.agent_button_list[i].configure(
                    background="gray"
                )
        else:
            for but in self.agent_button_list:
                but.destroy()
            self.agent_button_list = []
            self.setup_agent_grid()


if __name__ == '__main__':
    IL = InstaLocker()
    # IL.unlocked_agents = DEFAULT_AGENTS
    IL.start()
    IL.update_settings_file()
