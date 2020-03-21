import tkinter as tk
import threading
import time
import sys

class CountdownWindow(tk.Frame):
    def __init__(self, parent, countdown):
        super(CountdownWindow, self).__init__(parent)
        self.parent = parent
        self.countdown = tk.IntVar()
        self.countdown.set(countdown)
        coords = sys.stdin.readline().split(' ')

        self.grid(row=0, column=0, padx=20, pady=20, sticky=tk.NSEW)

        self.countdownLabel = tk.Label(self, text='До начала работы:', anchor=tk.E)
        self.countdownValue = tk.Label(self, textvariable=self.countdown)

        self.countdownLabel.grid(row=0, column=0, sticky=tk.W)
        self.countdownValue.grid(row=0, column=1, sticky=tk.E)

        #self.place(x=(int(coords[0]) * 2 - 60), y=(int(coords[1]) * 2 - 60))

        self.parent.wm_attributes('-topmost', 1)
        self.thread = threading.Thread(target=self.countdownProcess, daemon=True)
        self.thread.start()

    def countdownProcess(self):
        while self.countdown.get() > 0:
            print(self.countdown.get())
            time.sleep(1)
            self.countdown.set(self.countdown.get() - 1)
        self.parent.destroy()

if __name__ == '__main__':
    CountdownWindow(tk.Tk(), 30).mainloop()