import tkinter
from tkinter import *
import time
import random
import re
import ServerCoAP
from tkinter import ttk
from GetApiData import GetAPI


class MainApp():
    def __init__(self):
        self.root=Tk()
        self.root.geometry("800x600")
        self.initLabels()
        self.initEntries()
        self.initButtons()
        self.initLogBox()
        self.server = ""


    def initEntries(self):
        #ip
        self.ipContent = StringVar()
        self.ipEntry = Entry(self.root,textvariable=self.ipContent)
        self.ipEntry.place(x=50,y=30)

        #port
        self.portContent = StringVar()
        self.portEntry = Entry(self.root, textvariable=self.portContent)
        self.portEntry.place(x=320, y=30)

        #version
        self.versionContent = StringVar()
        self.versionEntry = Entry(self.root, textvariable=self.versionContent)
        self.versionEntry.place(x=600,y = 30)
    def initLabels(self):
        #ip
        self.ipLabel = Label(self.root,text="IP:")
        self.ipLabel.place(x=30,y=30)

        #port
        self.portLabel = Label(self.root,text="PORT:")
        self.portLabel.place(x=280,y=30)

        #version
        self.versionLabel = Label(self.root,text="VERSION:")
        self.versionLabel.place(x=540,y=30)

    def initButtons(self):
        #wait
        self.waitButtonLabel = StringVar()
        self.waitButtonLabel.set("Free")
        self.waitButton = Button(self.root,textvariable=self.waitButtonLabel,command=self.RandomWait)
        self.waitButton.place(x=120,y=100,width=100,height=30)

        #reset
        self.resetButton = Button(self.root,text="Reset",command= self.Reset)
        self.resetButton.place(x=260,y = 100,width=100,height=30)

        self.startServer = Button(self.root, text="StartServer", command= self.StartServer)
        self.startServer.place(x=540, y=100, width=100, height=30)

        self.stopServer = Button(self.root, text="StopServer", command= self.StopServer)
        self.stopServer.place(x=400, y=100, width=100, height=30)

        #clear interface
        self.clear = Button(self.root, text="Clear", command=lambda : self.log.delete(1.0, END))
        self.clear.place(x=540, y=70, width=100, height=30)

    def initLogBox(self):
        #text area of the log
        self.log = Text(self.root,bg="darkgreen")
        self.log.place(x = 100,y=140,width = 600,height=390)

        #scrollbar of the log
        self.scroll = Scrollbar(self.root,command=self.log.yview)
        self.scroll.place(x=690,y = 140,height = 390)
        self.log['yscrollcommand'] = self.scroll.set
    def RandomWait(self):
        self.server.SetDelayFlag(1)

    def Reset(self):
        self.server.SetResetFlag(1)

    def StopServer(self):
        if self.server != "":
            self.server.ShutDownServer()
            self.server = ""

    def StartServer(self):
        if self.server == "":
            (ip, port, vers) = self.getInput()
            self.server = ServerCoAP.ServerCOAP(ip, port, self)
            self.server.SetVersion(vers)
            self.server.StartServer()
            self.print(ip," server started on " + port)

    def getInput(self):
        p = 1
        if(not re.match("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",self.ipContent.get())):
            p = 0
        try:
            if(not(int(self.portContent.get()) > 0 and int(self.portContent.get()) < 65535)):
                p = 0
            if(not(int(self.versionContent.get()) >= 0 and int(self.versionContent.get()) <= 3)):
                p = 0
        except:
            p = 0
        if(p == 1):
            return (self.ipContent.get(),self.portContent.get(),self.versionContent.get())
        else:
            return None

    def print(self,addr,info):
        self.log.insert(INSERT,str(addr) + ": " + str(info) + '\n')
    def startMainProgramLoop(self):
        self.root.mainloop()

app = MainApp()
app.startMainProgramLoop()