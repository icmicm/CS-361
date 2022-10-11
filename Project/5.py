from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("Film Nerd")
root.iconbitmap("images/tripod.ico")

round_label = Label(root, text="Round 1 of 6")
round_label.grid(row=1, column=2)

root.mainloop()