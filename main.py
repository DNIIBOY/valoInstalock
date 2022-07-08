from tkinter import *
from PIL import ImageTk, Image, ImageGrab


class InstaLocker:
    def __init__(self):
        self.main_window = Tk()

    def start(self):
        self.setup_main_window()

    def setup_main_window(self):
        self.main_window.title("Valorant Instalocker")
        self.main_window.minsize(480, 270)
        self.main_window.geometry("640x360")  # Default size

        # Setup background image
        background_image = ImageTk.PhotoImage(file="img/iceboxBackground.png")
        background_label = Label(self.main_window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image  # Fixes issue with lost reference for image

        title = Label(self.main_window, text="Valorant Instalocker", fg="#ff4b50", font="Georgia 30", bg="#000000")
        title.pack(pady=10)


if __name__ == '__main__':
    IL = InstaLocker()
    IL.start()
    IL.main_window.mainloop()
