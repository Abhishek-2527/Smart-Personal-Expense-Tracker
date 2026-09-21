from datetime import datetime

from database import create_database

from expense_manager import (
    add_expense,
    get_all_expenses,
    display_expenses,
    update_expense,
    delete_expense,
    search_expenses,
    get_total_expenses,
    get_category_summary,
    get_monthly_summary,
    export_to_csv
)


def show_menu():
    print("\n" + "=" * 45)
    print("          PERSONAL EXPENSE TRACKER")
    print("=" * 45)
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Update Expense")
    print("4. Delete Expense")
    print("5. Search Expenses")
    print("6. Expense Summary")
    print("7. Category-wise Summary")
    print("8. Monthly Summary")
    print("9. Export to CSV")
    print("10. Exit")
    print("=" * 45)


def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

            return amount

        except ValueError:
            print("Please enter a valid amount.")


def get_valid_date():
    while True:
        date = input("Enter date (YYYY-MM-DD): ")

        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date

        except ValueError:
            print("Invalid date. Use YYYY-MM-DD format.")


def add_expense_menu():
    print("\n--- Add Expense ---")

    title = input("Enter expense title: ").strip()

    if not title:
        print("Title cannot be empty.")
        return

    amount = get_valid_amount()

    category = input("Enter category: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    date = get_valid_date()

    description = input("Enter description: ").strip()

    add_expense(
        title,
        amount,
        category,
        date,
        description
    )


def view_expenses_menu():
    print("\n--- All Expenses ---")

    expenses = get_all_expenses()

    display_expenses(expenses)


def update_expense_menu():
    print("\n--- Update Expense ---")

    expenses = get_all_expenses()

    if not expenses:
        print("No expenses available.")
        return

    display_expenses(expenses)

    try:
        expense_id = int(input("Enter expense ID to update: "))

    except ValueError:
        print("Invalid ID.")
        return

    title = input("Enter new title: ").strip()

    if not title:
        print("Title cannot be empty.")
        return

    amount = get_valid_amount()

    category = input("Enter new category: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    date = get_valid_date()

    description = input("Enter new description: ").strip()

    result = update_expense(
        expense_id,
        title,
        amount,
        category,
        date,
        description
    )

    if result:
        print("\nExpense updated successfully!")

    else:
        print("\nExpense ID not found.")


def delete_expense_menu():
    print("\n--- Delete Expense ---")

    expenses = get_all_expenses()

    if not expenses:
        print("No expenses available.")
        return

    display_expenses(expenses)

    try:
        expense_id = int(input("Enter expense ID to delete: "))

    except ValueError:
        print("Invalid ID.")
        return

    result = delete_expense(expense_id)

    if result:
        print("\nExpense deleted successfully!")

    else:
        print("\nExpense ID not found.")


def search_expenses_menu():
    print("\n--- Search Expenses ---")

    keyword = input(
        "Enter title, category, date or keyword: "
    ).strip()

    if not keyword:
        print("Search keyword cannot be empty.")
        return

    expenses = search_expenses(keyword)

    display_expenses(expenses)


def expense_summary_menu():
    print("\n--- Expense Summary ---")

    total = get_total_expenses()

    expenses = get_all_expenses()

    print(f"\nTotal Expenses : ₹{total:.2f}")
    print(f"Number of Expenses : {len(expenses)}")


def category_summary_menu():
    print("\n--- Category-wise Summary ---")

    summary = get_category_summary()

    if not summary:
        print("No expenses available.")
        return

    print("\n" + "=" * 50)
    print(f"{'Category':<25}{'Total':<15}{'Count':<10}")
    print("=" * 50)

    for category, total, count in summary:
        print(
            f"{category:<25}"
            f"₹{total:<14.2f}"
            f"{count:<10}"
        )

    print("=" * 50)


def monthly_summary_menu():
    print("\n--- Monthly Summary ---")

    summary = get_monthly_summary()

    if not summary:
        print("No expenses available.")
        return

    print("\n" + "=" * 45)
    print(f"{'Month':<20}{'Total':<15}{'Count':<10}")
    print("=" * 45)

    for month, total, count in summary:
        print(
            f"{month:<20}"
            f"₹{total:<14.2f}"
            f"{count:<10}"
        )

    print("=" * 45)


def main():
    create_database()

    while True:
        show_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense_menu()

        elif choice == "2":
            view_expenses_menu()

        elif choice == "3":
            update_expense_menu()

        elif choice == "4":
            delete_expense_menu()

        elif choice == "5":
            search_expenses_menu()

        elif choice == "6":
            expense_summary_menu()

        elif choice == "7":
            category_summary_menu()

        elif choice == "8":
            monthly_summary_menu()

        elif choice == "9":
            export_to_csv()

        elif choice == "10":
            print("\nThank you for using Expense Tracker!")
            break

        else:
            print("\nInvalid choice. Please select 1-10.")


if __name__ == "__main__":
    main()