import sqlite3
from database import DATABASE_NAME


def add_expense(title, amount, category, date, description):
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (title, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?)
    """, (title, amount, category, date, description))

    connection.commit()
    connection.close()

    print("\nExpense added successfully!")