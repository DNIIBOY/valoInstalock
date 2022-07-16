from constants import *
from tkinter import *

from helpers import get_locked_agents


class AgentGrid(Canvas):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.buttons = []  # Contains button objects for all agents

    def setup(self):
        self.configure(
            height=200,
            width=600,
            bg="white"
        )

        locked_agents = get_locked_agents(self.parent.settings["unlocked_agents"])

        i = 0
        for y in range(2):
            # Account for extra agent on top row, when there is and odd agent count
            odd_offset = int(len(AGENT_LIST) % 2 == 1 and y == 0)
            for x in range((len(AGENT_LIST) // 2) + odd_offset):
                if i < len(self.parent.settings["unlocked_agents"]):  # All unlocked agents first
                    self.buttons.append(
                        Button(
                            self,
                            text=self.parent.settings["unlocked_agents"][i],
                            height=3,
                            width=8,
                            background="white",
                            foreground="#ff4b50",
                            font="Rockwell 12",
                            command=lambda num=i: self.parent.select_agent(num),
                        )
                    )
                else:  # Locked agents last
                    self.buttons.append(
                        Button(
                            self,
                            text=locked_agents[i - len(self.parent.settings["unlocked_agents"])],
                            height=3,
                            width=8,
                            background="white",
                            foreground="#ff4b50",
                            font="Rockwell 12",
                            command=lambda num=i: self.parent.unlock_agent(num),
                        )
                    )
                    self.buttons[i]["state"] = "disabled"

                self.buttons[i].grid(column=x, row=y, padx=1, pady=1)
                i += 1

        # Select default agent
        try:
            self.buttons[self.parent.settings["unlocked_agents"].index(self.parent.settings["selected_agent"])].configure(bg="black")
        except ValueError:
            self.buttons[0].configure(bg="black")

        self.pack(pady=10)

    def destroy_buttons(self) -> None:
        for button in self.buttons:
            button.destroy()
        self.buttons = []
