import mysql.connector
from tkinter import messagebox

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1",
            database="employee_payroll"
        )
        if conn.is_connected():
            return conn
    except Exception as e:
        messagebox.showerror("Error", f"Error connecting to MySQL database: {str(e)}")
        return None

