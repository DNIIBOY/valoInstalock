from tkinter import *


class StatusField(Canvas):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.show_settings = False

        self.status_label = Label(self)
        self.run_button = Button(self)

    def setup(self):
        self.configure(
            height=700,
            width=600,
            bg="black"
        )

        self.status_label.configure(
            text="Waiting for start",
            fg="lightgreen",
            bg="black",
            font="Rockwell 20"
        )
        self.status_label.pack(side=TOP, padx=10, pady=5)

        self.run_button.configure(
            text="Run",
            font="Rockwell 15",
            command=lambda: self.parent.start_instalocker(),
            height=2,
            width=12,
            bg="#79c7c0",
            fg="#000000",
        )
        self.run_button.pack(side=BOTTOM, padx=90, pady=15)

        self.pack(side=TOP, pady=8)
