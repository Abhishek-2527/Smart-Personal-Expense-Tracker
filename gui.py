import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database import create_database
from expense_manager import (
    add_expense,
    get_all_expenses,
    update_expense,
    delete_expense,
    search_expenses,
    get_total_expenses,
    export_to_csv
)


class ExpenseTrackerGUI:

    def __init__(self, root):
        self.root = root

        self.root.title("Personal Expense Tracker")
        self.root.geometry("1000x650")

        self.selected_id = None

        self.create_widgets()
        self.load_expenses()

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="Personal Expense Tracker",
            font=("Arial", 24, "bold")
        )

        title.pack(pady=15)

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=5)

        # Title
        tk.Label(
            input_frame,
            text="Title"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.title_entry = tk.Entry(
            input_frame,
            width=20
        )

        self.title_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        # Amount
        tk.Label(
            input_frame,
            text="Amount"
        ).grid(row=0, column=2, padx=5, pady=5)

        self.amount_entry = tk.Entry(
            input_frame,
            width=15
        )

        self.amount_entry.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        # Category
        tk.Label(
            input_frame,
            text="Category"
        ).grid(row=1, column=0, padx=5, pady=5)

        self.category_entry = tk.Entry(
            input_frame,
            width=20
        )

        self.category_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        # Date
        tk.Label(
            input_frame,
            text="Date"
        ).grid(row=1, column=2, padx=5, pady=5)

        self.date_entry = tk.Entry(
            input_frame,
            width=15
        )

        self.date_entry.grid(
            row=1,
            column=3,
            padx=5,
            pady=5
        )

        self.date_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        # Description
        tk.Label(
            input_frame,
            text="Description"
        ).grid(row=2, column=0, padx=5, pady=5)

        self.description_entry = tk.Entry(
            input_frame,
            width=20
        )

        self.description_entry.grid(
            row=2,
            column=1,
            padx=5,
            pady=5
        )

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Add Expense",
            width=15,
            command=self.add_expense_gui
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Update",
            width=15,
            command=self.update_expense_gui
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Delete",
            width=15,
            command=self.delete_expense_gui
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="Clear",
            width=15,
            command=self.clear_fields
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            button_frame,
            text="Export CSV",
            width=15,
            command=self.export_csv_gui
        ).grid(row=0, column=4, padx=5)

        # Search
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=5)

        tk.Label(
            search_frame,
            text="Search:"
        ).pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(
            search_frame,
            width=30
        )

        self.search_entry.pack(
            side=tk.LEFT,
            padx=5
        )

        tk.Button(
            search_frame,
            text="Search",
            command=self.search_expenses_gui
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            search_frame,
            text="Show All",
            command=self.load_expenses
        ).pack(side=tk.LEFT, padx=5)

        # Table
        table_frame = tk.Frame(self.root)

        table_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=15,
            pady=10
        )

        columns = (
            "ID",
            "Title",
            "Amount",
            "Category",
            "Date",
            "Description"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:

            self.tree.heading(
                column,
                text=column
            )

            self.tree.column(
                column,
                width=120
            )

        self.tree.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.tree.bind(
            "<ButtonRelease-1>",
            self.select_expense
        )

        self.total_label = tk.Label(
            self.root,
            text="Total Expense: ₹0.00",
            font=("Arial", 16, "bold")
        )

        self.total_label.pack(pady=10)

    def add_expense_gui(self):

        title = self.title_entry.get().strip()
        amount = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()
        date = self.date_entry.get().strip()
        description = self.description_entry.get().strip()

        if not title or not amount or not category or not date:
            messagebox.showwarning(
                "Missing Data",
                "Please fill all required fields."
            )
            return

        try:
            amount = float(amount)

            if amount <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid positive amount."
            )
            return

        try:
            datetime.strptime(
                date,
                "%Y-%m-%d"
            )

        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Date must be YYYY-MM-DD."
            )
            return

        add_expense(
            title,
            amount,
            category,
            date,
            description
        )

        messagebox.showinfo(
            "Success",
            "Expense added successfully!"
        )

        self.clear_fields()
        self.load_expenses()

    def load_expenses(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        expenses = get_all_expenses()

        for expense in expenses:

            self.tree.insert(
                "",
                tk.END,
                values=expense
            )

        self.update_total()

    def select_expense(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        item = self.tree.item(
            selected[0]
        )

        values = item["values"]

        self.selected_id = values[0]

        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, values[1])

        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, values[2])

        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, values[3])

        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, values[4])

        self.description_entry.delete(0, tk.END)
        self.description_entry.insert(
            0,
            values[5]
        )

    def update_expense_gui(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "No Selection",
                "Select an expense first."
            )
            return

        title = self.title_entry.get().strip()
        amount = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()
        date = self.date_entry.get().strip()
        description = self.description_entry.get().strip()

        try:
            amount = float(amount)

            if amount <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Enter a valid positive amount."
            )
            return

        result = update_expense(
            self.selected_id,
            title,
            amount,
            category,
            date,
            description
        )

        if result:
            messagebox.showinfo(
                "Success",
                "Expense updated successfully!"
            )
        else:
            messagebox.showerror(
                "Error",
                "Expense not found."
            )

        self.clear_fields()
        self.load_expenses()

    def delete_expense_gui(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "No Selection",
                "Select an expense first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this expense?"
        )

        if not confirm:
            return

        result = delete_expense(
            self.selected_id
        )

        if result:
            messagebox.showinfo(
                "Success",
                "Expense deleted successfully!"
            )
        else:
            messagebox.showerror(
                "Error",
                "Expense not found."
            )

        self.clear_fields()
        self.load_expenses()

    def search_expenses_gui(self):

        keyword = self.search_entry.get().strip()

        if not keyword:
            self.load_expenses()
            return

        expenses = search_expenses(keyword)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for expense in expenses:
            self.tree.insert(
                "",
                tk.END,
                values=expense
            )

    def clear_fields(self):

        self.title_entry.delete(
            0,
            tk.END
        )

        self.amount_entry.delete(
            0,
            tk.END
        )

        self.category_entry.delete(
            0,
            tk.END
        )

        self.date_entry.delete(
            0,
            tk.END
        )

        self.date_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        self.description_entry.delete(
            0,
            tk.END
        )

        self.selected_id = None

    def update_total(self):

        total = get_total_expenses()

        self.total_label.config(
            text=f"Total Expense: ₹{total:.2f}"
        )

    def export_csv_gui(self):

        export_to_csv()

        messagebox.showinfo(
            "Export Complete",
            "Expenses exported to expenses_export.csv"
        )


def run_gui():

    create_database()

    root = tk.Tk()

    ExpenseTrackerGUI(root)

    root.mainloop()


if __name__ == "__main__":
    run_gui()