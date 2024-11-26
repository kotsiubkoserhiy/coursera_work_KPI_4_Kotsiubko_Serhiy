from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
import mysql.connector
from database import connect_to_db
from calculator import Calculator
from calendar_window import CalendarWindow
from theme_manager import ThemeManager
from clock import Clock
from employee_list import EmployeeList
from tkinter import Listbox, Scrollbar, ttk
from validators import *
import locale


class EmployeeSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Payroll System")
        # Set minimum window size
        self.root.minsize(1200, 800)
        self.root.config(bg="white")

        # Configure grid weight for root window
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.db_connection = connect_to_db()
        if not self.db_connection:
            messagebox.showerror("Database Error", "Failed to connect to database. Exiting.")
            root.destroy()
            return

        self.theme_manager = ThemeManager(self.root)

        # Create main container
        self.main_container = Frame(self.root, bg="white")
        self.main_container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Header Frame
        self.header_frame = Frame(self.root, bg="lightyellow")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=1)  # Make the title expand

        # Title
        title = Label(self.header_frame, text="Employee Payroll  System",
                      font=("times new roman", 25, "bold"),
                      bg="lightyellow", fg="gray")
        title.grid(row=0, column=0, pady=10, padx=15, sticky="w")

        # Clock Frame
        self.clock_frame = Frame(self.header_frame, bg="lightyellow")
        self.clock_frame.grid(row=0, column=2, padx=10, pady=5, sticky="e")

        # Buttons in header
        buttons_frame = Frame(self.header_frame)
        buttons_frame.grid(row=0, column=1, sticky="e", padx=5)

        # Header buttons with consistent styling
        button_style = {"font": ("Arial", 15, "bold"), "bg": "lightyellow", "fg": "gray", "padx": 10}

        Button(buttons_frame, text="Employee List",
               command=self.show_employee_list, **button_style).pack(side=LEFT, padx=5)
        Button(buttons_frame, text="Calculator",
               command=self.show_calculator, **button_style).pack(side=LEFT, padx=5)
        Button(buttons_frame, text="Calendar",
               command=self.open_calendar, **button_style).pack(side=LEFT, padx=5)
        Button(buttons_frame, text="Toggle Theme",
               command=self.theme_manager.toggle_theme, **button_style).pack(side=LEFT, padx=5)

        # Left Panel (Employee Details + Event List)
        self.left_panel = Frame(self.main_container, bg="white")
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=5)
        self.left_panel.grid_rowconfigure(1, weight=1)
        self.left_panel.grid_columnconfigure(0, weight=1)

        # Employee Details Frame
        self.create_employee_details_frame()

        # Event List Frame
        self.create_event_list_frame()

        # Right Panel (Salary Details + Receipt)
        self.right_panel = Frame(self.main_container, bg="white")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=5)
        self.right_panel.grid_rowconfigure(1, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)

        # Salary Details Frame
        self.create_salary_details_frame()

        # Salary Receipt Frame
        self.create_salary_receipt_frame()

        # Initialize components
        self.initialize_components()

        locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')


    def create_employee_details_frame(self):
        self.Frame1 = ttk.LabelFrame(self.left_panel, text="Employee Details", padding="10")
        self.Frame1.grid(row=0, column=0, sticky="nsew", pady=5)
        self.Frame1.grid_columnconfigure(1, weight=1)

        # Employee fields
        labels = ["Employee ID", "Name", "Email", "Phone", "Position", "Department", "Salary"]
        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(self.Frame1, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            self.entries[label] = ttk.Entry(self.Frame1)
            self.entries[label].grid(row=i, column=1, padx=5, pady=5, sticky="ew")

            if label == "Employee ID":
                search_btn = ttk.Button(self.Frame1, text="Search", command=self.search_employee)
                search_btn.grid(row=i, column=2, padx=5, pady=5)

        # Buttons frame
        btn_frame = ttk.Frame(self.Frame1)
        btn_frame.grid(row=len(labels), column=0, columnspan=3, pady=10)

        ttk.Button(btn_frame, text="Add", command=self.add_employee).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_employee).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_employee).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_fields).pack(side=LEFT, padx=5)

    def create_event_list_frame(self):
        self.event_list_frame = ttk.LabelFrame(self.left_panel, text="Upcoming Events", padding="10")
        self.event_list_frame.grid(row=1, column=0, sticky="nsew", pady=5)
        self.event_list_frame.grid_rowconfigure(0, weight=1)
        self.event_list_frame.grid_columnconfigure(0, weight=1)

        # Event listbox with scrollbar
        self.event_listbox = Listbox(self.event_list_frame, font=("Arial", 15),
                                     highlightbackground="lightyellow", highlightthickness=0, bd=0)
        self.event_listbox.grid(row=0, column=0, sticky="nsew")

        # Scrollbar configuration
        scrollbar = ttk.Scrollbar(self.event_list_frame, orient=VERTICAL, command=self.event_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.event_listbox.config(yscrollcommand=scrollbar.set)


    def create_salary_details_frame(self):
        self.Frame2 = ttk.LabelFrame(self.right_panel, text="Salary Details", padding="10")
        self.Frame2.grid(row=0, column=0, sticky="nsew", pady=5)
        self.Frame2.grid_columnconfigure(1, weight=1)

        # Salary fields
        labels = ["Employee ID", "Month", "Year", "Total Working Days", "Sick Leave", "Absences"]
        self.salary_entries = {}

        for i, label in enumerate(labels):
            ttk.Label(self.Frame2, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            self.salary_entries[label] = ttk.Entry(self.Frame2)
            self.salary_entries[label].grid(row=i, column=1, padx=5, pady=5, sticky="ew")

        # Buttons frame
        btn_frame = ttk.Frame(self.Frame2)
        btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Save Salary", command=self.add_salary).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Salary", command=self.update_salary).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Generate Receipt", command=self.generate_salary_slip).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_salary_fields).pack(side=LEFT, padx=5)

    def create_salary_receipt_frame(self):
        self.Frame3 = ttk.LabelFrame(self.right_panel, text="Salary Receipt", padding="10")
        self.Frame3.grid(row=1, column=0, sticky="nsew", pady=5)
        self.Frame3.grid_rowconfigure(0, weight=1)
        self.Frame3.grid_columnconfigure(0, weight=1)

        # Receipt text area with scrollbar
        self.salary_receipt_text = Text(self.Frame3, font=("Arial", 15))
        self.salary_receipt_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.Frame3, orient=VERTICAL, command=self.salary_receipt_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.salary_receipt_text.config(yscrollcommand=scrollbar.set)

        # Save button
        ttk.Button(self.Frame3, text="Save Details", command=self.save_receipt).grid(row=1, column=0, pady=5)

    def initialize_components(self):
        # Initialize other components
        self.calculator = Calculator(self.root)
        self.employee_list = EmployeeList(self.root, self.db_connection)
        self.clock = Clock(self.clock_frame)
        self.calendar_window = None


        # Fetch initial events
        self.fetch_upcoming_events()

    def show_calculator(self):
        self.calculator.show_calculator()

    def show_employee_list(self):
        self.employee_list.show_employee_list()

    def open_calendar(self):
        self.calendar_window = CalendarWindow(self.root, self.db_connection)
        self.fetch_upcoming_events()
    def fetch_upcoming_events(self):
        try:
            cursor = self.db_connection.cursor()
            query = "SELECT event_date, event_name FROM events ORDER BY event_date LIMIT 15"
            cursor.execute(query)
            events = cursor.fetchall()
            cursor.close()

            self.event_listbox.delete(0, END)
            if events:
                for event in events:
                    event_date = event[0]
                    event_name = event[1]
                    self.event_listbox.insert(END, f"{event_date}: {event_name}")
            else:
                self.event_listbox.insert(END, "No upcoming events.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error retrieving events: {err}")

    def search_employee(self):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("SELECT * FROM employees WHERE id=%s", (self.entries["Employee ID"].get(),))
            employee_row = cursor.fetchone()
            if employee_row:
                self.clear_salary_fields()

                if len(employee_row) >= 7:
                    self.entries["Name"].delete(0, END)
                    self.entries["Email"].delete(0, END)
                    self.entries["Phone"].delete(0, END)
                    self.entries["Position"].delete(0, END)
                    self.entries["Department"].delete(0, END)
                    self.entries["Salary"].delete(0, END)

                    self.entries["Name"].insert(0, employee_row[1])
                    self.entries["Email"].insert(0, employee_row[2])
                    self.entries["Phone"].insert(0, employee_row[3])
                    self.entries["Position"].insert(0, employee_row[4])
                    self.entries["Department"].insert(0, employee_row[5])
                    self.entries["Salary"].insert(0, employee_row[6])

                    # last salary information
                    cursor.execute("""
                        SELECT * FROM salaries 
                        WHERE employee_id=%s 
                        ORDER BY year DESC, month DESC 
                        LIMIT 1
                    """, (self.entries["Employee ID"].get(),))

                    salary_row = cursor.fetchone()
                    if salary_row:
                        self.salary_entries["Employee ID"].delete(0, END)
                        self.salary_entries["Month"].delete(0, END)
                        self.salary_entries["Year"].delete(0, END)
                        self.salary_entries["Total Working Days"].delete(0, END)
                        self.salary_entries["Sick Leave"].delete(0, END)
                        self.salary_entries["Absences"].delete(0, END)

                        self.salary_entries["Employee ID"].insert(0, salary_row[1])
                        self.salary_entries["Month"].insert(0, salary_row[2])
                        self.salary_entries["Year"].insert(0, salary_row[3])
                        self.salary_entries["Total Working Days"].insert(0, salary_row[4])
                        self.salary_entries["Sick Leave"].insert(0, salary_row[5])
                        self.salary_entries["Absences"].insert(0, salary_row[6])
                    else:
                        messagebox.showinfo("Info", "No salary record found for this employee")
                else:
                    messagebox.showerror("Error", "Unexpected data format from the database.")
            else:
                messagebox.showinfo("Info", "No record found")
                self.clear_fields()
                self.clear_salary_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error searching employee: {str(e)}")
        finally:
            cursor.close()

    def add_employee(self):
        emp_id = self.entries["Employee ID"].get()
        name = self.entries["Name"].get()
        email = self.entries["Email"].get()
        phone = self.entries["Phone"].get()
        position = self.entries["Position"].get()
        department = self.entries["Department"].get()
        salary = self.entries["Salary"].get()

        # validation
        if not validate_employee_id(emp_id):
            messagebox.showerror("Error", "Invalid Employee ID")
            return
        if not validate_name(name):
            messagebox.showerror("Error", "Invalid Name")
            return
        if not validate_email(email):
            messagebox.showerror("Error", "Invalid Email")
            return
        if not validate_phone(phone):
            messagebox.showerror("Error", "Invalid Phone Number")
            return
        if not validate_position(position):
            messagebox.showerror("Error", "Position cannot be empty")
            return
        if not validate_department(department):
            messagebox.showerror("Error", "Department cannot be empty")
            return
        if not validate_salary(salary):
            messagebox.showerror("Error", "Invalid Salary")
            return

        cursor = self.db_connection.cursor()
        try:
            query = "INSERT INTO employees (id, name, email, phone, position, department, salary) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            data = (emp_id, name, email, phone, position, department, salary)
            cursor.execute(query, data)
            self.db_connection.commit()
            messagebox.showinfo("Success", "Employee added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding employee: {str(e)}")
        finally:
            cursor.close()

    def update_employee(self):
        emp_id = self.entries["Employee ID"].get()
        name = self.entries["Name"].get()
        email = self.entries["Email"].get()
        phone = self.entries["Phone"].get()
        position = self.entries["Position"].get()
        department = self.entries["Department"].get()
        salary = self.entries["Salary"].get()

        # validation
        if not validate_employee_id(emp_id):
            messagebox.showerror("Error", "Invalid Employee ID")
            return
        if not validate_name(name):
            messagebox.showerror("Error", "Invalid Name")
            return
        if not validate_email(email):
            messagebox.showerror("Error", "Invalid Email")
            return
        if not validate_phone(phone):
            messagebox.showerror("Error", "Invalid Phone Number")
            return
        if not validate_position(position):
            messagebox.showerror("Error", "Position cannot be empty")
            return
        if not validate_department(department):
            messagebox.showerror("Error", "Department cannot be empty")
            return
        if not validate_salary(salary):
            messagebox.showerror("Error", "Invalid Salary")
            return

        cursor = self.db_connection.cursor()
        try:
            query = "UPDATE employees SET name=%s, email=%s, phone=%s, position=%s, department=%s, salary=%s WHERE id=%s"
            data = (name, email, phone, position, department, salary, emp_id)
            cursor.execute(query, data)
            self.db_connection.commit()
            messagebox.showinfo("Success", "Employee updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating employee: {str(e)}")
        finally:
            cursor.close()

    def delete_employee(self):
        cursor = self.db_connection.cursor()
        try:
            employee_id = self.entries["Employee ID"].get()

            if not employee_id:
                messagebox.showwarning("Warning", "Please enter a valid Employee ID")
                return

            query1 = "DELETE FROM salaries WHERE employee_id = %s;"
            cursor.execute(query1, (employee_id,))

            query2 = "DELETE FROM employees WHERE id = %s;"
            cursor.execute(query2, (employee_id,))

            messagebox.showinfo("Success", "Employee and related records deleted successfully")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting employee: {str(e)}")
        finally:
            cursor.close()

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, END)

    def clear_salary_fields(self):
        for entry in self.salary_entries.values():
            entry.delete(0, END)

    def calculate_net_salary(self, gross_salary):
        if gross_salary <= 0:
            return 0
        # PDFO 18%
        pdfo = gross_salary * 0.18
        # Military tax 1.5%
        military_tax = gross_salary * 0.015
        net_salary = gross_salary - (pdfo + military_tax)
        return round(net_salary, 2)

    # salary based on worked days
    def calculate_gross_salary(self, total_days, sick_days, absent_days, daily_salary):
        worked_days = total_days - (sick_days + absent_days)
        return worked_days * daily_salary

    def generate_salary_slip(self):
        try:
            id = self.entries["Employee ID"].get()
            name = self.entries["Name"].get()
            total_working_days = int(self.salary_entries["Total Working Days"].get())
            sick_leave = int(self.salary_entries["Sick Leave"].get())
            absences = int(self.salary_entries["Absences"].get())

            cursor = self.db_connection.cursor()
            cursor.execute("SELECT salary FROM employees WHERE id=%s", (id,))
            employee_row = cursor.fetchone()

            if employee_row:
                daily_salary = float(employee_row[0]) / total_working_days  # Зарплата за день
                gross_salary = self.calculate_gross_salary(total_working_days, sick_leave, absences, daily_salary)
                # net salary calculation
                net_salary = self.calculate_net_salary(gross_salary)

                salary_slip = (
                    f"Salary Receipt\n"
                    f"Employee ID: {id}\n"
                    f"Employee Name: {name}\n"
                    f"Total Working Days: {total_working_days}\n"
                    f"Sick Leave: {sick_leave}\n"
                    f"Absences: {absences}\n"
                    f"Gross Salary: {gross_salary:.2f} грн\n"
                    f"Net Salary: {net_salary:.2f} грн\n"
                )

                self.salary_receipt_text.delete(1.0, END)
                self.salary_receipt_text.insert(END, salary_slip)
            else:
                messagebox.showinfo("Info", "No employee record found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating salary slip: {str(e)}")
        finally:
            cursor.close()

    def print_salary_receipt(self):
        self.salary_receipt_text.delete('1.0', END)
        self.salary_receipt_text.insert(END, f"Company Name: XYZ\nAddress: XYZ, Floor4\n")
        self.salary_receipt_text.insert(END, f"Employee ID: {self.entries['Employee ID'].get()}\n")
        self.salary_receipt_text.insert(END,
                                        f"Salary of: {self.salary_entries['Month'].get()}-{self.salary_entries['Year'].get()}\n")
        self.salary_receipt_text.insert(END,
                                        f"Generated on: {self.salary_entries['Month'].get()}-{self.salary_entries['Year'].get()}\n")
        self.salary_receipt_text.insert(END, f"Total Days: {self.total()}\n")

    def save_receipt(self):
        receipt_content = self.salary_receipt_text.get("1.0", "end-1c")
        if receipt_content:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                try:
                    with open(file_path, "w") as file:
                        file.write(receipt_content)
                    messagebox.showinfo("Saved", f"Salary receipt saved successfully to {os.path.abspath(file_path)}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error saving salary receipt: {str(e)}")
        else:
            messagebox.showwarning("Empty Receipt", "Cannot save an empty salary receipt.")

    def add_salary(self):
        try:
            employee_id = self.salary_entries["Employee ID"].get()
            month = self.salary_entries["Month"].get()
            year = self.salary_entries["Year"].get()
            total_working_days = self.salary_entries["Total Working Days"].get()
            sick_leave = self.salary_entries["Sick Leave"].get()
            absences = self.salary_entries["Absences"].get()

            if not all([employee_id, month, year, total_working_days, sick_leave, absences]):
                messagebox.showwarning("Warning", "Please fill in all fields.")
                return

            # validation
            if not validate_employee_id(employee_id):
                messagebox.showerror("Error", "Invalid Employee ID")
                return
            if not validate_month(month):
                messagebox.showerror("Error", "Invalid Month")
                return
            if not validate_year(year):
                messagebox.showerror("Error", "Invalid Year")
                return
            if not validate_working_days(total_working_days):
                messagebox.showerror("Error", "Total Working Days must be a positive number.")
                return
            if not validate_leave_days(sick_leave) or not validate_leave_days(absences):
                messagebox.showerror("Error", "Sick Leave and Absences must be non-negative numbers.")
                return

            cursor = self.db_connection.cursor()
            cursor.execute("SELECT salary FROM employees WHERE id=%s", (employee_id,))
            employee_row = cursor.fetchone()

            if employee_row:
                daily_salary = float(employee_row[0]) / int(total_working_days)

                gross_salary = self.calculate_gross_salary(
                    int(total_working_days), int(sick_leave), int(absences), daily_salary
                )
                net_salary = self.calculate_net_salary(gross_salary)

                check_query = """SELECT * FROM salaries WHERE employee_id = %s AND month = %s AND year = %s"""
                cursor.execute(check_query, (employee_id, month, year))
                result = cursor.fetchone()

                if result is None:
                    query = """
                        INSERT INTO salaries (employee_id, month, year, total_working_days, sick_leave, absences, gross_salary, net_salary)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (
                        employee_id, month, year, total_working_days, sick_leave, absences, gross_salary, net_salary
                    ))
                    self.db_connection.commit()

                    messagebox.showinfo("Success", "Salary details added successfully.")
                    self.clear_salary_fields()
                else:
                    messagebox.showwarning("Warning", "Salary record for this month already exists.")
            else:
                messagebox.showinfo("Info", "No employee record found.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error adding salary details: {err}")
        finally:
            cursor.close()

    def update_salary(self):
        try:
            employee_id = self.salary_entries["Employee ID"].get()
            month = self.salary_entries["Month"].get()
            year = self.salary_entries["Year"].get()
            total_working_days = self.salary_entries["Total Working Days"].get()
            sick_leave = self.salary_entries["Sick Leave"].get()
            absences = self.salary_entries["Absences"].get()

            if not all([employee_id, month, year, total_working_days, sick_leave, absences]):
                messagebox.showwarning("Warning", "Please fill in all fields.")
                return


            # validation
            if not validate_employee_id(employee_id):
                messagebox.showerror("Error", "Invalid Employee ID")
                return
            if not validate_month(month):
                messagebox.showerror("Error", "Invalid Month")
                return
            if not validate_year(year):
                messagebox.showerror("Error", "Invalid Year")
                return
            if not validate_working_days(total_working_days):
                messagebox.showerror("Error", "Total Working Days must be a positive number.")
                return
            if not validate_leave_days(sick_leave) or not validate_leave_days(absences):
                messagebox.showerror("Error", "Sick Leave and Absences must be non-negative numbers.")
                return

            cursor = self.db_connection.cursor()
            cursor.execute("SELECT salary FROM employees WHERE id=%s", (employee_id,))
            employee_row = cursor.fetchone()

            if employee_row:
                daily_salary = float(employee_row[0]) / int(total_working_days)

                # salary calculation
                gross_salary = self.calculate_gross_salary(
                    int(total_working_days), int(sick_leave), int(absences), daily_salary
                )
                net_salary = self.calculate_net_salary(gross_salary)

                query = """UPDATE salaries SET total_working_days=%s, sick_leave=%s, absences=%s, gross_salary=%s, net_salary=%s
                           WHERE employee_id=%s AND month=%s AND year=%s"""
                cursor.execute(query, (
                    int(total_working_days), int(sick_leave), int(absences), gross_salary, net_salary, employee_id,
                    month, year
                ))
                self.db_connection.commit()

                if cursor.rowcount == 0:
                    messagebox.showwarning("Warning", "No records found to update.")
                else:
                    messagebox.showinfo("Success", "Salary details updated successfully.")
                self.clear_salary_fields()

            else:
                messagebox.showinfo("Info", "No employee record found.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error updating salary details: {err}")
        finally:
            cursor.close()

