from tkinter import StringVar
from tkinter import Text, Label, Entry, Button
class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.theme = StringVar()
        self.theme.set("light")  # Initial theme

    def toggle_theme(self):
        theme = self.theme.get()
        self.theme.set("dark" if theme == "light" else "light")
        self.apply_theme()

    def apply_theme(self):
        theme = self.theme.get()
        bg_color = "white" if theme == "light" else "black"
        fg_color = "black" if theme == "light" else "white"
        widget_bg = "lightyellow" if theme == "light" else "gray"
        widget_fg = "black" if theme == "light" else "white"

        self.root.config(bg=bg_color)

        for frame in self.root.winfo_children():
            frame.config(bg=bg_color)

        for widget in self.root.winfo_children():
            if isinstance(widget, (Label, Entry, Button, Text)):
                widget.config(bg=widget_bg, fg=widget_fg)
