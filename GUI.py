import tkinter
from tkinter import *
from tkinter import ttk
from GetApiData import GetAPI


class MainApp():
    def __init__(self,API):
        self.root=Tk()
        self.root.geometry("800x600")
        self.API=API

    def startMainProgramLoop(self):
        self.root.mainloop()