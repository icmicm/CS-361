from tkinter import *
from PIL import ImageTk,Image

root = Tk()
root.title("Film Nerd")
root.iconbitmap("images/tripod.ico")


def open():
    top = Toplevel()
    top.title("Second Window")
    top.iconbitmap("images/tripod.ico")
    lbl = Label(top, text="Hello").pack()
    btn2 = Button(top, text="Close Window", command=top.destroy).pack()

btn = Button(root, text="Open Second Window", command=open).pack()



mainloop()