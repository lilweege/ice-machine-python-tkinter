import tkinter as tk
from tkinter import *
from threading import Timer
#from PIL import Image, ImageTk
# Import gpiozero for Raspberry
# The Dispense will control OUTPUT pin, so it is similar like LED.
# from gpiozero import LED
# Check link https://www.raspberrypi.org/documentation/usage/gpio/ to get the PIN

DISPENSE_PIN = 17
BUTTON_FONT = ("Arial", 26,)
NORMAL_FONT = ("Calibri", 20)

BOLD_FONT = ("Calibri", 20, "bold")
SMALL_FONT = ("Calibri", 12)

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        def key_in(self):
            if self.keysym == 'Escape':
                app.destroy()
                print("Esc key pressed")
        # self.config(cursor="none")
        # self.overrideredirect(1)
        self.title("Ice Machine")
        self.geometry("800x480")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=2)
        container.grid_columnconfigure(0, weight=2)
        self.x = 5
        self.frames = {}
        self.roomID = ""
        self.roomCode = ""
        self.roomIDStatus = False
        self.roomCodeStatus = False
        self.isDispenseRun = False
        self.dispenseTimer = Timer(5, self.outputOff)
        # self.pinout = LED(DISPENSE_PIN)
        for F in (StartPage, PageOne, PageOK, PageError):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)
        container.bind_all('<Key>', key_in)
        self.outputOff()

    # def dispense_hold(self):
    #     self.isDispenseRun = True
    #     print("Dispense Button Hold")
    #     self.pinout.off()
    #     self.dispenseTimer = Timer(30, self.dispense_release)
    #     self.dispenseTimer.start()

    # def dispense_release(self):
    #     if self.isDispenseRun:
    #         self.dispenseTimer.cancel()
    #         self.pinout.on()
    #         print("Dispense Button Released")
    #         self.isDispenseRun = False
    #         self.done()

    def done(self):
        self.roomID = ""
        self.show_frame(StartPage)
        self.outputOff()

    def verify_code(self):
        if self.roomID != "" and self.roomIDStatus == True:
            self.show_frame(PageOne)

    def verify_code1(self):
        if self.roomIDStatus == True & self.roomCodeStatus == True:
            expectedCode = (int(self.roomID) * 2) + 29
            if expectedCode == int(self.roomCode):
                self.show_frame(PageOK)
                self.outputOn()
                self.x = 5
                self.counter()
            else:
                self.show_frame(PageError)
        self.roomCodeStatus = False

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.handler()
        frame.tkraise()

    def set_roomId(self, roomID):
        self.roomID = roomID
        self.roomIDStatus = True

    def get_roomId(self):
        return self.roomID

    def get_roomIDStatus(self):
        return self.roomIDStatus

    def set_roomCode(self, roomCode):
        self.roomCode = roomCode
        self.roomCodeStatus = True

    def get_roomCode(self):
        return self.roomCode

    def get_roomCodeStatus(self):
        return self.roomCodeStatus

    def outputOn(self):
        # self.pinout.off()
        self.dispenseTimer = Timer(5, self.outputOff)
        self.dispenseTimer.start()
        print("on")

    def outputOff(self):
        # self.pinout.on()
        self.dispenseTimer.cancel()
        print("off")

    def counter(self):
        if self.dispenseTimer.isAlive():
            self.x -= 1

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self._controller = controller
        controller.outputOff()
        self.configure(bg="white")
        label_001 = tk.Label(self, text="Hello and thank you for purchasing", font=NORMAL_FONT, bg="white", fg="#1482bf")
        label_001.place(x=-389, y=135, width=1200, height=30)
        label_002 = tk.Label(self, text="the premium ice and water available", font=NORMAL_FONT, bg="white", fg="#1482bf")
        label_002.place(x=-380, y=165, width=1200, height=30)
        label_003 = tk.Label(self, text="from this station.", font=NORMAL_FONT, bg="white", fg="#1482bf")
        label_003.place(x=-484, y=195, width=1200, height=30)
        label_004 = tk.Label(self, text="To get started, enter your room", font=BOLD_FONT, bg="white", fg="#1482bf")
        label_004.place(x=-402, y=250, width=1200, height=30)
        label_005 = tk.Label(self, text="number on the keypad to the right.", font=BOLD_FONT, bg="white", fg="#1482bf")
        label_005.place(x=-385, y=280, width=1200, height=30)
        self.textEntryVar = StringVar()
        label_roomNumber = Entry(self, width=10, bg='white', textvariable=self.textEntryVar, justify=CENTER, font=('-weight bold', 28))
        label_roomNumber.place(x=50, y=335, width=300, height=50)
        self._imgice = tk.PhotoImage(file="ice.png")
        ice = Button(self, width=402, bg="white", borderwidth="0", image=self._imgice, relief='flat')
        ice.place(x=20, y=5, width=412, height=125)
        self._imghotel = tk.PhotoImage(file="hotel.png")
        hotel = Button(self, width=402, bg="white", borderwidth="0", image=self._imghotel, relief='flat')
        hotel.place(x=20, y=410, width=196, height=52)
        self.createWidgets(x=160, y=160, w=240, h=240)

    def handler(self):
        self.textEntryVar.set("")
        print("Initialize System")

    def createWidgets(self,x,y,w,h):
        btn_list = ['1',  '4',  '7',  'CANCEL',  '2',  '5',  '8',  '0',  '3',  '6', '9', 'ENTER']
        self._imgb = tk.PhotoImage(file="button.png")
        self._imgc = tk.PhotoImage(file="cancel.png")
        self._imge = tk.PhotoImage(file="enter.png")
        y=35
        x=340
        r = 1
        c = 0
        n = 0
        btn = []
        for label in btn_list:
            cmd = lambda x = label: self.click(x)
            if label == 'CANCEL':
                cur = Button(self, text=label, width=200, command=cmd, activebackground="white", bg="white", borderwidth="0", image=self._imgc, relief='flat')
            elif label == 'ENTER':
                cur = tk.Button(self, text=label, command=lambda: self._controller.verify_code(), activebackground="white", bg="white", borderwidth="0", image=self._imge, relief='flat')
            else:
                cur = Button(self, text=label, width=200, command=cmd, compound="center", font=BUTTON_FONT, fg='#74a6d6', activeforeground='#74a6d6', bg="white", activebackground="white", borderwidth="0", image=self._imgb, relief='flat')
            cur.place(x=x + 110*r, y=y + 110*c, width=90, height=90)
            btn.append(cur)
            n += 1
            c += 1
            if c == 4:
                c = 0
                r += 1

    def click(self, label):
        if label == 'CANCEL':
            self.textEntryVar.set("")
        # elif label == 'DEL':
        #     currentText = self.textEntryVar.get()
        #     self.textEntryVar.set(currentText[:-1])
        else:
            currentText = self.textEntryVar.get()
            self.textEntryVar.set(currentText+label)
        self._controller.set_roomId(self.textEntryVar.get())

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self._controller = controller
        self.configure(bg="white")
        self.roomChar = StringVar()
        # label_001 = tk.Label(self, textvariable=self.roomChar, font=NORMAL_FONT, bg="white", fg="#1482bf")
        label_002 = tk.Label(self, text="Now enter your authorization code.", font=BOLD_FONT, bg="white", fg="#1482bf")
        label_002.place(x=-381, y=135, width=1200, height=30)
        label_003 = tk.Label(self, text="This is the number given to you at the", font=NORMAL_FONT, bg="white", fg="#1482bf")
        label_003.place(x=-378, y=185, width=1200, height=30)
        label_004 = tk.Label(self, text="front desk upon check in.", font=NORMAL_FONT, bg="white", fg="#1482bf")
        label_004.place(x=-445, y=215, width=1200, height=30)
        label_005 = tk.Label(self, text="If you do not yet have an authorization code, one may be", font=SMALL_FONT, bg="white", fg="#1482bf")
        label_005.place(x=-393, y=265, width=1200, height=18)
        label_006 = tk.Label(self, text="purchased at any time during your stay.", font=SMALL_FONT, bg="white", fg="#1482bf")
        label_006.place(x=-450, y=285, width=1200, height=18)
        self.textEntryVar = StringVar()
        label_roomNumber = Entry(self, width=10, bg='white', textvariable=self.textEntryVar, justify=CENTER, font=('-weight bold', 28))
        label_roomNumber.place(x=50, y=335, width=300, height=50)
        self._imgice = tk.PhotoImage(file="ice.png")
        ice = Button(self, width=402, bg="white", borderwidth="0", image=self._imgice, relief='flat')
        ice.place(x=20, y=5, width=412, height=125)
        self._imghotel = tk.PhotoImage(file="hotel.png")
        hotel = Button(self, width=402, bg="white", borderwidth="0", image=self._imghotel, relief='flat')
        hotel.place(x=20, y=410, width=196, height=52)
        self.createWidgets(x=160, y=160, w=240, h=240)

    def handler(self):
        self.textEntryVar.set("")
        self.roomChar.set("Room {0}".format(self._controller.get_roomId()))

    def createWidgets(self,x,y,w,h):
        btn_list = ['1',  '4',  '7',  'CANCEL',  '2',  '5',  '8',  '0',  '3',  '6', '9', 'ENTER']
        self._imgb = tk.PhotoImage(file="button.png")
        self._imgc = tk.PhotoImage(file="cancel.png")
        self._imge = tk.PhotoImage(file="enter.png")
        y=35
        x=340
        r = 1
        c = 0
        n = 0
        btn = []
        for label in btn_list:
            cmd = lambda x = label: self.click(x)
            if label == 'CANCEL':
                cur = Button(self, text=label, command=lambda: self._controller.done(), width=200, activebackground="white", bg="white", borderwidth="0", image=self._imgc, relief='flat')
            elif label == 'ENTER':
                cur = tk.Button(self, text=label, command=lambda: self._controller.verify_code1(), activebackground="white", bg="white", borderwidth="0", image=self._imge, relief='flat')
            else:
                cur = Button(self, text=label, width=200, command=cmd, compound="center", font=BUTTON_FONT, fg='#74a6d6', activeforeground='#74a6d6', bg="white", activebackground="white", borderwidth="0", image=self._imgb, relief='flat')
            cur.place(x=x + 110*r, y=y + 110*c, width=90, height=90)
            btn.append(cur)
            n += 1
            c += 1
            if c == 4:
                c = 0
                r += 1

    def click(self, label):
        currentText = self.textEntryVar.get()
        self.textEntryVar.set(currentText+label)
        self._controller.set_roomCode(self.textEntryVar.get())

class PageOK(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self._controller = controller
        self.configure(bg="white")
        label_001 = tk.Label(self, text="Thank you!", font=NORMAL_FONT, bg="white")
        label_001.place(x=-200, y=85, width=1200, heigh=30)
        label_002 = tk.Label(self, text="Please insert container", font=NORMAL_FONT, bg="white")
        label_002.place(x=-200, y=155, width=1200, heigh=30)
        label_003 = tk.Label(self, text="Time Remaining: " + str(controller.dispenseTimer), font=NORMAL_FONT, bg="white")
        label_003.place(x=-200, y=185, width=1200, heigh=30)
        # button_dispense = tk.Button(self, text="DISPENSE", font=BUTTON_FONT, bg="green", fg="white")
        # button_dispense.bind("<ButtonPress-1>", lambda event: controller.dispense_hold())
        # button_dispense.bind("<ButtonRelease-1>", lambda event: controller.dispense_release())
        # button_dispense.place(x=425, y=270, width=300, height=120)
        # label_003 = tk.Label(self, text="Press Cancel to return.", font=NORMAL_FONT)
        # label_003.place(x=0, y=360, width=1200, heigh=40)
        self._imgc = tk.PhotoImage(file="cancel.png")
        button_cancel = tk.Button(self, command=lambda: controller.done(), activebackground="white", bg="white", borderwidth="0", image=self._imgc, relief='flat')
        button_cancel.place(x=250, y=270, width=300, height=120)

    def handler(self):
        print("Successful to verify CODE")

class PageError(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="white")
        label_001 = tk.Label(self, text="Sorry, that code is invalid.", font=NORMAL_FONT, bg="white")
        label_001.place(x=-200, y=85, width=1200, heigh=30)
        label_002 = tk.Label(self, text="Please try again or contact", font=NORMAL_FONT, bg="white")
        label_002.place(x=-200, y=155, width=1200, heigh=30)
        label_003 = tk.Label(self, text="the front desk for assistance", font=NORMAL_FONT, bg="white")
        label_003.place(x=-200, y=185, width=1200, heigh=30)
        self._imgc = tk.PhotoImage(file="cancel.png")
        button_cancel = tk.Button(self, command=lambda: controller.done(), activebackground="white", bg="white", borderwidth="0", image=self._imgc, relief='flat')
        button_cancel.place(x=250, y=270, width=300, height=120)

    def handler(self):
        print("Failure to verify CODE")

if __name__ == '__main__':
    app = MainApp()
    app.mainloop()