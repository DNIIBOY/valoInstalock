from constants import *
from tkinter import *

from helpers import get_locked_agents


class AgentGrid(Canvas):
    """
    Grid of all agents, to be selected by the user.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.buttons = []  # Contains button objects for all agents

    def setup(self) -> None:
        self.configure(
            height=200,
            width=600,
            bg="white"
        )

        i = 0
        for y in range(2):
            # Account for extra agent on top row, when there is and odd agent count
            odd_offset = int(len(AGENT_LIST) % 2 == 1 and y == 0)
            for x in range((len(AGENT_LIST) // 2) + odd_offset):
                if i < len(self.parent.settings["unlocked_agents"]):  # All unlocked agents first
                    self.buttons.append(AgentButton(self, agent_number=i, locked=False))
                else:  # Locked agents last
                    self.buttons.append(AgentButton(self, agent_number=i, locked=True))

                self.buttons[i].grid(column=x, row=y, padx=1, pady=1)
                i += 1

        # Select default agent
        try:
            self.buttons[self.parent.settings["unlocked_agents"].index(self.parent.settings["selected_agent"])].configure(bg="black")
        except ValueError:
            # If the selected agent is not in the unlocked agents list, select the first unlocked agent
            self.buttons[0].configure(bg="black")
            self.parent.settings["selected_agent"] = self.parent.settings["unlocked_agents"][0]

        self.pack(pady=10)

    def destroy_buttons(self) -> None:
        """
        Destroy all buttons in the agent grid and reset the buttons list.
        :return:
        """
        for button in self.buttons:
            button.destroy()
        self.buttons = []


class AgentButton(Button):
    def __init__(self, parent: AgentGrid, agent_number: int, locked: bool):
        """
        Button in the agent grid
        :param parent: The parent AgentGrid object
        :param agent_number: The index of the agent in the grid
        :param locked: Whether the agent is locked or not
        """
        super().__init__(parent)
        if locked:
            locked_agents = get_locked_agents(parent.parent.settings["unlocked_agents"])
            self.configure(
                text=locked_agents[agent_number - len(parent.parent.settings["unlocked_agents"])],
                height=3,
                width=8,
                background="white",
                foreground="#ff4b50",
                font="Rockwell 12",
                command=lambda i=agent_number: parent.parent.unlock_agent(i),
            )
            self["state"] = "disabled"
        else:
            self.configure(
                text=parent.parent.settings["unlocked_agents"][agent_number],
                height=3,
                width=8,
                background="white",
                foreground="#ff4b50",
                font="Rockwell 12",
                command=lambda i=agent_number: parent.parent.select_agent(i),
            )
