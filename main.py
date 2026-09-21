from database import create_database
from expense_manager import add_expense


def show_menu():
    print("\n================================")
    print("       EXPENSE TRACKER")
    print("================================")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Update Expense")
    print("4. Delete Expense")
    print("5. Search Expenses")
    print("6. Expense Summary")
    print("7. Export to CSV")
    print("8. Exit")
    print("================================")


def main():
    create_database()

    while True:
        show_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter expense title: ")

            amount = float(input("Enter amount: "))

            category = input("Enter category: ")

            date = input("Enter date (YYYY-MM-DD): ")

            description = input("Enter description: ")

            add_expense(
                title,
                amount,
                category,
                date,
                description
            )

        elif choice == "2":
            print("\nView Expenses feature coming soon.")

        elif choice == "3":
            print("\nUpdate Expense feature coming soon.")

        elif choice == "4":
            print("\nDelete Expense feature coming soon.")

        elif choice == "5":
            print("\nSearch feature coming soon.")

        elif choice == "6":
            print("\nSummary feature coming soon.")

        elif choice == "7":
            print("\nCSV export feature coming soon.")

        elif choice == "8":
            print("\nThank you for using Expense Tracker!")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()