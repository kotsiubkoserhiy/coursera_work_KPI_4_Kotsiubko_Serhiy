from tkinter import Toplevel, Button, Listbox, END, BOTH, YES
from tkinter import messagebox

class EmployeeList:
    def __init__(self, root, db_connection):
        self.root = root
        self.db_connection = db_connection

    def show_employee_list(self):
        employee_list_window = Toplevel(self.root)
        employee_list_window.title("Employee List")
        employee_list_window.geometry("600x600")

        # ListBox to display employees
        self.employee_listbox = Listbox(employee_list_window, font=("times new roman", 15), bg="lightyellow", fg="black")
        self.employee_listbox.pack(fill=BOTH, expand=YES, padx=5, pady=5)

        # Button to show employee salaries
        show_salaries_button = Button(employee_list_window, text="Show Salaries", font=("Arial", 15, "bold"), bg="blue", fg="gray",
                                      command=self.show_salaries)
        show_salaries_button.pack(pady=10)

        # Initialize with all employees
        self.populate_employee_list()

    def populate_employee_list(self, employees=None):
        self.employee_listbox.delete(0, END)
        if employees is None:
            cursor = self.db_connection.cursor()
            try:
                cursor.execute("SELECT * FROM employees")
                employees = cursor.fetchall()
            except Exception as e:
                messagebox.showerror("Error", f"Error fetching employees: {str(e)}")
            finally:
                cursor.close()

        for emp in employees:
            employee_info = f"ID: {emp[0]}, Name: {emp[1]}, Email: {emp[2]}, Phone: {emp[3]}, Position: {emp[4]}, Department: {emp[5]}"
            self.employee_listbox.insert(END, employee_info)

    def show_salaries(self):
        # Get selected employee
        selected_index = self.employee_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Selection", "Please select an employee.")
            return

        selected_employee = self.employee_listbox.get(selected_index[0])
        employee_id = selected_employee.split(",")[0].split(": ")[1]

        salary_window = Toplevel(self.root)
        salary_window.title("Employee Salaries")
        salary_window.geometry("500x400")

        salary_listbox = Listbox(salary_window, font=("times new roman", 15), bg="lightblue", fg="black")
        salary_listbox.pack(fill=BOTH, expand=YES, padx=5, pady=5)

        self.populate_salary_list(employee_id, salary_listbox)

    def populate_salary_list(self, employee_id, salary_listbox):
        salary_listbox.delete(0, END)
        cursor = self.db_connection.cursor()
        try:
            query = """SELECT month, year, total_working_days, sick_leave, absences, gross_salary, net_salary
                       FROM salaries WHERE employee_id = %s"""
            cursor.execute(query, (employee_id,))
            salaries = cursor.fetchall()
            if not salaries:
                salary_listbox.insert(END, "No salary data available for this employee.")
            else:
                for sal in salaries:
                    salary_listbox.insert(END, f"Month: {sal[0]}, Year: {sal[1]}, Working Days: {sal[2]}, Sick Leave: {sal[3]}, "
                                                f"Absences: {sal[4]}, Gross Salary: {sal[5]}, Net Salary: {sal[6]}")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching salaries: {str(e)}")
        finally:
            cursor.close()
