
from threading import Thread
from tkinter import Label
from tkinter import Tk
from tkinter.font import Font

class Splash(Thread):
    def __init__(self, text, author, factor=0.4):
        Thread.__init__(self)
        self.setName("Splash")
        self.setDaemon(True)
        self.text = text
        self.author = author
        self.factor = factor
        self.screen = None

    def run(self):
        self.screen = Tk()
        spfont = Font(family="System", size=30)
        Label(self.screen, text=self.text, font=spfont).pack()
        Label(self.screen, text=self.author, font=spfont).pack()
        
        screen_w = self.screen.winfo_screenwidth()
        screen_h = self.screen.winfo_screenheight()
        w, h = screen_w * self.factor, screen_h * self.factor
        x, y = (screen_w/2) - (w/2), (screen_h/2) - (h/2)
        self.screen.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.screen.overrideredirect(True)
        self.screen.mainloop()

    show = Thread.start  # Alias

    def hide(self):
        if self.screen:
            self.screen.quit()

    def __enter__(self):
        self.show()

    def __exit__(self, *_):
        self.hide()
