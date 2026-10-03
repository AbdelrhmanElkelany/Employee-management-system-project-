# Employee Management System

A desktop application built with **Python** and **Tkinter** to manage company employees. It was developed as a university project to demonstrate the four core principles of **Object-Oriented Programming (OOP)** in a real, working GUI application.

---

## Features

- **Add employees** of three types: Full-Time, Part-Time, and Manager
- **Input validation** with clear error messages (empty fields, invalid numbers, negative values, duplicate IDs)
- **View all employees** in a table (`ttk.Treeview`) with pay details and monthly pay
- **Search** by ID, name, department, or employee type, with a "no results" message
- **Total monthly payroll** displayed under the table
- **Automatic saving** to `data.json`, so records remain after closing the app
- The form adapts to the selected type and enables only the fields it needs

---

## OOP Principles

| Principle | Where it is applied |
| --- | --- |
| **Encapsulation** | Private attributes (`__name`, `__monthly_salary`, ...) accessed through properties with validation in the setters. `EmployeeManager` keeps its list private and returns only a copy. |
| **Abstraction** | `Employee` is an abstract class (`ABC`) with abstract methods `calculate_salary()`, `get_employee_type()`, `get_details()`. `EmployeeManager` hides JSON handling and duplicate checking behind `add_employee()` and `search()`. |
| **Inheritance** | `FullTimeEmployee` and `PartTimeEmployee` inherit from `Employee`. `ManagerEmployee` inherits from `FullTimeEmployee` (a manager is a full-time employee with a bonus). |
| **Polymorphism** | `calculate_salary()`, `get_details()`, `get_employee_type()` and `to_dict()` are overridden in each subclass. The GUI calls them on any employee without checking its type. |

### Salary calculation

| Type | Monthly pay |
| --- | --- |
| Full-Time | Monthly salary |
| Part-Time | Hourly rate x hours worked |
| Manager | Monthly salary + bonus |

### Class hierarchy

```
Employee (abstract)
├── FullTimeEmployee
│   └── ManagerEmployee
└── PartTimeEmployee
```

---

## Project Structure

```
employee_system/
├── main.py      # Entry point: starts the application
├── models.py    # Employee classes (the OOP core) and validation helpers
├── manager.py   # EmployeeManager: storage, search, JSON save/load
├── gui.py       # EmployeeApp: the Tkinter user interface
└── data.json    # Created automatically after the first employee is added
```

The data logic (`models.py`, `manager.py`) is kept separate from the interface (`gui.py`).

---

## Getting Started

### Requirements

- Python **3.8 or newer**
- Tkinter (included with the standard Python installer)
  - On some Linux systems: `sudo apt install python3-tk`

No external libraries are needed.

### Run

```bash
git clone <your-repository-url>
cd employee_system
python main.py
```

On macOS/Linux, use `python3 main.py` if `python` does not work.

---

## How to Use

1. **Add:** fill in ID, name, department, choose the type, enter the pay fields, then click **Add Employee**.
2. **View:** all employees appear in the table on the right.
3. **Search:** type a keyword and click **Search** (or press Enter). Click **Show All** to see everyone again.
4. **Clear Form:** resets the input fields.

---

## Testing Checklist

| Test | Expected result |
| --- | --- |
| Add a valid employee | Success message, form clears, new row in the table |
| Add with empty name / `abc` salary / negative salary / duplicate ID | Error message, nothing added, no crash |
| Add Part-Time (rate 20, hours 50) and Manager (salary 5000, bonus 800) | Monthly pay shows `1,000.00` and `5,800.00` |
| Search for an existing value | Only matching rows are shown |
| Search for a non-existing value | "No Results" message |
| Close and reopen the app | Saved records are still there |

---

## Possible Improvements

- Edit and delete employees
- Export records to CSV
- Sort the table by column

---

## Author

**Abdelrhman Elkelany**
[LinkedIn](https://www.linkedin.com/in/abdelrhman-elkelany-583a302a7?utm_source=share_via&utm_content=profile&utm_medium=member_android)

## License

This project was created for educational purposes.
