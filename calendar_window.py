from datetime import datetime
from tkinter import Toplevel, Frame, Label, Entry, Button, messagebox, END
from tkcalendar import Calendar
import mysql.connector

def parse_date(date_str):
    formats = ["%d.%m.%y", "%d/%m/%Y", "%Y-%m-%d"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {date_str}")

class CalendarWindow:
    def __init__(self, parent, db_connection):
        self.parent = parent
        self.db_connection = db_connection

        self.calendar_window = Toplevel(parent)
        self.calendar_window.title("Calendar")
        self.calendar_window.geometry("400x400")

        self.calendar_frame = Frame(self.calendar_window, bg="white")
        self.calendar_frame.pack(fill="both", expand=True)

        # Get today's date in SQL format
        today = datetime.today()
        self.calendar = Calendar(self.calendar_frame, selectmode="day", year=today.year, month=today.month, day=today.day, showweeknumbers=False, date_pattern="dd.mm.yy")
        self.calendar.pack(fill="both", expand=True)
        self.calendar.bind("<<CalendarSelected>>", self.show_selected_date)

        self.selected_date_label = Label(self.calendar_window, text="", font=("Arial", 15))
        self.selected_date_label.pack(pady=10)

        self.event_name_entry = Entry(self.calendar_window, font=("Arial", 12))
        self.event_name_entry.pack(pady=5)

        save_event_btn = Button(
            self.calendar_window, text="Save Event", font=("Arial", 12), command=self.save_event
        )
        save_event_btn.pack(pady=5)

        delete_event_btn = Button(
            self.calendar_window, text="Delete Event", font=("Arial", 12), command=self.delete_event
        )
        delete_event_btn.pack(pady=5)

    def show_selected_date(self, event=None):
        selected_date = self.calendar.get_date()
        self.selected_date_label.config(text=f"Selected Date: {selected_date}")
        self.display_events(selected_date)

    def save_event(self):
        selected_date = self.calendar.get_date()
        event_name = self.event_name_entry.get()

        if selected_date and event_name:
            try:
                # parse date
                formatted_date = parse_date(selected_date)
                formatted_date_sql = formatted_date.strftime("%Y-%m-%d")

                cursor = self.db_connection.cursor()
                query = "INSERT INTO events (event_date, event_name) VALUES (%s, %s)"
                data = (formatted_date_sql, event_name)
                cursor.execute(query, data)
                self.db_connection.commit()
                cursor.close()
                messagebox.showinfo("Event Saved", f"Event '{event_name}' saved for {formatted_date_sql}")
                self.event_name_entry.delete(0, END)
                self.display_events(formatted_date_sql)
            except ValueError as ve:
                messagebox.showerror("Error", f"Invalid date format: {ve}")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error saving event: {err}")
        else:
            messagebox.showerror("Error", "Please select a date and enter event name.")

    def delete_event(self):
        selected_date = self.calendar.get_date()
        event_name = self.event_name_entry.get()

        if selected_date and event_name:
            try:
                formatted_date = parse_date(selected_date).strftime("%Y-%m-%d")
                cursor = self.db_connection.cursor()
                query = "DELETE FROM events WHERE event_date = %s AND event_name = %s"
                data = (formatted_date, event_name)
                cursor.execute(query, data)
                self.db_connection.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Event Deleted", f"Event '{event_name}' deleted for {formatted_date}")
                    self.event_name_entry.delete(0, END)
                    self.display_events(formatted_date)
                else:
                    messagebox.showerror("Error", f"Event '{event_name}' not found for {formatted_date}")
                cursor.close()
            except ValueError as ve:
                messagebox.showerror("Error", f"Invalid date format: {ve}")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error deleting event: {err}")
        else:
            messagebox.showerror("Error", "Please select a date and enter event name.")

    def display_events(self, selected_date):
        try:
            formatted_date = parse_date(selected_date).strftime("%Y-%m-%d")
            cursor = self.db_connection.cursor()
            query = "SELECT event_name FROM events WHERE event_date = %s"
            cursor.execute(query, (formatted_date,))
            events = cursor.fetchall()
            cursor.close()

            if events:
                event_list_text = "\n".join(event[0] for event in events)
            else:
                event_list_text = "No events for this date."

            messagebox.showinfo("Events for Selected Date", f"Events for {formatted_date}:\n{event_list_text}")
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid date format: {ve}")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error retrieving events: {err}")

    def __del__(self):
        if self.calendar_window:
            self.calendar_window.destroy()
