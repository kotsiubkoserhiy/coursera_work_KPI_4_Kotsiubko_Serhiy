import re

def validate_employee_id(emp_id):
    # Checking that the ID consists of only numbers
    return emp_id.isdigit() and len(emp_id) > 0

def validate_name(name):
    # Allows Ukrainian, English letters and spaces
    return bool(re.match(r"^[A-Za-zА-Яа-яЇїІіЄєҐґ\s]+$", name))

def validate_email(email):
    # email check
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))

def validate_phone(phone):
    # number consists of numbers and can start with plus, from 10 to 15 characters
    return bool(re.match(r"^\+?\d{10,15}$", phone))

def validate_position(position):
    # Allows Ukrainian and English letters, spaces and some symbols (dot, comma, hyphen)
    return bool(re.match(r"^[A-Za-zА-Яа-яЇїІіЄєҐґ\s\.,-]+$", position))

def validate_department(department):
    # Check for a non-empty value, with Ukrainian and English letters
    return bool(re.match(r"^[A-Za-zА-Яа-яЇїІіЄєҐґ\s]+$", department))

def validate_salary(salary):
    try:
        return float(salary) > 0
    except ValueError:
        return False

def validate_month(month):
    return month.isdigit() and 1 <= int(month) <= 12

def validate_year(year):
    return year.isdigit() and 1900 <= int(year) <= 2100

def validate_working_days(days):
    try:
        days = int(days)
        return days > 0
    except ValueError:
        return False

def validate_leave_days(leave_days):
    try:
        leave_days = int(leave_days)
        return leave_days >= 0
    except ValueError:
        return False