import csv
from database import get_connection


# =========================
# ADD EXPENSE
# =========================
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


# =========================
# GET ALL EXPENSES
# =========================
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


# Keep your old function name working too
def get_expenses():
    return get_all_expenses()


# =========================
# UPDATE EXPENSE
# =========================
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
    """, (
        title,
        amount,
        category,
        date,
        description,
        expense_id
    ))

    connection.commit()
    connection.close()


# =========================
# DELETE EXPENSE
# =========================
def delete_expense(expense_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (expense_id,))

    connection.commit()
    connection.close()


# =========================
# SEARCH EXPENSES
# =========================
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
        ORDER BY date DESC
    """, (
        search_value,
        search_value,
        search_value
    ))

    expenses = cursor.fetchall()

    connection.close()

    return expenses


# =========================
# TOTAL EXPENSE
# =========================
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


# =========================
# EXPORT CSV
# =========================
def export_to_csv(filename="expenses_export.csv"):
    expenses = get_all_expenses()

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

    return filename


# =========================
# MONTHLY EXPENSE
# =========================
def get_monthly_expense(month):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE substr(date, 1, 7) = ?
    """, (month,))

    total = cursor.fetchone()[0]

    connection.close()

    return total


# =========================
# MONTHLY EXPENSE COUNT
# =========================
def get_monthly_expense_count(month):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM expenses
        WHERE substr(date, 1, 7) = ?
    """, (month,))

    count = cursor.fetchone()[0]

    connection.close()

    return count


# =========================
# SET MONTHLY BUDGET
# =========================
def set_monthly_budget(amount):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE settings
        SET monthly_budget = ?
        WHERE id = 1
    """, (amount,))

    connection.commit()
    connection.close()


# =========================
# GET MONTHLY BUDGET
# =========================
def get_monthly_budget():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT monthly_budget
        FROM settings
        WHERE id = 1
    """)

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return 0


# =========================
# HIGHEST SPENDING CATEGORY
# =========================
def get_highest_category(month):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE substr(date, 1, 7) = ?
        GROUP BY category
        ORDER BY SUM(amount) DESC
        LIMIT 1
    """, (month,))

    result = cursor.fetchone()

    connection.close()

    return result


# =========================
# CATEGORY SUMMARY
# =========================
def get_category_summary():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    result = cursor.fetchall()

    connection.close()

    return result


# =========================
# MONTHLY SUMMARY
# =========================
def get_monthly_summary():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT substr(date, 1, 7) AS month,
               SUM(amount)
        FROM expenses
        GROUP BY month
        ORDER BY month ASC
    """)

    result = cursor.fetchall()

    connection.close()

    return result