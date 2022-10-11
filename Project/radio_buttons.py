from tkinter import *
from PIL import ImageTk,Image

root = Tk()
root.title("Film Nerd")
root.iconbitmap("images/tripod.ico")

r = IntVar() #StrVar()
r.set(2)

def clicked(value):
    myLabel = Label(root, text=value)
    myLabel.pack()

#one way to do it
#Radiobutton(root, text="Option 1", variable=r, value=1, command=lambda: clicked(r.get())).pack()
#Radiobutton(root, text="Option 2", variable=r, value=2, command=lambda: clicked(r.get())).pack()

#another way
TOPPINGS = [
    ("Pepperoni","Pepperoni"),
    ("Cheese","Cheese"),
    ("Onion","Onion"),
    ("Mushroom","Mushroom")
]

pizza = StringVar()
pizza.set("Pepperoni")

for text, topping in TOPPINGS:
    Radiobutton(root, text=text, variable=pizza, value=topping).pack(anchor=W)

#myButton = Button(root, text="Click Me!", command=lambda: clicked(r.get()))
myButton = Button(root, text="Click Me!", command=lambda: clicked(pizza.get()))
myButton.pack()

mainloop()