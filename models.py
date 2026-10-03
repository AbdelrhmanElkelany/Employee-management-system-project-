import math
from abc import ABC, abstractmethod


def clean_text(value, field_name):
    """Return the text without extra spaces, or raise ValueError if empty."""
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field_name} cannot be empty.")
    return text


def clean_number(value, field_name):
    """Return value as a float, or raise ValueError if it is not a valid number >= 0."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a number.") from None
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"{field_name} must be a valid number that is 0 or greater.")
    return number


class Employee(ABC):
    """Abstract parent class: data and behavior shared by all employees."""

    def __init__(self, employee_id, name, department):
        # Encapsulation: private attributes, validated when created.
        self.__employee_id = clean_text(employee_id, "Employee ID")
        self.__name = clean_text(name, "Name")
        self.__department = clean_text(department, "Department")

    # ---------- Encapsulation: controlled access ----------
    @property
    def employee_id(self):
        return self.__employee_id  # read-only: no setter on purpose

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = clean_text(value, "Name")

    @property
    def department(self):
        return self.__department

    @department.setter
    def department(self, value):
        self.__department = clean_text(value, "Department")

    # ---------- Abstraction: every subclass MUST implement these ----------
    @abstractmethod
    def calculate_salary(self):
        """Return the employee's monthly pay."""

    @abstractmethod
    def get_employee_type(self):
        """Return the employee type as text."""

    @abstractmethod
    def get_details(self):
        """Return a short text describing how this employee is paid."""

    # ---------- Shared behavior (inherited by all subclasses) ----------
    def to_dict(self):
        """Convert the object to a dictionary so it can be saved as JSON."""
        return {
            "type": self.get_employee_type(),
            "employee_id": self.__employee_id,
            "name": self.__name,
            "department": self.__department,
        }

    def matches(self, keyword):
        """Return True if keyword appears in the ID, name, department or type."""
        keyword = keyword.strip().lower()
        fields = (self.employee_id, self.name, self.department, self.get_employee_type())
        return any(keyword in field.lower() for field in fields)

    def __str__(self):
        return f"{self.employee_id} - {self.name} ({self.get_employee_type()})"


class FullTimeEmployee(Employee):
    """Employee paid a fixed monthly salary."""

    def __init__(self, employee_id, name, department, monthly_salary):
        super().__init__(employee_id, name, department)
        self.__monthly_salary = clean_number(monthly_salary, "Monthly salary")

    @property
    def monthly_salary(self):
        return self.__monthly_salary

    @monthly_salary.setter
    def monthly_salary(self, value):
        self.__monthly_salary = clean_number(value, "Monthly salary")

    # Polymorphism: overriding the abstract methods
    def calculate_salary(self):
        return self.__monthly_salary

    def get_employee_type(self):
        return "Full-Time"

    def get_details(self):
        return f"Monthly salary: {self.__monthly_salary:,.2f}"

    def to_dict(self):
        data = super().to_dict()
        data["monthly_salary"] = self.__monthly_salary
        return data


class PartTimeEmployee(Employee):
    """Employee paid per hour worked."""

    def __init__(self, employee_id, name, department, hourly_rate, hours_worked):
        super().__init__(employee_id, name, department)
        self.__hourly_rate = clean_number(hourly_rate, "Hourly rate")
        self.__hours_worked = clean_number(hours_worked, "Hours worked")

    @property
    def hourly_rate(self):
        return self.__hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, value):
        self.__hourly_rate = clean_number(value, "Hourly rate")

    @property
    def hours_worked(self):
        return self.__hours_worked

    @hours_worked.setter
    def hours_worked(self, value):
        self.__hours_worked = clean_number(value, "Hours worked")

    # Polymorphism: a different salary formula than FullTimeEmployee
    def calculate_salary(self):
        return self.__hourly_rate * self.__hours_worked

    def get_employee_type(self):
        return "Part-Time"

    def get_details(self):
        return f"{self.__hourly_rate:,.2f} per hour x {self.__hours_worked:g} hours"

    def to_dict(self):
        data = super().to_dict()
        data["hourly_rate"] = self.__hourly_rate
        data["hours_worked"] = self.__hours_worked
        return data


class ManagerEmployee(FullTimeEmployee):
    """A full-time employee who also receives a bonus (multi-level inheritance)."""

    def __init__(self, employee_id, name, department, monthly_salary, bonus):
        super().__init__(employee_id, name, department, monthly_salary)
        self.__bonus = clean_number(bonus, "Bonus")

    @property
    def bonus(self):
        return self.__bonus

    @bonus.setter
    def bonus(self, value):
        self.__bonus = clean_number(value, "Bonus")

    # Polymorphism: reuses the parent's salary and adds the bonus
    def calculate_salary(self):
        return super().calculate_salary() + self.__bonus

    def get_employee_type(self):
        return "Manager"

    def get_details(self):
        return f"Monthly salary: {self.monthly_salary:,.2f} + bonus: {self.__bonus:,.2f}"

    def to_dict(self):
        data = super().to_dict()
        data["bonus"] = self.__bonus
        return data


# Maps the type name shown in the GUI / saved in JSON to its class.
EMPLOYEE_TYPES = {
    "Full-Time": FullTimeEmployee,
    "Part-Time": PartTimeEmployee,
    "Manager": ManagerEmployee,
}


def create_employee(employee_type, **data):
    """Create the right kind of Employee object from keyword data."""
    return EMPLOYEE_TYPES[employee_type](**data)


def employee_from_dict(data):
    """Rebuild an Employee object from a dictionary loaded from JSON."""
    data = dict(data)
    employee_type = data.pop("type")
    return create_employee(employee_type, **data)