import tkinter as tk
from tkinter import ttk, messagebox

from employee_db import (
    add_employee,
    create_database,
    delete_employee,
    get_all_employees,
    search_employee,
    update_employee,
)


class EmployeeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("1100x620")
        self.root.resizable(True, True)

        self.employee_id = None

        self.create_widgets()
        self.load_employees()

    def create_widgets(self):
        form_frame = ttk.LabelFrame(self.root, text="Employee Details", padding=15)
        form_frame.pack(fill="x", padx=10, pady=10)

        fields = [
            ("Name", 0, 0),
            ("Department", 0, 2),
            ("Position", 1, 0),
            ("Salary", 1, 2),
            ("Email", 2, 0),
            ("Phone", 2, 2),
            ("Date of Joining (YYYY-MM-DD)", 3, 0),
        ]

        self.entries = {}

        for label_text, row, col in fields:
            label = ttk.Label(form_frame, text=label_text)
            label.grid(row=row, column=col, padx=8, pady=8, sticky="w")

            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=row + 1, column=col, padx=8, pady=5, sticky="ew")
            self.entries[label_text] = entry

        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(3, weight=1)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(button_frame, text="Add Employee", command=self.add_employee).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Update Employee", command=self.update_employee).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Delete Employee", command=self.delete_employee).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Search", command=self.search_employee).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_fields).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(button_frame, text="Refresh", command=self.load_employees).grid(row=0, column=5, padx=5, pady=5)

        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Label(search_frame, text="Search Keyword:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var, width=40).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("id", "name", "department", "position", "salary", "email", "phone", "doj")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<ButtonRelease-1>", self.select_employee)

    def get_form_values(self):
        return {
            "name": self.entries["Name"].get().strip(),
            "department": self.entries["Department"].get().strip(),
            "position": self.entries["Position"].get().strip(),
            "salary": self.entries["Salary"].get().strip(),
            "email": self.entries["Email"].get().strip(),
            "phone": self.entries["Phone"].get().strip(),
            "doj": self.entries["Date of Joining (YYYY-MM-DD)"].get().strip(),
        }

    def clear_fields(self):
        self.employee_id = None
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.search_var.set("")
        self.load_employees()

    def add_employee(self):
        data = self.get_form_values()
        if not all(data.values()):
            messagebox.showwarning("Warning", "Please fill all fields.")
            return

        try:
            salary = float(data["salary"])
        except ValueError:
            messagebox.showwarning("Warning", "Salary must be a valid number.")
            return

        success = add_employee(
            data["name"],
            data["department"],
            data["position"],
            salary,
            data["email"],
            data["phone"],
            data["doj"],
        )

        if success:
            messagebox.showinfo("Success", "Employee added successfully.")
            self.clear_fields()
        else:
            messagebox.showerror("Error", "Failed to add employee.")

    def update_employee(self):
        if self.employee_id is None:
            messagebox.showwarning("Warning", "Please select an employee to update.")
            return

        data = self.get_form_values()
        if not all(data.values()):
            messagebox.showwarning("Warning", "Please fill all fields.")
            return

        try:
            salary = float(data["salary"])
        except ValueError:
            messagebox.showwarning("Warning", "Salary must be a valid number.")
            return

        success = update_employee(
            self.employee_id,
            data["name"],
            data["department"],
            data["position"],
            salary,
            data["email"],
            data["phone"],
            data["doj"],
        )

        if success:
            messagebox.showinfo("Success", "Employee updated successfully.")
            self.clear_fields()
        else:
            messagebox.showerror("Error", "Failed to update employee.")

    def delete_employee(self):
        if self.employee_id is None:
            messagebox.showwarning("Warning", "Please select an employee to delete.")
            return

        result = messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?")
        if not result:
            return

        success = delete_employee(self.employee_id)
        if success:
            messagebox.showinfo("Success", "Employee deleted successfully.")
            self.clear_fields()
        else:
            messagebox.showerror("Error", "Failed to delete employee.")

    def search_employee(self):
        keyword = self.search_var.get().strip()
        if not keyword:
            self.load_employees()
            return

        employees = search_employee(keyword)
        self.show_employees(employees)

    def load_employees(self):
        employees = get_all_employees()
        self.show_employees(employees)

    def show_employees(self, employees):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for emp in employees:
            self.tree.insert(
                "",
                "end",
                values=(
                    emp["id"],
                    emp["name"],
                    emp["department"],
                    emp["position"],
                    emp["salary"],
                    emp["email"],
                    emp["phone"],
                    emp["doj"],
                ),
            )

    def select_employee(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return

        values = self.tree.item(selected_item, "values")
        if not values:
            return

        self.employee_id = values[0]

        self.entries["Name"].delete(0, tk.END)
        self.entries["Name"].insert(0, values[1])

        self.entries["Department"].delete(0, tk.END)
        self.entries["Department"].insert(0, values[2])

        self.entries["Position"].delete(0, tk.END)
        self.entries["Position"].insert(0, values[3])

        self.entries["Salary"].delete(0, tk.END)
        self.entries["Salary"].insert(0, values[4])

        self.entries["Email"].delete(0, tk.END)
        self.entries["Email"].insert(0, values[5])

        self.entries["Phone"].delete(0, tk.END)
        self.entries["Phone"].insert(0, values[6])

        self.entries["Date of Joining (YYYY-MM-DD)"].delete(0, tk.END)
        self.entries["Date of Joining (YYYY-MM-DD)"].insert(0, values[7])


def main():
    create_database()
    root = tk.Tk()
    app = EmployeeManagementSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
