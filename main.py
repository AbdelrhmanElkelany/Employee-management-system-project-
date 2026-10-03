import os
import tkinter as tk
from tkinter import messagebox

from gui import EmployeeApp
from manager import EmployeeManager


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    manager = EmployeeManager(os.path.join(folder, "data.json"))

    root = tk.Tk()
    EmployeeApp(root, manager)

    if manager.load_warning:
        messagebox.showwarning("Data File", manager.load_warning)

    root.mainloop()


if __name__ == "__main__":
    main()