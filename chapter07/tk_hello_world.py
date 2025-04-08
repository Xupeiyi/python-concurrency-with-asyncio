import tkinter
from tkinter import ttk


window = tkinter.Tk()
window.title("Hello World app")
window.geometry("200x100")


def say_hello():
    print("Hello World!")


hello_button = ttk.Button(window, text='Say Hello', command=say_hello)
hello_button.pack()
window.mainloop()
