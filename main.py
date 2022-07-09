import tkinter
from tkinter import *
from PIL import ImageTk, Image, ImageGrab

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


class InstaLocker:
    def __init__(self):
        self.main_window = Tk()  # Root window

        # Setup background image
        background_image = ImageTk.PhotoImage(file="img/iceboxBackground.png")
        background_label = Label(self.main_window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image  # Fixes issue with lost reference for image

        self.agent_canvas = Canvas(self.main_window, height=200, width=600)  # Grid of agents

        self.unlocked_agents = []
        self.selected_agent = ""

        self.agent_button_list = []  # Contains button objects for all agents

    def start(self):
        self.setup_main_window()
        self.setup_agent_grid()

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

        i = 0
        for y in range(2):
            # Account for extra agent on top row, when there is and odd agent count
            odd_offset = int(len(AGENT_LIST) % 2 == 1 and y == 0)
            for x in range((len(AGENT_LIST) // 2) + odd_offset):
                self.agent_button_list.append(
                    Button(
                        self.agent_canvas,
                        text=AGENT_LIST[i],
                        height=3,
                        width=7,
                        background="white",
                        foreground="#ff4b50",
                        command=(lambda i=i: self.select_agent(i)),
                    )
                )

                self.agent_button_list[i].grid(column=x, row=y, padx=1, pady=1)

                i += 1

        self.agent_canvas.pack(pady=25)

    def select_agent(self, agent_num: int):
        print(agent_num)
        self.selected_agent = AGENT_LIST[agent_num]
        for but in self.agent_button_list:
            but.configure(
                bg="white"
            )
        self.agent_button_list[agent_num].configure(
            bg="black"
        )


if __name__ == '__main__':
    IL = InstaLocker()
    IL.start()
