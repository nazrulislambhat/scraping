from tkinter import *
myGui = Tk()
txt = StringVar()
myGui.title("Product Price App")
myGui.geometry("900x500+250+100")
def search(event=None):
    Label(myGui, text="Button has been clicked!").pack()
myGui.bind('<Return>', search)

btn_srch = Button(text="Button", fg="green", font="15", command=search).pack()

myGui.mainloop()