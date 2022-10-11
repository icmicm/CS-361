from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog

root = Tk()
root.title("Film Nerd")
root.iconbitmap("images/tripod.ico")

def open():
    global myImage
    root.filename = filedialog.askopenfilename(initialdir="images", title="select a file", filetypes=(("png files", "*.png"), ("ico files", "*.ico")))
    myLabel = Label(root, text=root.filename).pack()
    myImage = ImageTk.PhotoImage(Image.open(root.filename))
    myImageLabel = Label(image=myImage).pack()


byButton = Button(root, text="Open File", command=open).pack()

mainloop()