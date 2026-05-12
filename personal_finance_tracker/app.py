from flask import Flask, render_template, request, redirect, session, jsonify, send_file
import sqlite3
from datetime import datetime
import io
from reportlab.platypus import SimpleDocTemplate, Table

app = Flask(__name__)
app.secret_key = "secret123"

def connect_db():
    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connect_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            type TEXT,
            category TEXT,
            amount REAL,
            date TEXT
        )
    """)
    conn.close()

init_db()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = connect_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()
        if user:
            session["user"] = username
            return redirect("/")
        else:
            return "Invalid login!"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = connect_db()
        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            conn.close()
            return "Username already exists!"
    return render_template("register.html")

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        username = request.form["username"]
        new_password = request.form["new_password"]
        conn = connect_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()
        if user:
            conn.execute(
                "UPDATE users SET password=? WHERE username=?",
                (new_password, username)
            )
            conn.commit()
            conn.close()
            return redirect("/login")
        else:
            conn.close()
            return "User not found!"
    return render_template("forgot.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html", user=session["user"])

@app.route("/transactions_page")
def transactions_page():
    if "user" not in session:
        return redirect("/login")
    return render_template("transactions.html", user=session["user"])

@app.route("/report")
def report():
    if "user" not in session:
        return redirect("/login")
    return render_template("report.html", user=session["user"])

@app.route("/add", methods=["POST"])
def add():
    if "user" not in session:
        return jsonify({"error": "login required"})
    data = request.get_json()
    conn = connect_db()
    conn.execute("""
        INSERT INTO transactions (username, type, category, amount, date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        session["user"],
        data["type"],
        data["category"],
        float(data["amount"]),
        datetime.now().strftime("%Y-%m-%d")
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "added"})

@app.route("/transactions")
def transactions():
    if "user" not in session:
        return jsonify([])
    month = request.args.get("month")
    type_filter = request.args.get("type")
    conn = connect_db()
    query = "SELECT * FROM transactions WHERE username=?"
    params = [session["user"]]
    if month:
        query += " AND strftime('%Y-%m', date)=?"
        params.append(month)
    if type_filter and type_filter != "all":
        query += " AND type=?"
        params.append(type_filter)
    query += " ORDER BY id DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    result = []
    for r in rows:
        result.append({
            "id": r["id"],
            "type": r["type"],
            "category": r["category"],
            "amount": r["amount"],
            "date": r["date"]
        })
    return jsonify(result)

@app.route("/delete/<int:id>")
def delete(id):
    conn = connect_db()
    conn.execute("DELETE FROM transactions WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/transactions_page")

@app.route("/report_summary")
def summary():
    conn = connect_db()
    income = conn.execute(
        "SELECT SUM(amount) FROM transactions WHERE type='income' AND username=?",
        (session["user"],)
    ).fetchone()[0] or 0
    expense = conn.execute(
        "SELECT SUM(amount) FROM transactions WHERE type='outcome' AND username=?",
        (session["user"],)
    ).fetchone()[0] or 0
    conn.close()
    return jsonify({
        "income": income,
        "expense": expense,
        "balance": income - expense
    })

@app.route("/monthly_report")
def monthly_report():
    conn = connect_db()
    rows = conn.execute("""
        SELECT strftime('%Y-%m', date) as month,
        SUM(CASE WHEN type='income' THEN amount ELSE 0 END) as income,
        SUM(CASE WHEN type='outcome' THEN amount ELSE 0 END) as expense
        FROM transactions
        WHERE username=?
        GROUP BY month
        ORDER BY month DESC
    """, (session["user"],)).fetchall()
    conn.close()
    result = []
    for r in rows:
        income = r["income"] or 0
        expense = r["expense"] or 0
        result.append({
            "month": r["month"],
            "income": income,
            "expense": expense,
            "balance": income - expense
        })
    return jsonify(result)

@app.route("/download_pdf")
def download_pdf():
    if "user" not in session:
        return redirect("/login")
    conn = connect_db()
    rows = conn.execute("""
        SELECT date, type, category, amount
        FROM transactions
        WHERE username=?
    """, (session["user"],)).fetchall()
    conn.close()
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    data = [["Date", "Type", "Category", "Amount"]]
    for r in rows:
        data.append([
            r["date"],
            r["type"],
            r["category"],
            str(r["amount"])
        ])
    table = Table(data)
    doc.build([table])
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="report.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)
