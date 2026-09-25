# 💰 Smart Personal Expense Tracker

<p align="center">
  <b>A simple and user-friendly desktop application for managing, tracking, and analyzing personal expenses.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-Database-lightgrey?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/GUI-Tkinter-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/CSV-Export-green?style=for-the-badge" />
</p>

---

## 📌 About The Project

**Smart Personal Expense Tracker** is a Python-based desktop application designed to help users record, manage, search, and analyze their daily expenses.

The application uses **SQLite for persistent data storage** and provides a graphical interface for interacting with expense records.

It was developed as a practical project to strengthen Python programming, database management, GUI development, and application-building skills.

---

## ✨ Features

* ➕ Add new expenses
* 📋 View all expenses
* ✏️ Update existing expenses
* 🗑️ Delete expenses
* 🔍 Search expenses
* 💰 Calculate total expenses
* 📊 Category-wise expense summary
* 📅 Monthly expense summary
* 📄 Export expenses to CSV
* ✅ Input validation
* 💾 Persistent data storage using SQLite
* 🖥️ User-friendly graphical interface

---

## 🛠️ Tech Stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,sqlite" />
</p>

**Technologies:** Python • Tkinter • SQLite • SQL • CSV • Git • GitHub

---

## 🏗️ Project Structure

```text
Smart-Personal-Expense-Tracker/
│
├── database.py
├── expense_manager.py
├── gui.py
├── gui_old.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ How It Works

```text
             ┌─────────────────────┐
             │      User Input     │
             └──────────┬──────────┘
                        ↓
             ┌─────────────────────┐
             │   Tkinter GUI       │
             └──────────┬──────────┘
                        ↓
             ┌─────────────────────┐
             │ Expense Management  │
             │      Logic          │
             └──────────┬──────────┘
                        ↓
             ┌─────────────────────┐
             │   SQLite Database   │
             └──────────┬──────────┘
                        ↓
             ┌─────────────────────┐
             │ Reports / CSV Export│
             └─────────────────────┘
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Abhishek-2527/Smart-Personal-Expense-Tracker.git
```

### 2. Open the project

```bash
cd Smart-Personal-Expense-Tracker
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python gui.py
```

---

## 📊 Core Operations

| Operation  | Description                     |
| ---------- | ------------------------------- |
| ➕ Add      | Add a new expense               |
| 📋 View    | Display saved expenses          |
| ✏️ Update  | Modify an existing expense      |
| 🗑️ Delete | Remove an expense               |
| 🔍 Search  | Find specific expenses          |
| 💰 Total   | Calculate total spending        |
| 📊 Summary | View category/monthly summaries |
| 📄 Export  | Export expense data to CSV      |

---

## 🎯 Learning Outcomes

Through this project, I practiced:

* Python application development
* GUI development with Tkinter
* SQLite database integration
* SQL CRUD operations
* Data validation
* CSV data handling
* Modular Python programming
* Git & GitHub workflow

---

## 🔮 Future Improvements

Possible future enhancements include:

* 📈 Expense visualization and charts
* 🔐 User authentication
* 📱 Responsive/web version
* ☁️ Cloud database integration
* 📊 Advanced financial analytics
* 📅 Budget planning and tracking

---

## 👨‍💻 Author

### Abhishek Singh

🎓 B.Tech Computer Science Student
💻 Aspiring Software Engineer | Java Full Stack Developer

<p>
  <a href="https://github.com/Abhishek-2527">
    <img src="https://img.shields.io/badge/GitHub-Abhishek--2527-black?style=for-the-badge&logo=github" />
  </a>
</p>

---

<p align="center">
  ⭐ If you find this project useful, consider giving it a star!
</p>

<p align="center">
  <b>Built with Python ❤️</b>
</p>
