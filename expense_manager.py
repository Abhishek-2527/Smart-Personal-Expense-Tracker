import sqlite3
import csv

from database import get_connection


def add_expense(title, amount, category, date, description):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (title, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?)
    """, (title, amount, category, date, description))

    connection.commit()
    connection.close()

    print("\nExpense added successfully!")


def get_all_expenses():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, amount, category, date, description
        FROM expenses
        ORDER BY date DESC, id DESC
    """)

    expenses = cursor.fetchall()

    connection.close()

    return expenses


def display_expenses(expenses):
    if not expenses:
        print("\nNo expenses found.")
        return

    print("\n" + "=" * 90)
    print(
        f"{'ID':<5}"
        f"{'Title':<20}"
        f"{'Amount':<12}"
        f"{'Category':<15}"
        f"{'Date':<15}"
        f"{'Description':<20}"
    )
    print("=" * 90)

    for expense in expenses:
        expense_id, title, amount, category, date, description = expense

        print(
            f"{expense_id:<5}"
            f"{title[:18]:<20}"
            f"₹{amount:<11.2f}"
            f"{category[:13]:<15}"
            f"{date:<15}"
            f"{(description or '')[:18]:<20}"
        )

    print("=" * 90)


def update_expense(expense_id, title, amount, category, date, description):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE expenses
        SET title = ?,
            amount = ?,
            category = ?,
            date = ?,
            description = ?
        WHERE id = ?
    """, (title, amount, category, date, description, expense_id))

    connection.commit()

    updated = cursor.rowcount

    connection.close()

    return updated


def delete_expense(expense_id):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    connection.commit()

    deleted = cursor.rowcount

    connection.close()

    return deleted


def search_expenses(keyword):
    connection = get_connection()

    cursor = connection.cursor()

    search_value = f"%{keyword}%"

    cursor.execute("""
        SELECT id, title, amount, category, date, description
        FROM expenses
        WHERE title LIKE ?
           OR category LIKE ?
           OR description LIKE ?
           OR date LIKE ?
        ORDER BY date DESC
    """, (search_value, search_value, search_value, search_value))

    expenses = cursor.fetchall()

    connection.close()

    return expenses


def get_total_expenses():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
    """)

    total = cursor.fetchone()[0]

    connection.close()

    return total


def get_category_summary():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, SUM(amount), COUNT(*)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    summary = cursor.fetchall()

    connection.close()

    return summary


def get_monthly_summary():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT substr(date, 1, 7) AS month,
               SUM(amount),
               COUNT(*)
        FROM expenses
        GROUP BY month
        ORDER BY month DESC
    """)

    summary = cursor.fetchall()

    connection.close()

    return summary


def export_to_csv(filename="expenses_export.csv"):
    expenses = get_all_expenses()

    if not expenses:
        print("\nNo expenses available for export.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Title",
            "Amount",
            "Category",
            "Date",
            "Description"
        ])

        writer.writerows(expenses)

    print(f"\nExpenses exported successfully to {filename}")