from tkinter import *


class SpikeTimerWindow(Canvas):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.timer_label = Label(self)
        self.finish_time_label = Label(self)
        self.time = 45.0  # Time shown on timer

    def setup(self) -> None:
        self.configure(
            bg="#454d59",
        )
        self.timer_label.configure(
            text=self.time,
            font="Rockwell 72",
            bg="#454d59",
            fg="lightgreen",
        )
        self.finish_time_label.configure(
            text=0.0,
            font="Rockwell 42",
            bg="#454d59",
            fg="green",
        )
        self.timer_label.pack(padx=10, pady=5)

    def update_time(self, new_time: float) -> None:
        """
        Update the time and color of the timer
        """
        self.time = new_time

        if new_time > 14:
            new_color = "lightgreen"
        elif new_time > 7:
            new_color = "yellow"
        else:
            new_color = "red"

        self.timer_label.configure(
            text=self.time,
            fg=new_color,
        )

    def update_finish_time(self, new_time: float) -> None:
        """
        Update the finish time and show it
        """
        new_color = "#ebeeb2" if new_time > 0 else "red"
        self.finish_time_label.configure(
            text=new_time,
            fg=new_color,
        )
        self.finish_time_label.pack(padx=10, pady=9, side=BOTTOM)

    def hide_finish_time(self) -> None:
        """
        Hide the finish time
        """
        self.finish_time_label.place_forget()

    def show(self) -> None:
        """
        Show the timer
        """
        self.place(relx=0.35, rely=0.25, relwidth=0.3, height=200)

    def hide(self) -> None:
        """
        Hide the timer
        """
        self.hide_finish_time()
        self.place_forget()
