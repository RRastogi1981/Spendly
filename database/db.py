import os
import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "expense_tracker.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            description TEXT,
            date        DATE    NOT NULL,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    init_db()
    conn = get_db()
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        conn.close()
        return

    conn.executemany(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        [
            ("Nitish Kumar", "nitish@example.com", generate_password_hash("password123")),
            ("Priya Sharma",  "priya@example.com",  generate_password_hash("password123")),
        ],
    )
    conn.commit()

    user_id = conn.execute(
        "SELECT id FROM users WHERE email = ?", ("nitish@example.com",)
    ).fetchone()[0]

    from datetime import date, timedelta
    today = date.today()
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
        [
            (user_id, 4500.00, "Bills",     "Electricity bill",   str(today - timedelta(days=5))),
            (user_id, 3200.00, "Food",      "Grocery shopping",   str(today - timedelta(days=3))),
            (user_id, 2050.00, "Health",    "Pharmacy",           str(today - timedelta(days=10))),
            (user_id, 1800.00, "Transport", "Monthly metro pass", str(today - timedelta(days=1))),
            (user_id,  900.00, "Food",      "Restaurant dinner",  str(today - timedelta(days=2))),
        ],
    )
    conn.commit()
    conn.close()
