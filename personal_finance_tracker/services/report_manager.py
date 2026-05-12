from database.db import db

class ReportManager:

    def get_summary(self, username):
        conn = db.connect()

        income = conn.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE username=? AND type='income'
        """, (username,)).fetchone()[0] or 0

        expense = conn.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE username=? AND type='expense'
        """, (username,)).fetchone()[0] or 0

        conn.close()

        return {
            "income": income,
            "expense": expense,
            "balance": income - expense
        }

    def get_monthly_report(self, username):
        conn = db.connect()

        rows = conn.execute("""
        SELECT 
        strftime('%Y-%m', date) as month,
        SUM(CASE WHEN type='income' THEN amount ELSE 0 END) as income,
        SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) as expense
        FROM transactions
        WHERE username=?
        GROUP BY month
        ORDER BY month DESC
        """, (username,)).fetchall()

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

        return result