from tkinter import *
from tkinter import ttk, colorchooser, filedialog
import tkinter as tk
import PIL
from PIL import ImageGrab
from neuralNet import Network
import imageToMNIST as itm

class Paint:
    def __init__(self, master):
        self.brain = Network()
        self.master = master
        self.old_x = None
        self.old_y = None
        self.setup()
        self.c.bind('<B1-Motion>', self.write)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def reset(self, e):
        self.old_x = None
        self.old_y = None

    def write(self, e):
        if self.old_x and self.old_y:
            self.c.create_line( self.old_x,
                                self.old_y,
                                e.x,
                                e.y,
                                width=40,
                                fill='black',
                                capstyle=ROUND,
                                smooth=True)
        self.old_x = e.x
        self.old_y = e.y

    def clear(self):
        self.c.delete(ALL)

    def read(self):
        x = self.master.winfo_rootx() + self.c.winfo_x()
        y = self.master.winfo_rooty() + self.c.winfo_y() + 41
        x1 = x + self.c.winfo_width()
        y1 = y + self.c.winfo_height() - 41
        coords = [x, y, x1, y1]
        PIL.ImageGrab.grab(coords).save('image.png')
        mnistImage = itm.convertImage('./image.png')
        readNum = self.brain.predict_digit(mnistImage)
        label = tk.Label(self.c, text=readNum, bd=1, relief='solid', font='Helvetica 32 bold')
        label.place(relx=1.0, rely=1.0, anchor='se')

    def setup(self):
        self.c = Canvas(self.master, width=400, height=400, bg='white')
        self.c.pack(fill=BOTH, expand=True)

        clear_button = tk.Button(self.c, width=25, height=2, text='Clear', command=self.clear)
        read_button = tk.Button(self.c, width=25, height=2, text='Read', command=self.read)
        clear_button.place(x=0, y=0)
        read_button.place(x=220, y=0)

root = Tk()
Paint(root)
root.title("Digit Classifier")
root.mainloop()
