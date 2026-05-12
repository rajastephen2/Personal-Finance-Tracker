from database.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User:

    def register(self, username, password):
        conn = db.connect()
        cur = conn.cursor()

        hashed = generate_password_hash(password)

        try:
            cur.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username, hashed)
            )
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    def login(self, username, password):
        conn = db.connect()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )

        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            return user

        return None