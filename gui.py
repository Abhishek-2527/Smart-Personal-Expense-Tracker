import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

from expense_manager import (
    add_expense,
    get_all_expenses,
    delete_expense,
    get_total_expenses,
    get_monthly_expense,
    get_monthly_budget,
    set_monthly_budget
)


# ==========================================
# APP SETTINGS
# ==========================================

# ==========================================
# COLOR THEME
# ==========================================

ctk.set_appearance_mode("dark")

COLORS = {
    "background": "#0F172A",
    "sidebar": "#111827",
    "card": "#1E293B",
    "card_blue": "#2563EB",
    "card_green": "#059669",
    "card_orange": "#D97706",
    "card_purple": "#7C3AED",
    "text": "#F8FAFC",
    "secondary_text": "#94A3B8",
    "button": "#2563EB",
    "button_hover": "#1D4ED8",
    "success": "#10B981",
    "danger": "#EF4444",
    "border": "#334155"
}

# ==========================================
# MAIN APPLICATION
# ==========================================

class ExpenseTracker(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Smart Expense Tracker")
        self.geometry("1200x750")
        self.minsize(1000, 650)

        self.configure(
            fg_color=COLORS["background"]
    )

        self.current_month = datetime.now().strftime("%Y-%m")

        self.create_layout()
        self.create_dashboard()

        self.refresh_dashboard()


    # ==========================================
    # LAYOUT
    # ==========================================

    def create_layout(self):

        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0,
            fg_color=COLORS["sidebar"]
    )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)


        # Main area
        self.main_area = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=COLORS["background"]
    )

        self.main_area.pack(
            side="right",
            fill="both",
            expand=True
        )


        # Sidebar title
        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="💰 Expense\nTracker",
            font=("Segoe UI", 24, "bold")
        )

        self.logo.pack(
            pady=(40, 50)
        )


        # Navigation buttons
        self.dashboard_btn = ctk.CTkButton(
            self.sidebar,
            text="🏠  Dashboard",
            height=45,
            corner_radius=12,
            fg_color=COLORS["button"],
            hover_color=COLORS["button_hover"],
            text_color=COLORS["text"],
            font=("Segoe UI", 15, "bold"),
            command=self.show_dashboard
    )

        self.dashboard_btn.pack(
            padx=20,
            pady=10,
            fill="x"
        )


        self.expense_btn = ctk.CTkButton(
            self.sidebar,
            text="💳  Expenses",
            height=45,
            corner_radius=12,
            fg_color=COLORS["button"],
            hover_color=COLORS["button_hover"],
            text_color=COLORS["text"],
            font=("Segoe UI", 15, "bold"),
            command=self.show_expenses
        )

        self.expense_btn.pack(
            padx=20,
            pady=10,
            fill="x"
        )


        self.budget_btn = ctk.CTkButton(
            self.sidebar,
            text="🎯  Budget",
            height=45,
            corner_radius=12,
            fg_color=COLORS["button"],
            hover_color=COLORS["button_hover"],
            text_color=COLORS["text"],
            font=("Segoe UI", 15, "bold"),
            command=self.show_budget
        )

        self.budget_btn.pack(
            padx=20,
            pady=10,
            fill="x"
        )


        # Theme button
        self.theme_btn = ctk.CTkButton(
            self.sidebar,
            text="☀️  Toggle Theme",
            height=42,
            corner_radius=12,
            fg_color="transparent",
            hover_color=COLORS["card"],
            border_width=1,
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            command=self.toggle_theme
        )

        self.theme_btn.pack(
            side="bottom",
            padx=20,
            pady=30,
            fill="x"
        )


    # ==========================================
    # DASHBOARD
    # ==========================================

    def create_dashboard(self):

        self.clear_main()

        title = ctk.CTkLabel(
            self.main_area,
            text="Dashboard",
            font=("Segoe UI", 32, "bold")
        )

        title.pack(
            anchor="w",
            padx=40,
            pady=(35, 5)
        )


        subtitle = ctk.CTkLabel(
            self.main_area,
            text="Track your spending and manage your money smarter.",
            font=("Segoe UI", 15)
        )

        subtitle.pack(
            anchor="w",
            padx=40,
            pady=(0, 30)
        )


        # Cards container
        cards = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        cards.pack(
            fill="x",
            padx=40
        )


        # Total expenses
        self.total_card = self.create_card(
            cards,
            "💰 Total Expenses",
            "₹0",
            COLORS["card_blue"]
    )

        self.total_card.grid(
            row=0,
            column=0,
            padx=10,
            sticky="nsew"
        )


        # Monthly expense
        self.month_card = self.create_card(
            cards,
            "📅 This Month",
            "₹0",
            COLORS["card_green"]
        )

        self.month_card.grid(
            row=0,
            column=1,
            padx=10,
            sticky="nsew"
        )


        # Budget
        self.budget_card = self.create_card(
            cards,
            "🎯 Monthly Budget",
            "₹0",
            COLORS["card_orange"]
        )

        self.budget_card.grid(
            row=0,
            column=2,
            padx=10,
            sticky="nsew"
        )


        cards.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )


        # Welcome section

        welcome = ctk.CTkFrame(
            self.main_area,
            corner_radius=25,
            fg_color=COLORS["card"],
            border_width=1,
            border_color=COLORS["border"]
        )

        welcome.pack(
            fill="both",
            expand=True,
            padx=50,
            pady=40
        )


        welcome_title = ctk.CTkLabel(
            welcome,
            text="Welcome to Smart Expense Tracker 🚀",
            font=("Segoe UI", 26, "bold"),
            text_color=COLORS["text"]
        )

        welcome_title.pack(
            pady=(50, 15)
        )


        welcome_text = ctk.CTkLabel(
            welcome,
            text=(
                "Manage your daily expenses,\n"
                "track your monthly budget,\n"
                "and understand your spending habits."
            ),
            font=("Segoe UI", 17),
            text_color=COLORS["secondary_text"],
            justify="center"
        )

        welcome_text.pack(
            pady=10
        )


        add_button = ctk.CTkButton(
            welcome,
            text="＋ Add New Expense",
            width=240,
            height=52,
            corner_radius=15,
            fg_color=COLORS["button"],
            hover_color=COLORS["button_hover"],
            text_color="white",
            font=("Segoe UI", 16, "bold"),
            command=self.show_expenses
        )

        add_button.pack(
            pady=30
        )


    # ==========================================
    # CARD
    # ==========================================

    def create_card(self, parent, title, value, color=None):

        if color is None:
            color = COLORS["card"]

        card = ctk.CTkFrame(
            parent,
            height=160,
            corner_radius=20,
            fg_color=color
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 15, "bold"),
            text_color="#E2E8F0"
        )

        title_label.pack(
            anchor="w",
            padx=22,
            pady=(22, 5)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        )

        value_label.pack(
            anchor="w",
            padx=22,
            pady=10
        )

        card.value_label = value_label

        return card


    # ==========================================
    # EXPENSE PAGE
    # ==========================================

    def show_expenses(self):

        self.clear_main()

        title = ctk.CTkLabel(
            self.main_area,
            text="Expense Manager",
            font=("Segoe UI", 30, "bold")
        )

        title.pack(
            anchor="w",
            padx=40,
            pady=(30, 20)
        )


        form = ctk.CTkFrame(
            self.main_area,
            corner_radius=20
        )

        form.pack(
            fill="x",
            padx=40
        )


        self.title_entry = ctk.CTkEntry(
            form,
            placeholder_text="Expense title",
            height=45
        )

        self.title_entry.grid(
            row=0,
            column=0,
            padx=15,
            pady=20
        )


        self.amount_entry = ctk.CTkEntry(
            form,
            placeholder_text="Amount",
            height=45
        )

        self.amount_entry.grid(
            row=0,
            column=1,
            padx=15
        )


        self.category_entry = ctk.CTkEntry(
            form,
            placeholder_text="Category",
            height=45
        )

        self.category_entry.grid(
            row=0,
            column=2,
            padx=15
        )


        add_btn = ctk.CTkButton(
            form,
            text="＋ Add",
            height=45,
            width=120,
            command=self.add_new_expense
        )

        add_btn.grid(
            row=0,
            column=3,
            padx=15
        )


        # Expense list
        self.expense_list = ctk.CTkTextbox(
            self.main_area,
            corner_radius=15,
            font=("Consolas", 14)
        )

        self.expense_list.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=30
        )

        self.load_expenses()


    # ==========================================
    # ADD EXPENSE
    # ==========================================

    def add_new_expense(self):

        title = self.title_entry.get()
        amount = self.amount_entry.get()
        category = self.category_entry.get()

        if not title or not amount or not category:

            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )

            return


        try:

            amount = float(amount)

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid number."
            )

            return


        date = datetime.now().strftime("%Y-%m-%d")


        add_expense(
            title,
            amount,
            category,
            date,
            ""
        )


        self.title_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")
        self.category_entry.delete(0, "end")


        self.load_expenses()
        self.refresh_dashboard()


        messagebox.showinfo(
            "Success",
            "Expense added successfully! 🎉"
        )


    # ==========================================
    # LOAD EXPENSES
    # ==========================================

    def load_expenses(self):

        expenses = get_all_expenses()

        self.expense_list.delete(
            "1.0",
            "end"
        )


        if not expenses:

            self.expense_list.insert(
                "end",
                "\nNo expenses added yet."
            )

            return


        for expense in expenses:

            expense_id, title, amount, category, date, description = expense

            text = (
                f"#{expense_id:<4} "
                f"{title:<20} "
                f"₹{amount:<10.2f} "
                f"{category:<15} "
                f"{date}\n"
            )

            self.expense_list.insert(
                "end",
                text
            )


    # ==========================================
    # BUDGET
    # ==========================================

    def show_budget(self):

        self.clear_main()

        title = ctk.CTkLabel(
            self.main_area,
            text="Monthly Budget",
            font=("Segoe UI", 30, "bold")
        )

        title.pack(
            anchor="w",
            padx=40,
            pady=(30, 20)
        )


        budget_frame = ctk.CTkFrame(
            self.main_area,
            corner_radius=20
        )

        budget_frame.pack(
            padx=40,
            pady=20,
            fill="x"
        )


        self.budget_entry = ctk.CTkEntry(
            budget_frame,
            placeholder_text="Enter monthly budget",
            width=300,
            height=45
        )

        self.budget_entry.pack(
            side="left",
            padx=20,
            pady=30
        )


        save_btn = ctk.CTkButton(
            budget_frame,
            text="Save Budget",
            height=45,
            command=self.save_budget
        )

        save_btn.pack(
            side="left",
            padx=10
        )


        self.budget_status = ctk.CTkLabel(
            self.main_area,
            text="",
            font=("Segoe UI", 20)
        )

        self.budget_status.pack(
            pady=40
        )


        self.update_budget_display()


    # ==========================================
    # SAVE BUDGET
    # ==========================================

    def save_budget(self):

        try:

            budget = float(
                self.budget_entry.get()
            )

            if budget <= 0:

                raise ValueError


            set_monthly_budget(
                budget
            )


            self.update_budget_display()

            messagebox.showinfo(
                "Budget Updated",
                "Monthly budget saved successfully! 🎯"
            )


        except ValueError:

            messagebox.showerror(
                "Invalid Budget",
                "Enter a valid positive amount."
            )


    # ==========================================
    # BUDGET DISPLAY
    # ==========================================

    def update_budget_display(self):

        budget = get_monthly_budget()

        spent = get_monthly_expense(
            self.current_month
        )


        remaining = budget - spent


        self.budget_status.configure(
            text=(
                f"Budget: ₹{budget:,.2f}\n\n"
                f"Spent: ₹{spent:,.2f}\n\n"
                f"Remaining: ₹{remaining:,.2f}"
            )
        )


    # ==========================================
    # DASHBOARD REFRESH
    # ==========================================

    def refresh_dashboard(self):

        total = get_total_expenses()

        monthly = get_monthly_expense(
            self.current_month
        )

        budget = get_monthly_budget()


        if hasattr(self, "total_card"):

            self.total_card.value_label.configure(
                text=f"₹{total:,.2f}"
            )


        if hasattr(self, "month_card"):

            self.month_card.value_label.configure(
                text=f"₹{monthly:,.2f}"
            )


        if hasattr(self, "budget_card"):

            self.budget_card.value_label.configure(
                text=f"₹{budget:,.2f}"
            )


    # ==========================================
    # PAGE SWITCH
    # ==========================================

    def show_dashboard(self):

        self.create_dashboard()
        self.refresh_dashboard()


    # ==========================================
    # THEME
    # ==========================================

    def toggle_theme(self):

        current = ctk.get_appearance_mode()

        if current == "Dark":

            ctk.set_appearance_mode("light")

        else:

            ctk.set_appearance_mode("dark")


    # ==========================================
    # CLEAR MAIN AREA
    # ==========================================

    def clear_main(self):

        for widget in self.main_area.winfo_children():

            widget.destroy()


# ==========================================
# RUN APP
# ==========================================

def run_gui():

    app = ExpenseTracker()

    app.mainloop()


if __name__ == "__main__":

    run_gui()