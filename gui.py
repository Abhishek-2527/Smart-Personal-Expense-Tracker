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
    export_to_csv,
    get_monthly_expense,
    get_monthly_expense_count,
    set_monthly_budget,
    get_monthly_budget,
    get_highest_category,
    get_category_summary,
    get_monthly_summary
)

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ExpenseTrackerGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("Smart Personal Expense Tracker")

        self.root.geometry("1200x750")

        self.root.minsize(1000, 650)

        self.selected_id = None

        self.create_widgets()

        self.load_expenses()

        self.update_dashboard()

    # =====================================================
    # MAIN GUI
    # =====================================================

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="Smart Personal Expense Tracker",
            font=("Arial", 24, "bold")
        )

        title.pack(pady=10)

        notebook = ttk.Notebook(self.root)

        notebook.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=5
        )

        self.expense_tab = ttk.Frame(notebook)

        self.dashboard_tab = ttk.Frame(notebook)

        self.chart_tab = ttk.Frame(notebook)

        notebook.add(
            self.expense_tab,
            text="Expense Manager"
        )

        notebook.add(
            self.dashboard_tab,
            text="Dashboard"
        )

        notebook.add(
            self.chart_tab,
            text="Charts"
        )

        self.create_expense_tab()

        self.create_dashboard_tab()

        self.create_chart_tab()

    # =====================================================
    # EXPENSE TAB
    # =====================================================

    def create_expense_tab(self):

        input_frame = tk.Frame(
            self.expense_tab
        )

        input_frame.pack(
            pady=10
        )

        # Title
        tk.Label(
            input_frame,
            text="Title"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

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
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5
        )

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
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

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
        ).grid(
            row=1,
            column=2,
            padx=5,
            pady=5
        )

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
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=5
        )

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
        button_frame = tk.Frame(
            self.expense_tab
        )

        button_frame.pack(
            pady=5
        )

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
        search_frame = tk.Frame(
            self.expense_tab
        )

        search_frame.pack(
            pady=5
        )

        tk.Label(
            search_frame,
            text="Search:"
        ).pack(
            side=tk.LEFT,
            padx=5
        )

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
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        tk.Button(
            search_frame,
            text="Show All",
            command=self.load_expenses
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        # Table
        table_frame = tk.Frame(
            self.expense_tab
        )

        table_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
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
                width=130
            )

        self.tree.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.tree.bind(
            "<ButtonRelease-1>",
            self.select_expense
        )

    # =====================================================
    # DASHBOARD
    # =====================================================

    def create_dashboard_tab(self):

        tk.Label(
            self.dashboard_tab,
            text="Financial Dashboard",
            font=("Arial", 22, "bold")
        ).pack(pady=15)

        cards_frame = tk.Frame(
            self.dashboard_tab
        )

        cards_frame.pack(
            pady=10
        )

        self.total_card = self.create_card(
            cards_frame,
            "Total Expenses",
            0
        )

        self.month_card = self.create_card(
            cards_frame,
            "This Month",
            0
        )

        self.budget_card = self.create_card(
            cards_frame,
            "Monthly Budget",
            0
        )

        self.remaining_card = self.create_card(
            cards_frame,
            "Remaining",
            0
        )

        # Budget section
        budget_frame = tk.LabelFrame(
            self.dashboard_tab,
            text="Monthly Budget"
        )

        budget_frame.pack(
            pady=15,
            padx=20,
            fill=tk.X
        )

        tk.Label(
            budget_frame,
            text="Set Budget:"
        ).pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )

        self.budget_entry = tk.Entry(
            budget_frame,
            width=15
        )

        self.budget_entry.pack(
            side=tk.LEFT,
            padx=5
        )

        tk.Button(
            budget_frame,
            text="Save Budget",
            command=self.save_budget
        ).pack(
            side=tk.LEFT,
            padx=10
        )

        self.budget_status = tk.Label(
            budget_frame,
            text="Budget not set.",
            font=("Arial", 11, "bold")
        )

        self.budget_status.pack(
            side=tk.LEFT,
            padx=20
        )

        # Insights
        insight_frame = tk.LabelFrame(
            self.dashboard_tab,
            text="Smart Spending Insights"
        )

        insight_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=20,
            pady=10
        )

        self.insights_text = tk.Text(
            insight_frame,
            height=10,
            font=("Arial", 12)
        )

        self.insights_text.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

    def create_card(
        self,
        parent,
        title,
        value
    ):

        frame = tk.LabelFrame(
            parent,
            text=title,
            width=200,
            height=100
        )

        frame.pack(
            side=tk.LEFT,
            padx=10
        )

        label = tk.Label(
            frame,
            text=f"₹{value:.2f}",
            font=("Arial", 18, "bold")
        )

        label.pack(
            padx=25,
            pady=20
        )

        return label

    # =====================================================
    # CHART TAB
    # =====================================================

    def create_chart_tab(self):

        tk.Label(
            self.chart_tab,
            text="Expense Analytics",
            font=("Arial", 22, "bold")
        ).pack(pady=10)

        button_frame = tk.Frame(
            self.chart_tab
        )

        button_frame.pack(
            pady=5
        )

        tk.Button(
            button_frame,
            text="Category Chart",
            command=self.show_category_chart
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        tk.Button(
            button_frame,
            text="Monthly Chart",
            command=self.show_monthly_chart
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        self.chart_frame = tk.Frame(
            self.chart_tab
        )

        self.chart_frame.pack(
            fill=tk.BOTH,
            expand=True
        )

    # =====================================================
    # ADD
    # =====================================================

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
                "Enter a valid positive amount."
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

        self.update_dashboard()

    # =====================================================
    # LOAD
    # =====================================================

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

    # =====================================================
    # SELECT
    # =====================================================

    def select_expense(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        item = self.tree.item(
            selected[0]
        )

        values = item["values"]

        self.selected_id = values[0]

        self.title_entry.delete(
            0,
            tk.END
        )

        self.title_entry.insert(
            0,
            values[1]
        )

        self.amount_entry.delete(
            0,
            tk.END
        )

        self.amount_entry.insert(
            0,
            values[2]
        )

        self.category_entry.delete(
            0,
            tk.END
        )

        self.category_entry.insert(
            0,
            values[3]
        )

        self.date_entry.delete(
            0,
            tk.END
        )

        self.date_entry.insert(
            0,
            values[4]
        )

        self.description_entry.delete(
            0,
            tk.END
        )

        self.description_entry.insert(
            0,
            values[5]
        )

    # =====================================================
    # UPDATE
    # =====================================================

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
                "Enter a valid amount."
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

        self.update_dashboard()

    # =====================================================
    # DELETE
    # =====================================================

    def delete_expense_gui(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "No Selection",
                "Select an expense first."
            )

            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete this expense?"
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

        self.clear_fields()

        self.load_expenses()

        self.update_dashboard()

    # =====================================================
    # SEARCH
    # =====================================================

    def search_expenses_gui(self):

        keyword = self.search_entry.get().strip()

        if not keyword:

            self.load_expenses()

            return

        expenses = search_expenses(
            keyword
        )

        for item in self.tree.get_children():

            self.tree.delete(item)

        for expense in expenses:

            self.tree.insert(
                "",
                tk.END,
                values=expense
            )

    # =====================================================
    # CLEAR
    # =====================================================

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

    # =====================================================
    # BUDGET
    # =====================================================

    def save_budget(self):

        value = self.budget_entry.get().strip()

        try:

            budget = float(value)

            if budget <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Budget",
                "Enter a valid positive budget."
            )

            return

        set_monthly_budget(
            budget
        )

        messagebox.showinfo(
            "Success",
            "Monthly budget saved."
        )

        self.update_dashboard()

    # =====================================================
    # DASHBOARD UPDATE
    # =====================================================

    def update_dashboard(self):

        total = get_total_expenses()

        current_month = datetime.now().strftime(
            "%Y-%m"
        )

        monthly = get_monthly_expense(
            current_month
        )

        budget = get_monthly_budget()

        remaining = budget - monthly

        self.total_card.config(
            text=f"₹{total:.2f}"
        )

        self.month_card.config(
            text=f"₹{monthly:.2f}"
        )

        self.budget_card.config(
            text=f"₹{budget:.2f}"
        )

        self.remaining_card.config(
            text=f"₹{remaining:.2f}"
        )

        if budget == 0:

            self.budget_status.config(
                text="Set a monthly budget."
            )

        elif monthly > budget:

            self.budget_status.config(
                text=f"⚠ Budget exceeded by ₹{abs(remaining):.2f}"
            )

        else:

            percentage = (
                monthly / budget
            ) * 100

            self.budget_status.config(
                text=f"Budget used: {percentage:.1f}%"
            )

        self.generate_insights(
            current_month,
            monthly,
            budget
        )

    # =====================================================
    # SMART INSIGHTS
    # =====================================================

    def generate_insights(
        self,
        month,
        monthly,
        budget
    ):

        self.insights_text.delete(
            "1.0",
            tk.END
        )

        insights = []

        expense_count = get_monthly_expense_count(
            month
        )

        insights.append(
            f"• You have {expense_count} transaction(s) this month."
        )

        if expense_count > 0:

            average = monthly / expense_count

            insights.append(
                f"• Your average expense per transaction is ₹{average:.2f}."
            )

        highest = get_highest_category(
            month
        )

        if highest:

            category, amount = highest

            insights.append(
                f"• Your highest spending category is "
                f"{category} (₹{amount:.2f})."
            )

        if budget > 0:

            percentage = (
                monthly / budget
            ) * 100

            if percentage >= 100:

                insights.append(
                    "• ⚠ You have exceeded your monthly budget."
                )

            elif percentage >= 80:

                insights.append(
                    "• ⚠ You have used more than 80% of your budget."
                )

            else:

                remaining = budget - monthly

                insights.append(
                    f"• You have ₹{remaining:.2f} remaining in your budget."
                )

        if monthly > 0:

            insights.append(
                f"• Your total spending this month is ₹{monthly:.2f}."
            )

        for insight in insights:

            self.insights_text.insert(
                tk.END,
                insight + "\n\n"
            )

    # =====================================================
    # CATEGORY CHART
    # =====================================================

    def show_category_chart(self):

        summary = get_category_summary()

        if not summary:

            messagebox.showinfo(
                "No Data",
                "Add expenses first."
            )

            return

        self.clear_chart()

        categories = [
            item[0]
            for item in summary
        ]

        amounts = [
            item[1]
            for item in summary
        ]

        figure = Figure(
            figsize=(7, 5),
            dpi=100
        )

        axis = figure.add_subplot(111)

        axis.pie(
            amounts,
            labels=categories,
            autopct="%1.1f%%"
        )

        axis.set_title(
            "Expense by Category"
        )

        canvas = FigureCanvasTkAgg(
            figure,
            master=self.chart_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True
        )

    # =====================================================
    # MONTHLY CHART
    # =====================================================

    def show_monthly_chart(self):

        summary = get_monthly_summary()

        if not summary:

            messagebox.showinfo(
                "No Data",
                "Add expenses first."
            )

            return

        self.clear_chart()

        months = [
            item[0]
            for item in summary
        ]

        amounts = [
            item[1]
            for item in summary
        ]

        months.reverse()

        amounts.reverse()

        figure = Figure(
            figsize=(8, 5),
            dpi=100
        )

        axis = figure.add_subplot(111)

        axis.bar(
            months,
            amounts
        )

        axis.set_title(
            "Monthly Expenses"
        )

        axis.set_xlabel(
            "Month"
        )

        axis.set_ylabel(
            "Amount (₹)"
        )

        axis.tick_params(
            axis="x",
            rotation=45
        )

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            master=self.chart_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True
        )

    # =====================================================
    # CLEAR CHART
    # =====================================================

    def clear_chart(self):

        for widget in self.chart_frame.winfo_children():

            widget.destroy()

    # =====================================================
    # CSV
    # =====================================================

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