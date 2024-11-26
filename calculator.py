from tkinter import Toplevel, Frame, Entry, Button, StringVar

class Calculator:
    def __init__(self, master):
        self.master = master
        self.calc_window = None

    def show_calculator(self):
        if self.calc_window is None or not self.calc_window.winfo_exists():
            self.calc_window = Toplevel(self.master)  # Створення нового вікна
            self.calc_window.title("Calculator")
            self.calc_window.geometry("502x255")
            self.frame_calculator = Frame(self.calc_window, bd=3, relief='ridge', bg="white")
            self.frame_calculator.place(x=0, y=0, width=502, height=255)

            self.calc_input_text = StringVar()
            self.calc_input = Entry(self.frame_calculator, font=("Arial", 20), textvariable=self.calc_input_text,
                                    width=40, bd=5, relief='groove')
            self.calc_input.grid(row=0, column=0, columnspan=4, sticky="nsew")

            calc_buttons = [
                ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3),
                ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
                ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('*', 3, 3),
                ('C', 4, 0), ('0', 4, 1), ('.', 4, 2), ('/', 4, 3),
                ('=', 5, 0, 4)
            ]

            for button in calc_buttons:
                if len(button) == 4:
                    text, row, col, colspan = button
                    Button(self.frame_calculator, text=text, font=("Arial", 17), width=4, height=2,
                           command=lambda t=text: self.on_calc_button_click(t)).grid(row=row, column=col,
                                                                                     columnspan=colspan, sticky="nsew")
                else:
                    text, row, col = button
                    Button(self.frame_calculator, text=text, font=("Arial", 17), width=4, height=2,
                           command=lambda t=text: self.on_calc_button_click(t)).grid(row=row, column=col, sticky="nsew")

            # Налаштування автоматичного розширення кнопок
            for i in range(6):
                self.frame_calculator.grid_rowconfigure(i, weight=1)
            for j in range(4):
                self.frame_calculator.grid_columnconfigure(j, weight=1)

    def on_calc_button_click(self, char):
        current_text = self.calc_input_text.get()

        if char == "=":
            try:
                self.calc_input_text.set(eval(current_text))
            except Exception as e:
                self.calc_input_text.set("ERROR")
        elif char == "C":
            self.calc_input_text.set("")
        elif char == ".":
            if not current_text or current_text[-1] in "+-*/":
                self.calc_input_text.set(current_text + "0.")
            elif "." not in current_text.split()[-1]:
                self.calc_input_text.set(current_text + ".")
        else:
            self.calc_input_text.set(current_text + char)
