from tkinter import *
from webbrowser import open_new
from UpdateHandler import UpdateHandler


class StatusField(Canvas):
    """
    An area containing information such as the current state of the program, and the run button
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.show_settings = False

        self.version_button = VersionButton(self)  # VersionButton instance, to check for updates
        self.status_label = Label(self)
        self.run_button = Button(self)

    def setup(self):
        self.configure(
            height=700,
            width=600,
            bg="black"
        )

        self.version_button.setup()
        self.version_button.pack(side=TOP, padx=10, pady=2)

        self.status_label.configure(
            text="Waiting for start",
            fg="lightgreen",
            bg="black",
            font="Rockwell 20"
        )
        self.status_label.pack(side=TOP, padx=10, pady=0)

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


class VersionButton(Button):
    def __init__(self, parent):
        """
        Button to display the current version of the program
        """
        super().__init__(parent)
        self.UH = UpdateHandler()

    def setup(self) -> None:
        """
        Set up the button to display the current version of the program and check for updates
        """
        releases_url = "https://github.com/DNIIBOY/valoInstalock/releases"
        self["state"] = "disabled"
        self.configure(
            font="Rockwell 10",
            bg="black",
            fg="#ff4b50",
            disabledforeground="#bbbbbb",
            borderwidth=0,
            command=lambda url=releases_url: open_new(url),
            activebackground="black",
            activeforeground="#ff4b50",
        )
        if self.UH.is_latest_version():
            self.configure(
                text=self.UH.current_version,
            )
        elif self.UH.is_future_version():
            self.configure(
                text=self.UH.current_version + " (Dev)",
            )
        else:
            self.configure(
                text=self.UH.current_version + " (Outdated)",
            )
            self["state"] = "normal"
