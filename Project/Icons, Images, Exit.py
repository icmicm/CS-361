from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("Film Nerd")
root.iconbitmap("images/tripod.ico")

my_img = ImageTk.PhotoImage(Image.open("images/FILM_NERD.png"))
my_label = Label(image=my_img)
my_label.pack()

button_quit = Button(root, text="Exit Program", command=root.quit)
button_quit.pack()

root.mainloop()