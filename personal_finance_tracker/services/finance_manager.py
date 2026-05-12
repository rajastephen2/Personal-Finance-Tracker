from database.db import db

class FinanceManager:

    def add_transaction(self, username, type, amount, category):
        conn = db.connect()
        conn.execute("""
            INSERT INTO transactions(username, type, category, amount, date)
            VALUES (?, ?, ?, ?, DATE('now'))
        """, (username, type, category, amount))
        conn.commit()
        conn.close()


   
    def get_transactions(self, username, month=None, type_filter=None):
        conn = db.connect()
        cur = conn.cursor()

        query = "SELECT id, type, category, amount, date FROM transactions WHERE username=?"
        params = [username]

        if month:
            query += " AND strftime('%Y-%m', date)=?"
            params.append(month)

        if type_filter and type_filter != "all":
            query += " AND type=?"
            params.append(type_filter)

        query += " ORDER BY id DESC"

        rows = cur.execute(query, params).fetchall()
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

        return result