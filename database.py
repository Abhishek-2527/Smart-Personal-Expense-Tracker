import sqlite3

DATABASE_NAME = "expenses.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    """)

    # Settings table for monthly budget
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            monthly_budget REAL NOT NULL DEFAULT 0
        )
    """)

    # Create default budget setting
    cursor.execute("""
        INSERT OR IGNORE INTO settings (id, monthly_budget)
        VALUES (1, 0)
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("Database created successfully!")