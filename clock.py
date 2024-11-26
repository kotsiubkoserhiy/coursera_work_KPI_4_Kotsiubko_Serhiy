import time
from tkinter import Frame, Canvas

class Clock:
    def __init__(self, clock_frame):
        self.clock_canvas = Canvas(clock_frame, bg="lightyellow", width=140, height=50)
        self.clock_canvas.pack(padx=5)
        self.update_clock()

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.clock_canvas.delete("all")
        self.clock_canvas.create_text(70, 25, text=now, font=("Arial", 20, "bold"), fill="gray")
        self.clock_canvas.after(1000, self.update_clock)