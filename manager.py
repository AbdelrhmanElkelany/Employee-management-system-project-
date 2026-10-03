import json
from models import employee_from_dict

class EmployeeManager:

    def __init__(self, file_path="data.json"):
        self.__file_path = file_path
        self.__employees = []
        self.__load_warning = ""
        self.__load_from_file()

    @property
    def load_warning(self):
        return self.__load_warning

    # ---------- Public interface ----------
    def add_employee(self, employee):
        """Add an employee. Raises ValueError for duplicate IDs, OSError if saving fails."""
        if self.__find_by_id(employee.employee_id) is not None:
            raise ValueError(f"An employee with ID '{employee.employee_id}' already exists.")
        self.__employees.append(employee)
        try:
            self.__save_to_file()
        except OSError:
            self.__employees.remove(employee)  # undo so memory matches the file
            raise

    def get_all_employees(self):
        """Return a copy of the list (the private list stays protected)."""
        return list(self.__employees)

    def search(self, keyword):
        """Return all employees whose ID, name, department or type contains keyword."""
        return [emp for emp in self.__employees if emp.matches(keyword)]

    def total_payroll(self):
        """Return the sum of every employee's monthly pay."""
        return sum(emp.calculate_salary() for emp in self.__employees)

    # ---------- Private helpers (hidden implementation details) ----------
    def __find_by_id(self, employee_id):
        for emp in self.__employees:
            if emp.employee_id.lower() == employee_id.lower():
                return emp
        return None

    def __save_to_file(self):
        data = [emp.to_dict() for emp in self.__employees]
        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def __load_from_file(self):
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                records = json.load(file)
        except FileNotFoundError:
            return  # first run: no data yet
        except (OSError, json.JSONDecodeError):
            self.__load_warning = "The data file could not be read. Starting with an empty list."
            return

        if not isinstance(records, list):
            self.__load_warning = "The data file has an unexpected format. Starting with an empty list."
            return

        skipped = 0
        for record in records:
            try:
                self.__employees.append(employee_from_dict(record))
            except (KeyError, TypeError, ValueError):
                skipped += 1
        if skipped:
            self.__load_warning = f"{skipped} invalid record(s) in the data file were skipped."