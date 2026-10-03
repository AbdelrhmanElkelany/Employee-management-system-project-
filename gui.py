import tkinter as tk
from tkinter import ttk, messagebox

from models import EMPLOYEE_TYPES, create_employee


class EmployeeApp:

    FIELD_LABELS = {
        "monthly_salary": "Monthly Salary",
        "hourly_rate": "Hourly Rate",
        "hours_worked": "Hours Worked",
        "bonus": "Bonus",
    }
    # Which number fields each employee type needs.
    TYPE_FIELDS = {
        "Full-Time": ["monthly_salary"],
        "Part-Time": ["hourly_rate", "hours_worked"],
        "Manager": ["monthly_salary", "bonus"],
    }

    def __init__(self, root, manager):
        self.root = root
        self.manager = manager

        self.id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.department_var = tk.StringVar()
        self.type_var = tk.StringVar(value="Full-Time")
        self.number_vars = {key: tk.StringVar() for key in self.FIELD_LABELS}
        self.number_entries = {}
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar()

        self.root.title("Employee Management System")
        self.root.geometry("1050x540")
        self.root.minsize(950, 480)

        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self._build_form(main_frame)
        self._build_table_area(main_frame)

        self._update_fields()
        self._refresh_table(self.manager.get_all_employees())

    # ---------- Building the interface ----------
    def _build_form(self, parent):
        form = ttk.LabelFrame(parent, text="Add New Employee", padding=10)
        form.grid(row=0, column=0, sticky="n", padx=(0, 10))

        self._add_text_row(form, 0, "Employee ID", self.id_var)
        self._add_text_row(form, 1, "Name", self.name_var)
        self._add_text_row(form, 2, "Department", self.department_var)

        ttk.Label(form, text="Employee Type").grid(row=3, column=0, sticky="w", pady=4)
        type_box = ttk.Combobox(form, textvariable=self.type_var, state="readonly",
                                values=list(EMPLOYEE_TYPES), width=22)
        type_box.grid(row=3, column=1, pady=4)
        type_box.bind("<<ComboboxSelected>>", self._update_fields)

        for row, (key, label) in enumerate(self.FIELD_LABELS.items(), start=4):
            entry = self._add_text_row(form, row, label, self.number_vars[key])
            self.number_entries[key] = entry

        button_frame = ttk.Frame(form)
        button_frame.grid(row=8, column=0, columnspan=2, pady=(12, 0))
        ttk.Button(button_frame, text="Add Employee", command=self.on_add).pack(side="left", padx=4)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side="left", padx=4)

    def _add_text_row(self, parent, row, label, variable):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        entry = ttk.Entry(parent, textvariable=variable, width=25)
        entry.grid(row=row, column=1, pady=4)
        return entry

    def _build_table_area(self, parent):
        right = ttk.Frame(parent)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

        # Search bar
        search_frame = ttk.LabelFrame(right, text="Search (ID, name, department or type)", padding=8)
        search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        search_frame.columnconfigure(0, weight=1)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        search_entry.bind("<Return>", lambda event: self.on_search())
        ttk.Button(search_frame, text="Search", command=self.on_search).grid(row=0, column=1, padx=3)
        ttk.Button(search_frame, text="Show All", command=self.on_show_all).grid(row=0, column=2, padx=3)

        # Table of employees
        columns = ("id", "name", "department", "type", "details", "salary")
        self.tree = ttk.Treeview(right, columns=columns, show="headings", selectmode="browse")
        headings = {"id": ("ID", 70), "name": ("Name", 140), "department": ("Department", 110),
                    "type": ("Type", 80), "details": ("Pay Details", 260), "salary": ("Monthly Pay", 100)}
        for column, (title, width) in headings.items():
            self.tree.heading(column, text=title)
            self.tree.column(column, width=width, anchor="w")
        self.tree.grid(row=1, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(right, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        ttk.Label(right, textvariable=self.status_var).grid(row=2, column=0, columnspan=2,
                                                            sticky="w", pady=(8, 0))

    # ---------- Form helpers ----------
    def _update_fields(self, event=None):
        """Enable only the number fields needed by the selected employee type."""
        active = self.TYPE_FIELDS[self.type_var.get()]
        for key, entry in self.number_entries.items():
            if key in active:
                entry.config(state="normal")
            else:
                self.number_vars[key].set("")
                entry.config(state="disabled")

    def clear_form(self):
        self.id_var.set("")
        self.name_var.set("")
        self.department_var.set("")
        for variable in self.number_vars.values():
            variable.set("")

    def _read_number_text(self, key):
        text = self.number_vars[key].get().strip()
        if not text:
            raise ValueError(f"{self.FIELD_LABELS[key]} is required.")
        return text

    def _build_employee_from_form(self):
        """Create an Employee object from the form. Raises ValueError if invalid."""
        employee_type = self.type_var.get()
        extra_values = {key: self._read_number_text(key) for key in self.TYPE_FIELDS[employee_type]}
        return create_employee(
            employee_type,
            employee_id=self.id_var.get(),
            name=self.name_var.get(),
            department=self.department_var.get(),
            **extra_values,
        )

    # ---------- Button actions ----------
    def on_add(self):
        try:
            employee = self._build_employee_from_form()
            self.manager.add_employee(employee)
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
            return
        except OSError as error:
            messagebox.showerror("File Error", f"The employee could not be saved:\n{error}")
            return

        self._refresh_table(self.manager.get_all_employees())
        self.search_var.set("")
        self.clear_form()
        messagebox.showinfo("Success", f"{employee.name} was added successfully.")

    def on_search(self):
        keyword = self.search_var.get().strip()
        if not keyword:
            messagebox.showwarning("Search", "Please type something to search for.")
            return
        results = self.manager.search(keyword)
        self._refresh_table(results)
        if not results:
            messagebox.showinfo("No Results", f'No employee matches "{keyword}".')

    def on_show_all(self):
        self.search_var.set("")
        self._refresh_table(self.manager.get_all_employees())

    # ---------- Table helper ----------
    def _refresh_table(self, employees):
        """Show the given employees in the table and update the status line."""
        self.tree.delete(*self.tree.get_children())
        for employee in employees:
            # Polymorphism: same calls, different result for each employee type.
            self.tree.insert("", "end", values=(
                employee.employee_id,
                employee.name,
                employee.department,
                employee.get_employee_type(),
                employee.get_details(),
                f"{employee.calculate_salary():,.2f}",
            ))
        total = len(self.manager.get_all_employees())
        self.status_var.set(
            f"Showing {len(employees)} of {total} employee(s)   |   "
            f"Total monthly payroll: {self.manager.total_payroll():,.2f}"
        )