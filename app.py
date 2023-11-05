import sqlite3
from datetime import datetime

from flask import Flask, render_template, request

app = Flask(__name__)

CATEGORIES = ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Health", "Other"]


def get_db():
    db = sqlite3.connect("expenses.db")
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    db.commit()
    db.close()


init_db()


@app.route("/")
def index():
    db = get_db()
    expenses = db.execute(
        "SELECT * FROM expenses ORDER BY date DESC LIMIT 20"
    ).fetchall()
    total = db.execute("SELECT COALESCE(SUM(amount), 0) as total FROM expenses").fetchone()["total"]

    summary = db.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses GROUP BY category ORDER BY total DESC
    """).fetchall()

    db.close()
    return render_template("index.html", expenses=expenses, total=total, summary=summary, categories=CATEGORIES)


@app.route("/expenses", methods=["POST"])
def add_expense():
    description = request.form.get("description", "").strip()
    amount = request.form.get("amount", "0")
    category = request.form.get("category", "Other")
    date = request.form.get("date", datetime.now().strftime("%Y-%m-%d"))

    if not description or not amount:
        return render_template("partials/error.html", message="Description and amount are required"), 400

    db = get_db()
    db.execute(
        "INSERT INTO expenses (description, amount, category, date) VALUES (?, ?, ?, ?)",
        (description, float(amount), category, date),
    )
    db.commit()

    expenses = db.execute("SELECT * FROM expenses ORDER BY date DESC LIMIT 20").fetchall()
    total = db.execute("SELECT COALESCE(SUM(amount), 0) as total FROM expenses").fetchone()["total"]
    summary = db.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses GROUP BY category ORDER BY total DESC
    """).fetchall()
    db.close()

    return render_template("partials/dashboard.html", expenses=expenses, total=total, summary=summary, categories=CATEGORIES)


@app.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    db = get_db()
    db.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    db.commit()

    expenses = db.execute("SELECT * FROM expenses ORDER BY date DESC LIMIT 20").fetchall()
    total = db.execute("SELECT COALESCE(SUM(amount), 0) as total FROM expenses").fetchone()["total"]
    summary = db.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses GROUP BY category ORDER BY total DESC
    """).fetchall()
    db.close()

    return render_template("partials/dashboard.html", expenses=expenses, total=total, summary=summary, categories=CATEGORIES)


@app.route("/expenses/<int:expense_id>/edit", methods=["GET"])
def edit_form(expense_id):
    db = get_db()
    expense = db.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    db.close()
    if not expense:
        return "", 404
    return render_template("partials/edit_row.html", expense=expense, categories=CATEGORIES)


@app.route("/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    description = request.form.get("description", "").strip()
    amount = request.form.get("amount", "0")
    category = request.form.get("category", "Other")
    date = request.form.get("date")

    db = get_db()
    db.execute(
        "UPDATE expenses SET description = ?, amount = ?, category = ?, date = ? WHERE id = ?",
        (description, float(amount), category, date, expense_id),
    )
    db.commit()

    expenses = db.execute("SELECT * FROM expenses ORDER BY date DESC LIMIT 20").fetchall()
    total = db.execute("SELECT COALESCE(SUM(amount), 0) as total FROM expenses").fetchone()["total"]
    summary = db.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses GROUP BY category ORDER BY total DESC
    """).fetchall()
    db.close()

    return render_template("partials/dashboard.html", expenses=expenses, total=total, summary=summary, categories=CATEGORIES)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
